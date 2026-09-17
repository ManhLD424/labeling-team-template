#!/usr/bin/env python3
"""
Công cụ chuẩn hóa Taxonomy và làm sạch đa giác phân đoạn (Polygon Cleaner & Remapper).
Phát triển bởi Đội T030 (P-030) - AI20K Build Phase Cohort 4A.

Giải quyết trực tiếp 2 Pain Points:
1. [P-006]: Lệch chuẩn định danh Class ID (Alias classes: 28->0, 29->8, 30->9).
2. [P-007]: Đa giác rác và phân mảnh siêu nhỏ (< 10 px² hoặc suy biến < 1 px²).
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import cv2
import numpy as np

# Bảng ánh xạ chuẩn hóa class ID
ALIAS_REMAP = {
    28: 0,   # person -> pedestrian
    29: 8,   # traffic_light -> traffic light
    30: 9,   # traffic_sign -> traffic sign
}

def process_label_file(
    file_path: Path,
    out_path: Path | None,
    img_w: int = 1280,
    img_h: int = 720,
    min_area: float = 10.0,
    dry_run: bool = False,
) -> dict:
    """Xử lý 1 tệp nhãn YOLO segmentation: remap và lọc bỏ đa giác rác."""
    lines = file_path.read_text(encoding="utf-8").strip().splitlines()
    
    total_before = 0
    remapped_count = 0
    removed_tiny_count = 0
    removed_degen_count = 0
    kept_lines = []

    for idx, line in enumerate(lines):
        if not line.strip():
            continue
        total_before += 1
        parts = line.strip().split()
        cls_id = int(parts[0])
        coords_raw = [float(x) for x in parts[1:]]

        # Kiểm tra suy biến
        if len(coords_raw) < 6:
            removed_degen_count += 1
            continue

        # Tính diện tích thực theo pixel
        pts = np.array(coords_raw, dtype=np.float32).reshape(-1, 2)
        pts[:, 0] *= img_w
        pts[:, 1] *= img_h
        area = cv2.contourArea(pts.astype(np.float32))

        if area < 1.0:
            removed_degen_count += 1
            continue
        if area < min_area:
            removed_tiny_count += 1
            continue

        # Remap class nếu là alias
        new_cls_id = ALIAS_REMAP.get(cls_id, cls_id)
        if new_cls_id != cls_id:
            remapped_count += 1

        # Lưu lại dòng hợp lệ
        new_line = f"{new_cls_id} " + " ".join(parts[1:])
        kept_lines.append(new_line)

    if not dry_run and out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("\n".join(kept_lines) + ("\n" if kept_lines else ""), encoding="utf-8")

    return {
        "file": file_path.name,
        "total_before": total_before,
        "total_after": len(kept_lines),
        "remapped": remapped_count,
        "removed_tiny": removed_tiny_count,
        "removed_degen": removed_degen_count,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean and remap YOLO segmentation polygons (Team T030)")
    parser.add_argument(
        "--labels-dir",
        default="submissions/w1-segmentation-G04-Danh/labels/train/w1/segmentation/G04",
        help="Thư mục chứa các tệp txt nhãn",
    )
    parser.add_argument("--output-dir", default=None, help="Thư mục xuất kết quả (nếu None sẽ ghi đè khi có --in-place)")
    parser.add_argument("--in-place", action="store_true", help="Ghi đè trực tiếp lên tệp nguồn")
    parser.add_argument("--min-area", type=float, default=10.0, help="Diện tích tối thiểu (px^2), mặc định 10.0")
    parser.add_argument("--dry-run", action="store_true", help="Chạy kiểm toán không sửa file")
    parser.add_argument("--width", type=int, default=1280, help="Độ rộng ảnh gốc (mặc định 1280)")
    parser.add_argument("--height", type=int, default=720, help="Độ cao ảnh gốc (mặc định 720)")
    args = parser.parse_args()

    lbl_dir = Path(args.labels_dir)
    if not lbl_dir.is_absolute():
        lbl_dir = Path("d:/Project/labeling-team-template") / lbl_dir

    if not lbl_dir.exists():
        print(f"Lỗi: Không tìm thấy thư mục nhãn tại {lbl_dir}", file=sys.stderr)
        return 1

    files = sorted(list(lbl_dir.glob("*.txt")))
    if not files:
        print(f"Cảnh báo: Không có tệp .txt nào trong {lbl_dir}")
        return 0

    print(f"=== KHỞI CHẠY KIỂM ĐỊNH & LÀM SẠCH ĐA GIÁC (TEAM T030) ===")
    print(f"Thư mục nguồn: {lbl_dir}")
    print(f"Tổng số tệp: {len(files)} tệp")
    print(f"Ngưỡng diện tích lọc bỏ: < {args.min_area} px^2")
    print(f"Chế độ: {'DRY RUN (Chỉ kiểm toán)' if args.dry_run else ('IN-PLACE (Ghi đè)' if args.in_place else 'OUTPUT TO NEW DIR')}")
    print("-" * 65)

    tot_before = 0
    tot_after = 0
    tot_remapped = 0
    tot_tiny = 0
    tot_degen = 0

    for f in files:
        out_f = f if args.in_place else (Path(args.output_dir) / f.name if args.output_dir else None)
        stat = process_label_file(
            file_path=f,
            out_path=out_f,
            img_w=args.width,
            img_h=args.height,
            min_area=args.min_area,
            dry_run=args.dry_run,
        )
        tot_before += stat["total_before"]
        tot_after += stat["total_after"]
        tot_remapped += stat["remapped"]
        tot_tiny += stat["removed_tiny"]
        tot_degen += stat["removed_degen"]
        print(
            f"  {stat['file']:15s}: {stat['total_before']:3d} -> {stat['total_after']:3d} polygons | "
            f"Lệch: {stat['remapped']:2d} | Rác <10px: {stat['removed_tiny']:2d} | Suy biến: {stat['removed_degen']:2d}"
        )

    print("-" * 65)
    print("=== BÁO CÁO TỔNG HỢP KIỂM TOÁN DỮ LIỆU ===")
    print(f"Tổng số đa giác ban đầu: {tot_before}")
    print(f"Tổng số đa giác sau làm sạch: {tot_after} (giảm {tot_before - tot_after} đa giác rác ~ {(tot_before - tot_after)/tot_before*100:.1f}%)")
    print(f"Số đối tượng remap taxonomy (P-006): {tot_remapped} objects")
    print(f"Số đa giác siêu nhỏ < {args.min_area} px^2 (P-007): {tot_tiny} objects")
    print(f"Số đa giác suy biến degenerate < 1 px^2: {tot_degen} objects")
    print("==========================================")
    return 0


if __name__ == "__main__":
    sys.exit(main())
