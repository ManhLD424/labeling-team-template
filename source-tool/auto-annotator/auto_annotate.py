#!/usr/bin/env python3
"""
Công cụ tự động gán nhãn Bounding Box cho CVAT thông qua REST API & YOLO ONNX Runtime.
Tuân thủ Annotation Guideline BBox, Polygon & Polyline v1.0 (AI20K Cohort 4A - Tuần 1 Challenge).

Giải quyết Pain Point (P-004):
- Vẽ tay hàng chục đối tượng trên mỗi ảnh đường phố rất tốn thời gian.
- Dễ bỏ sót phương tiện, đèn giao thông hoặc biển báo ở xa (vi phạm tiêu chí Completeness §7).
- Tự động phát hiện và đánh dấu thuộc tính `truncated = true` khi vật thể chạm/cắt mép ảnh (§3.1).
- Tự động phát hiện và đánh dấu `occluded = true` khi các đối tượng chồng lấn nhau (§3.1).
"""

from __future__ import annotations

import argparse
import io
import os
import sys
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

# Mapping COCO class IDs sang CVAT Label Names
COCO_TO_CVAT = {
    0: "pedestrian",
    1: "bicycle",
    2: "car",
    3: "motorcycle",
    5: "bus",
    6: "train",
    7: "truck",
    9: "traffic light",
    11: "traffic sign",
}

# Mapping chuẩn BDD100K 10 classes (Khớp 100% Taxonomy của bài toán)
BDD_TO_CVAT = {
    0: "pedestrian",
    1: "rider",
    2: "car",
    3: "bus",
    4: "truck",
    5: "bicycle",
    6: "motorcycle",
    7: "traffic light",
    8: "traffic sign",
    9: "train",
}


def letterbox(
    im: np.ndarray,
    new_shape: tuple[int, int] = (640, 640),
    color: tuple[int, int, int] = (114, 114, 114),
) -> tuple[np.ndarray, float, tuple[float, float]]:
    """Giữ tỉ lệ khung hình (aspect ratio) với padding khi đưa vào YOLO."""
    shape = im.shape[:2]  # [h, w]
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    new_unpad = (int(round(shape[1] * r)), int(round(shape[0] * r)))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
    dw, dh = dw / 2, dh / 2

    if shape[::-1] != new_unpad:
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)

    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return im, r, (dw, dh)


def calculate_iou(box1: list[float], box2: list[float]) -> float:
    """Tính IoU giữa 2 box [x1, y1, x2, y2]."""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    inter_w = max(0.0, x2 - x1)
    inter_h = max(0.0, y2 - y1)
    inter_area = inter_w * inter_h

    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])

    union_area = area1 + area2 - inter_area
    if union_area <= 0:
        return 0.0
    return inter_area / union_area


def check_truncated(box: list[float], img_w: int, img_h: int, margin: int = 3) -> bool:
    """Kiểm tra box có chạm biên ảnh hay không (§3.1 Truncated)."""
    x1, y1, x2, y2 = box
    return x1 <= margin or y1 <= margin or x2 >= (img_w - margin) or y2 >= (img_h - margin)


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

    def get_labels(self, job_id: int) -> tuple[dict[str, int], dict[str, int]]:
        """Lấy id của label và attribute truncated."""
        resp = self.session.get(f"{self.server_url}/api/labels?job_id={job_id}")
        resp.raise_for_status()
        data = resp.json()

        label_map: dict[str, int] = {}
        truncated_attr_map: dict[str, int] = {}

        for item in data.get("results", []):
            name = item["name"]
            label_map[name] = item["id"]
            for attr in item.get("attributes", []):
                if attr["name"] == "truncated":
                    truncated_attr_map[name] = attr["id"]

        return label_map, truncated_attr_map

    def download_frame(self, job_id: int, frame_idx: int) -> np.ndarray:
        resp = self.session.get(
            f"{self.server_url}/api/jobs/{job_id}/data",
            params={"type": "frame", "number": frame_idx},
        )
        resp.raise_for_status()
        arr = np.frombuffer(resp.content, dtype=np.uint8)
        img_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return img_bgr

    def upload_annotations(self, job_id: int, shapes: list[dict[str, Any]]) -> dict[str, Any]:
        url = f"{self.server_url}/api/jobs/{job_id}/annotations/"
        payload = {"shapes": shapes, "tracks": [], "tags": []}
        resp = self.session.put(url, json=payload)
        resp.raise_for_status()
        return resp.json() if resp.text else {}


class YOLOAnnotator:
    def __init__(self, model_path: str | Path | None = None, conf_thresh: float = 0.25, nms_thresh: float = 0.45):
        if model_path is None:
            model_path = Path(__file__).parent / "yolo11m_bdd100k.onnx"
        model_path = Path(model_path)
        if not model_path.exists():
            print(f"Không tìm thấy model tại {model_path}. Đang tự động tải YOLO11m BDD100k về từ Hugging Face...")
            model_path.parent.mkdir(parents=True, exist_ok=True)
            import urllib.request
            url = "https://huggingface.co/banu4prasad/YOLO11m_BDD100k/resolve/main/YOLO11m.onnx"
            urllib.request.urlretrieve(url, str(model_path))
            print("✓ Tải model YOLO11m BDD100k hoàn tất!")

        self.session = ort.InferenceSession(str(model_path))
        self.conf_thresh = conf_thresh
        self.nms_thresh = nms_thresh

    def detect(self, img_bgr: np.ndarray) -> list[tuple[str, float, list[float]]]:
        """Trả về list (class_name, confidence, [x1, y1, x2, y2])."""
        h_orig, w_orig = img_bgr.shape[:2]
        img_lb, r_scale, (dw, dh) = letterbox(img_bgr, (640, 640))
        blob = cv2.cvtColor(img_lb, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        blob = blob.transpose(2, 0, 1)[np.newaxis, ...]

        preds = self.session.run(None, {"images": blob})[0][0].T
        boxes = preds[:, :4]
        scores = preds[:, 4:]
        class_ids = np.argmax(scores, axis=1)
        confidences = np.max(scores, axis=1)

        # Tự động chọn schema: BDD100k (10 classes) hay COCO (80 classes)
        num_classes = scores.shape[1]
        active_map = BDD_TO_CVAT if num_classes == 10 else COCO_TO_CVAT

        mask = confidences >= self.conf_thresh
        b_filt = boxes[mask]
        s_filt = confidences[mask]
        c_filt = class_ids[mask]

        nms_boxes = []
        for b in b_filt:
            xc, yc, bw, bh = b
            x1 = (xc - bw / 2.0 - dw) / r_scale
            y1 = (yc - bh / 2.0 - dh) / r_scale
            w = bw / r_scale
            h = bh / r_scale
            x1 = max(0.0, min(float(w_orig), x1))
            y1 = max(0.0, min(float(h_orig), y1))
            nms_boxes.append([int(x1), int(y1), int(w), int(h)])

        if not nms_boxes:
            return []

        indices = cv2.dnn.NMSBoxes(nms_boxes, s_filt.tolist(), self.conf_thresh, self.nms_thresh)
        results: list[tuple[str, float, list[float]]] = []

        for i in indices:
            idx = i if isinstance(i, (int, np.integer)) else i[0]
            cid = int(c_filt[idx])
            if cid in active_map:
                cname = active_map[cid]
                score = float(s_filt[idx])
                x, y, w, h = nms_boxes[idx]
                x2 = min(float(w_orig), float(x + w))
                y2 = min(float(h_orig), float(y + h))
                results.append((cname, score, [float(x), float(y), x2, y2]))

        return results


def process_and_annotate(
    client: CVATClient,
    detector: YOLOAnnotator,
    job_id: int,
    label_map: dict[str, int],
    truncated_map: dict[str, int],
    dry_run: bool = False,
) -> int:
    job = client.get_job(job_id)
    start_f = job.get("start_frame", 0)
    stop_f = job.get("stop_frame", 0)
    total_f = job.get("frame_count", 0)

    print(f"\n--- BẮT ĐẦU GÁN NHÃN CHO JOB {job_id} ---")
    print(f"Tổng số frames: {total_f} (từ frame {start_f} đến {stop_f})")

    all_shapes: list[dict[str, Any]] = []
    class_counter: dict[str, int] = {}
    truncated_count = 0
    occluded_count = 0

    for frame_idx in range(start_f, stop_f + 1):
        img_bgr = client.download_frame(job_id, frame_idx)
        h_img, w_img = img_bgr.shape[:2]

        detections = detector.detect(img_bgr)
        frame_shapes: list[dict[str, Any]] = []

        for i, (cname, conf, box) in enumerate(detections):
            if cname not in label_map:
                continue

            # 1. Truncated rule (§3.1)
            is_truncated = check_truncated(box, w_img, h_img)
            if is_truncated:
                truncated_count += 1

            # 2. Occluded rule (§3.1)
            is_occluded = False
            for j, (_, _, other_box) in enumerate(detections):
                if i != j and calculate_iou(box, other_box) > 0.12:
                    is_occluded = True
                    break
            if is_occluded:
                occluded_count += 1

            # 3. Attributes
            attrs: list[dict[str, Any]] = []
            if cname in truncated_map:
                attrs.append({
                    "spec_id": truncated_map[cname],
                    "value": "true" if is_truncated else "false"
                })

            shape = {
                "type": "rectangle",
                "frame": frame_idx,
                "label_id": label_map[cname],
                "points": [round(box[0], 2), round(box[1], 2), round(box[2], 2), round(box[3], 2)],
                "occluded": is_occluded,
                "outside": False,
                "attributes": attrs,
            }
            frame_shapes.append(shape)
            class_counter[cname] = class_counter.get(cname, 0) + 1

        all_shapes.extend(frame_shapes)
        print(f"  ✓ Frame {frame_idx:02d}/{stop_f:02d}: phát hiện {len(frame_shapes):2d} objects")

    print("\n--- BÁO CÁO TỔNG HỢP GÁN NHÃN ---")
    print(f"Tổng số Bounding Box sinh ra: {len(all_shapes)}")
    print(f"Số lượng vật thể truncated (cắt mép): {truncated_count}")
    print(f"Số lượng vật thể occluded (bị che): {occluded_count}")
    print("Chi tiết từng class:")
    for cname, count in sorted(class_counter.items(), key=lambda x: -x[1]):
        print(f"  • {cname:15s}: {count:3d} boxes")

    if dry_run:
        print("\n[DRY RUN] Đã chạy xong, không upload dữ liệu lên server.")
    else:
        print(f"\nĐang đẩy {len(all_shapes)} annotations lên CVAT Job {job_id}...")
        client.upload_annotations(job_id, all_shapes)
        print(f"✅ THÀNH CÔNG! Toàn bộ nhãn đã được lưu vào Job {job_id}.")
        print(f"Link xem lại: {client.server_url}/tasks/{job.get('task_id')}/jobs/{job_id}")

    return len(all_shapes)


def main() -> int:
    parser = argparse.ArgumentParser(description="Auto Annotator for CVAT BBox (Cohort 4A)")
    parser.add_argument("--job-id", type=int, default=1447, help="CVAT Job ID (mặc định 1447)")
    parser.add_argument("--server", default="https://cvat.note.transformerlabs.ai", help="CVAT Server URL")
    parser.add_argument("--token", default=None, help="Personal Access Token")
    parser.add_argument("--model", default=str(Path(__file__).parent / "yolo11m_bdd100k.onnx"), help="Đường dẫn file ONNX (mặc định YOLO11m BDD100k)")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold (mặc định 0.25)")
    parser.add_argument("--dry-run", action="store_true", help="Chạy thử nghiệm không upload")
    args = parser.parse_args()

    token = args.token or os.environ.get("CVAT_TOKEN")
    if not token:
        # Đọc từ file CVAT.txt nếu có
        token_file = Path("d:/Project/VinPrj/CVAT.txt")
        if token_file.exists():
            token = token_file.read_text(encoding="utf-8").strip()

    if not token:
        print("Lỗi: Không tìm thấy CVAT token qua --token, CVAT_TOKEN, hoặc VinPrj/CVAT.txt", file=sys.stderr)
        return 1

    client = CVATClient(args.server, token)
    user = client.verify()
    print(f"Đã kết nối CVAT thành công với tài khoản: {user.get('username')}")

    label_map, truncated_map = client.get_labels(args.job_id)
    detector = YOLOAnnotator(args.model, conf_thresh=args.conf)

    process_and_annotate(
        client=client,
        detector=detector,
        job_id=args.job_id,
        label_map=label_map,
        truncated_map=truncated_map,
        dry_run=args.dry_run,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
