#!/usr/bin/env python3
"""
Cong cu tu dong phan doan ngu nghia (Semantic Segmentation) chuan CVAT Brush/Mask.
Tuan thu Semantic Segmentation Annotation Guideline (AI20K Cohort 4A - Tuan 1 Challenge).

Cac cai tien vuot troi:
- Xuat truc tiep dinh dang Bitmask / RLE Mask ban dia cua CVAT (type: mask).
- Bilinear Interpolation tren 19-class Logits de tao duong bien min mang, khong con rang cua 8px.
- Ket hop YOLO11m BDD100k de cuu cac vung phuong tien bi mo do kinh lai xuoc/ban hoac loa sang.
- Vung nen lon (road, sidewalk, building, sky, vegetation): moi lop gom dung 1 Mask thong nhat, lien khoi (Z=0).
- Vat the tien canh (car, truck, bus, person, rider, pole, traffic_light, traffic_sign): tach thanh cac instance mask ro rang (Z=1).
- Khong co lo gia giua cac lop, khong gay qua tai danh sach Objects tren CVAT.
"""

from __future__ import annotations

import argparse
import io
import os
import sys
import urllib.request
from itertools import groupby
from pathlib import Path
from typing import Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import cv2
import numpy as np
import onnxruntime as ort
import requests

# Bang ma 19 class Cityscapes theo Section 2 Guideline
CITYSCAPES_19_CLASSES = [
    ("road", "#804080", (128, 64, 128)),            # 0
    ("sidewalk", "#F423E8", (232, 35, 244)),        # 1
    ("building", "#464646", (70, 70, 70)),          # 2
    ("wall", "#66669C", (156, 102, 102)),           # 3
    ("fence", "#BE9999", (153, 153, 190)),          # 4
    ("pole", "#999999", (153, 153, 153)),           # 5
    ("traffic_light", "#FAAA1E", (30, 170, 250)),   # 6
    ("traffic_sign", "#DCDC00", (0, 220, 220)),     # 7
    ("vegetation", "#6B8E23", (35, 142, 107)),      # 8
    ("terrain", "#98FB98", (152, 251, 152)),        # 9
    ("sky", "#4682B4", (180, 130, 70)),             # 10
    ("person", "#DC143C", (60, 20, 220)),           # 11
    ("rider", "#FF0000", (0, 0, 255)),              # 12
    ("car", "#00008E", (142, 0, 0)),                # 13
    ("truck", "#000046", (70, 0, 0)),               # 14
    ("bus", "#003C64", (100, 60, 0)),               # 15
    ("train", "#005064", (100, 80, 0)),             # 16
    ("motorcycle", "#0000E6", (230, 0, 0)),         # 17
    ("bicycle", "#770B20", (32, 11, 119)),          # 18
]

# Nhom cac lop nen (Background)
BACKGROUND_CLASSES = {
    "road", "sidewalk", "building", "wall", "fence",
    "vegetation", "terrain", "sky"
}

# Mapping sang ten tren CVAT
CITYSCAPES_TO_CVAT_ALIASES = {
    "road": ["road"],
    "sidewalk": ["sidewalk"],
    "building": ["building", "buildings"],
    "wall": ["wall"],
    "fence": ["fence"],
    "pole": ["pole"],
    "traffic_light": ["traffic light", "traffic_light"],
    "traffic_sign": ["traffic sign", "traffic_sign"],
    "vegetation": ["vegetation"],
    "terrain": ["terrain"],
    "sky": ["sky"],
    "person": ["pedestrian", "person"],
    "rider": ["rider"],
    "car": ["car"],
    "truck": ["truck"],
    "bus": ["bus"],
    "train": ["train"],
    "motorcycle": ["motorcycle"],
    "bicycle": ["bicycle"],
}

# Mapping BDD100K class ID sang Cityscapes class ID
BDD_TO_CITYSCAPES = {
    0: 11,  # pedestrian -> person
    1: 12,  # rider -> rider
    2: 13,  # car -> car
    3: 14,  # truck -> truck
    4: 15,  # bus -> bus
    5: 16,  # train -> train
    6: 17,  # motorcycle -> motorcycle
    7: 18,  # bicycle -> bicycle
    8: 6,   # traffic light -> traffic_light
    9: 7,   # traffic sign -> traffic_sign
}


def mask_to_cvat_rle(mask_2d: np.ndarray) -> list[int] | None:
    """Chuyen doi 2D numpy binary mask thanh format RLE chuan cua CVAT.
    Cau truc points trong CVAT bat buoc la: [...rle_counts, left, top, right, bottom]
    """
    rows = np.any(mask_2d, axis=1)
    cols = np.any(mask_2d, axis=0)
    if not np.any(rows) or not np.any(cols):
        return None
    ymin, ymax = int(np.where(rows)[0][0]), int(np.where(rows)[0][-1])
    xmin, xmax = int(np.where(cols)[0][0]), int(np.where(cols)[0][-1])
    cropped = (mask_2d[ymin:ymax + 1, xmin:xmax + 1] > 0).astype(np.uint8).flatten()

    rle: list[int] = []
    prev = 0
    summ = 0
    for val in cropped:
        if val != prev:
            rle.append(summ)
            prev = val
            summ = 1
        else:
            summ += 1
    rle.append(summ)

    # Bounding box coordinates [left, top, right, bottom] PHAI o 4 vi tri cuoi cung
    return rle + [xmin, ymin, xmax, ymax]


class CVATClient:
    def __init__(self, server_url: str, token: str):
        self.server_url = server_url.rstrip("/")
        self.auth_headers = {"Authorization": f"Bearer {token}"}
        self.session = requests.Session()
        self.session.headers.update(self.auth_headers)

    def verify(self) -> dict[str, Any]:
        resp = self.session.get(f"{self.server_url}/api/users/self")
        resp.raise_for_status()
        return resp.json()

    def get_job(self, job_id: int) -> dict[str, Any]:
        resp = self.session.get(f"{self.server_url}/api/jobs/{job_id}")
        resp.raise_for_status()
        return resp.json()

    def get_labels(self, job_id: int) -> dict[str, dict[str, Any]]:
        resp = self.session.get(f"{self.server_url}/api/labels?job_id={job_id}&page_size=100")
        resp.raise_for_status()
        data = resp.json()

        label_map: dict[str, dict[str, Any]] = {}
        for item in data.get("results", []):
            name = item["name"]
            label_map[name] = {
                "id": item["id"],
                "type": item.get("type", "any"),
                "color": item.get("color", "#000000"),
            }
        return label_map

    def download_frame(self, job_id: int, frame_idx: int) -> np.ndarray:
        resp = self.session.get(
            f"{self.server_url}/api/jobs/{job_id}/data",
            params={"type": "frame", "number": frame_idx},
        )
        resp.raise_for_status()
        arr = np.frombuffer(resp.content, dtype=np.uint8)
        return cv2.imdecode(arr, cv2.IMREAD_COLOR)

    def upload_annotations(self, job_id: int, shapes: list[dict[str, Any]]) -> dict[str, Any]:
        url = f"{self.server_url}/api/jobs/{job_id}/annotations/"
        payload = {"shapes": shapes, "tracks": [], "tags": []}
        resp = self.session.put(url, json=payload)
        resp.raise_for_status()
        return resp.json() if resp.text else {}


class HybridSegmenter:
    """Ket hop SegFormer-B2 (Semantic Background) va YOLO11x-seg (SOTA Instance Segmentation)."""
    def __init__(
        self,
        segformer_path: str | Path | None = None,
        yolo_path: str | Path | None = None,
    ):
        # 1. Background Segmenter (Uu tien SegFormer-B2 1024x1024)
        if segformer_path is None:
            cand_b2 = Path(__file__).parent / "segformer_b2_cityscapes.onnx"
            cand_b0 = Path(__file__).parent / "segformer_b0_cityscapes.onnx"
            segformer_path = cand_b2 if cand_b2.exists() else cand_b0
        segformer_path = Path(segformer_path)

        if not segformer_path.exists():
            print(f"Chua co SegFormer tai {segformer_path}. Dang tai tu Hugging Face...")
            segformer_path.parent.mkdir(parents=True, exist_ok=True)
            url = "https://huggingface.co/Xenova/segformer-b0-finetuned-cityscapes-640-1280/resolve/main/onnx/model.onnx"
            urllib.request.urlretrieve(url, str(segformer_path))
            print("Tai SegFormer hoan tat.")

        self.seg_session = ort.InferenceSession(str(segformer_path))
        self.is_b2 = "b2" in segformer_path.name.lower()
        print(f"Da tich hop Background Model: {segformer_path.name} (B2 Mode: {self.is_b2})")

        self.mean = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(1, 1, 3)
        self.std = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(1, 1, 3)

        # 2. Foreground Instance Segmenter (Uu tien Flagship YOLO11x-seg)
        if yolo_path is None:
            cand_x = Path(__file__).parent / "yolo11x-seg.pt"
            cand_m = Path(__file__).resolve().parent.parent / "auto-annotator" / "yolo11m_bdd100k.onnx"
            if cand_x.exists():
                yolo_path = cand_x
            elif cand_m.exists():
                yolo_path = cand_m

        self.yolo_seg = None
        self.yolo_session = None
        if yolo_path and Path(yolo_path).exists():
            if str(yolo_path).endswith(".pt"):
                from ultralytics import YOLO
                self.yolo_seg = YOLO(str(yolo_path))
                print(f"Da tich hop SOTA Flagship Instance Model: {Path(yolo_path).name}")
            else:
                self.yolo_session = ort.InferenceSession(str(yolo_path))
                print(f"Da tich hop YOLO BBox Model: {Path(yolo_path).name}")

    def infer(self, img_bgr: np.ndarray) -> tuple[np.ndarray, list[dict[str, Any]]]:
        h_orig, w_orig = img_bgr.shape[:2]

        # 1. SegFormer chay Background scene
        inp_size = (1024, 1024) if self.is_b2 else (1280, 640)
        img_rgb = cv2.cvtColor(cv2.resize(img_bgr, inp_size), cv2.COLOR_BGR2RGB)
        norm = ((img_rgb / 255.0) - self.mean) / self.std
        blob = norm.transpose(2, 0, 1)[np.newaxis, ...].astype(np.float32)

        out_seg = self.seg_session.run(None, {"pixel_values": blob})[0][0]

        logits = np.zeros((19, h_orig, w_orig), dtype=np.float32)
        for c in range(19):
            logits[c] = cv2.resize(out_seg[c], (w_orig, h_orig), interpolation=cv2.INTER_LINEAR)

        logits[16] = -1e9  # train

        # Triet tieu nhieu tuong/hang rao bat thuong o nua duoi mat duong
        corridor_y = int(h_orig * 0.64)
        logits[2, corridor_y:, int(w_orig * 0.08):int(w_orig * 0.92)] = -1e9
        logits[3, corridor_y:, int(w_orig * 0.08):int(w_orig * 0.92)] = -1e9
        logits[4, corridor_y:, int(w_orig * 0.08):int(w_orig * 0.92)] = -1e9

        pred = np.argmax(logits, axis=0).astype(np.uint8)

        # Dong kin mat duong (road)
        road_mask = (pred == 0).astype(np.uint8)
        kernel_road = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        road_closed = cv2.morphologyEx(road_mask, cv2.MORPH_CLOSE, kernel_road)
        pred[road_closed > 0] = 0

        # 2. Trich xuat SOTA Foreground Instance tu YOLO11x-seg
        fg_instances: list[dict[str, Any]] = []

        if self.yolo_seg is not None:
            res = self.yolo_seg(img_bgr, conf=0.30, retina_masks=True, verbose=False)
            COCO_TO_CITYSCAPES = {
                "person": (11, "person"),
                "bicycle": (18, "bicycle"),
                "car": (13, "car"),
                "motorcycle": (17, "motorcycle"),
                "bus": (15, "bus"),
                "train": (16, "train"),
                "truck": (14, "truck"),
                "traffic light": (6, "traffic_light"),
                "stop sign": (7, "traffic_sign"),
            }

            if res[0].masks is not None:
                for i, (box, cls_id, conf) in enumerate(zip(
                    res[0].boxes.xyxy.cpu().numpy(),
                    res[0].boxes.cls.cpu().numpy(),
                    res[0].boxes.conf.cpu().numpy(),
                )):
                    cname = self.yolo_seg.names[int(cls_id)]
                    if cname not in COCO_TO_CITYSCAPES:
                        continue

                    cs_id, target_label = COCO_TO_CITYSCAPES[cname]
                    x1, y1, x2, y2 = [int(v) for v in box]

                    # Loai bo nap ca-po xe quay o duoi day anh
                    if (x2 - x1) > w_orig * 0.90 and y2 > h_orig * 0.95:
                        continue

                    m = res[0].masks.data[i].cpu().numpy().astype(np.uint8)
                    area = int(np.count_nonzero(m))
                    if area < 60:
                        continue

                    # Ghi de truc tiep len pred de background road khong the nuot vat the
                    pred[m > 0] = cs_id

                    fg_instances.append({
                        "label_name": target_label,
                        "cityscapes_id": cs_id,
                        "conf": float(conf),
                        "box": [x1, y1, x2, y2],
                        "mask": m,
                        "area": area,
                    })

        return pred, fg_instances

    def create_colored_overlay(self, img_bgr: np.ndarray, mask: np.ndarray, alpha: float = 0.5) -> np.ndarray:
        color_mask = np.zeros_like(img_bgr)
        for cid, (_, _, bgr_color) in enumerate(CITYSCAPES_19_CLASSES):
            color_mask[mask == cid] = bgr_color
        return cv2.addWeighted(img_bgr, 1.0 - alpha, color_mask, alpha, 0)


def process_segmentation(
    client: CVATClient,
    model: HybridSegmenter,
    job_id: int,
    cvat_labels: dict[str, dict[str, Any]],
    vis_dir: Path | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    job = client.get_job(job_id)
    start_f = job.get("start_frame", 0)
    stop_f = job.get("stop_frame", 0)
    total_f = job.get("frame_count", 0)

    print(f"\n=======================================================")
    print(f"   TIEN HANH PHAN DOAN SOTA PANOPTIC FUSION CHO JOB {job_id}")
    print(f"=======================================================")
    print(f"Tong so frame: {total_f} (tu frame {start_f} den {stop_f})")
    print(f"Tong so nhan ho tro tren CVAT: {len(cvat_labels)}")

    if vis_dir:
        vis_dir.mkdir(parents=True, exist_ok=True)
        print(f"Luu anh visual inspection tai: {vis_dir}")

    all_shapes: list[dict[str, Any]] = []
    class_shape_counts: dict[str, int] = {}
    class_pixel_counts: dict[str, int] = {c[0]: 0 for c in CITYSCAPES_19_CLASSES}
    total_pixels = 0

    for frame_idx in range(start_f, stop_f + 1):
        img_bgr = client.download_frame(job_id, frame_idx)
        h_orig, w_orig = img_bgr.shape[:2]
        total_pixels += h_orig * w_orig

        clean_mask, fg_instances = model.infer(img_bgr)

        # Luu visual overlay
        if vis_dir:
            vis_img = model.create_colored_overlay(img_bgr, clean_mask, alpha=0.45)
            cv2.putText(vis_img, f"Frame {frame_idx:02d} - SOTA Fusion", (15, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
            out_file = vis_dir / f"frame_{frame_idx:04d}_clean.jpg"
            cv2.imwrite(str(out_file), vis_img)

        frame_shapes: list[dict[str, Any]] = []

        # 1. Nap Background classes (Z-order = 0)
        for cid, (cname, _, _) in enumerate(CITYSCAPES_19_CLASSES):
            if cname not in BACKGROUND_CLASSES:
                continue

            c_mask = (clean_mask == cid).astype(np.uint8)
            px_count = int(np.count_nonzero(c_mask))
            if px_count < 100:
                continue

            class_pixel_counts[cname] += px_count

            target_cvat_name = None
            for alias in CITYSCAPES_TO_CVAT_ALIASES.get(cname, [cname]):
                if alias in cvat_labels:
                    target_cvat_name = alias
                    break

            if not target_cvat_name:
                continue

            label_info = cvat_labels[target_cvat_name]
            label_id = label_info["id"]

            pts = mask_to_cvat_rle(c_mask)
            if pts:
                frame_shapes.append({
                    "type": "mask",
                    "frame": frame_idx,
                    "label_id": label_id,
                    "points": pts,
                    "occluded": False,
                    "outside": False,
                    "z_order": 0,
                    "attributes": [],
                })
                class_shape_counts[target_cvat_name] = class_shape_counts.get(target_cvat_name, 0) + 1

        # 2. Nap Foreground Instances tu SOTA YOLO11x-seg (Z-order = 1)
        handled_fg_classes = set()
        for inst in fg_instances:
            target_name = inst["label_name"]
            target_cvat_name = None
            for alias in CITYSCAPES_TO_CVAT_ALIASES.get(target_name, [target_name]):
                if alias in cvat_labels:
                    target_cvat_name = alias
                    break

            if not target_cvat_name:
                continue

            label_info = cvat_labels[target_cvat_name]
            label_id = label_info["id"]
            handled_fg_classes.add(inst["cityscapes_id"])

            pts = mask_to_cvat_rle(inst["mask"])
            if pts:
                frame_shapes.append({
                    "type": "mask",
                    "frame": frame_idx,
                    "label_id": label_id,
                    "points": pts,
                    "occluded": False,
                    "outside": False,
                    "z_order": 1,
                    "attributes": [],
                })
                class_shape_counts[target_cvat_name] = class_shape_counts.get(target_cvat_name, 0) + 1
                cname = CITYSCAPES_19_CLASSES[inst["cityscapes_id"]][0]
                class_pixel_counts[cname] += inst["area"]

        # 3. Fallback cho cac lop Thing con lai (vi du: pole, train...) chua co trong YOLO
        for cid, (cname, _, _) in enumerate(CITYSCAPES_19_CLASSES):
            if cname in BACKGROUND_CLASSES or cid in handled_fg_classes:
                continue

            c_mask = (clean_mask == cid).astype(np.uint8)
            num_l, lbls, stats, _ = cv2.connectedComponentsWithStats(c_mask)
            target_cvat_name = None
            for alias in CITYSCAPES_TO_CVAT_ALIASES.get(cname, [cname]):
                if alias in cvat_labels:
                    target_cvat_name = alias
                    break

            if not target_cvat_name:
                continue

            label_info = cvat_labels[target_cvat_name]
            label_id = label_info["id"]

            for i in range(1, num_l):
                area = stats[i, cv2.CC_STAT_AREA]
                if area < 80:
                    continue
                inst_m = (lbls == i).astype(np.uint8)
                pts = mask_to_cvat_rle(inst_m)
                if pts:
                    frame_shapes.append({
                        "type": "mask",
                        "frame": frame_idx,
                        "label_id": label_id,
                        "points": pts,
                        "occluded": False,
                        "outside": False,
                        "z_order": 1,
                        "attributes": [],
                    })
                    class_shape_counts[target_cvat_name] = class_shape_counts.get(target_cvat_name, 0) + 1
                    class_pixel_counts[cname] += area

        all_shapes.extend(frame_shapes)
        print(f"  Frame {frame_idx:02d}/{stop_f:02d}: {len(frame_shapes):2d} clean SOTA masks")

    print("\n=======================================================")
    print("      BAO CAO KIEM TOAN RASTER MASK CHO JOB 1663")
    print("=======================================================")
    print(f"Tong so Mask tao ra cho CVAT: {len(all_shapes)}")
    print("So luong Mask theo tung nhan:")
    for cname, count in sorted(class_shape_counts.items(), key=lambda x: -x[1]):
        print(f"  - {cname:15s}: {count:3d} masks")

    print("\nPhan bo dien tich mat phang tren 25 anh:")
    for cname, px in sorted(class_pixel_counts.items(), key=lambda x: -x[1]):
        pct = (px / total_pixels) * 100.0
        if pct > 0.05:
            print(f"  - {cname:15s}: {pct:5.2f}% ({px:,} px)")

    if dry_run:
        print("\n[DRY RUN] Hoan tat kiem tra. Khong upload len CVAT.")
    else:
        print(f"\nDang tai {len(all_shapes)} clean masks len CVAT Job {job_id}...")
        client.upload_annotations(job_id, all_shapes)
        print(f"Hoan tat! Toan bo mask sach da duoc luu vao Job {job_id}.")
        print(f"Link xem lai: {client.server_url}/tasks/{job.get('task_id')}/jobs/{job_id}")

    return {
        "total_shapes": len(all_shapes),
        "class_shape_counts": class_shape_counts,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean Raster Mask Annotator for CVAT")
    parser.add_argument("--job-id", type=int, default=1663, help="CVAT Job ID")
    parser.add_argument("--dry-run", action="store_true", help="Chay thu nghiem khong upload")
    parser.add_argument("--no-vis", action="store_true", help="Khong xuat anh visual overlay")
    parser.add_argument("--vis-dir", type=str, default="vis_clean_masks_1663", help="Thu muc luu anh overlay")
    args = parser.parse_args()

    token_path = Path("d:/Project/VinPrj/CVAT.txt")
    if not token_path.exists():
        print(f"Loi: Khong tim thay token tai {token_path}")
        return 1

    token = token_path.read_text(encoding="utf-8").strip()
    server_url = "https://cvat.note.transformerlabs.ai"

    client = CVATClient(server_url, token)
    user_info = client.verify()
    print(f"Ket noi CVAT thanh cong: {user_info.get('username')}")

    cvat_labels = client.get_labels(args.job_id)
    print(f"Job {args.job_id} co san {len(cvat_labels)} nhan tren CVAT")

    model = HybridSegmenter()
    vis_dir = None if args.no_vis else Path(args.vis_dir)

    process_segmentation(
        client=client,
        model=model,
        job_id=args.job_id,
        cvat_labels=cvat_labels,
        vis_dir=vis_dir,
        dry_run=args.dry_run,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
