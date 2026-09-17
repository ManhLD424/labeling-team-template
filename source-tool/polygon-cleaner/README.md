# Polygon Cleaner & Taxonomy Remapper Tool (Team T030)

Công cụ chuẩn hóa Taxonomy và làm sạch đa giác phân đoạn cho các tập dữ liệu YOLO Segmentation của Đội **T030**.

---

## 1. Mục đích & Vấn đề giải quyết

1. **[P-006](../../problem-backlog.md#p-006) — Lệch Taxonomy & Alias Class**:
   Tự động phát hiện và remap các nhãn lệch danh mục về chuẩn của đội:
   - `28` (`person`) $\to$ `0` (`pedestrian`)
   - `29` (`traffic_light`) $\to$ `8` (`traffic light`)
   - `30` (`traffic_sign`) $\to$ `9` (`traffic sign`)

2. **[P-007](../../problem-backlog.md#p-007) — Đa giác phân mảnh & Đa giác rác**:
   - Tự động tính toán diện tích thực (pixel) của từng đa giác bằng thuật toán Green / `cv2.contourArea`.
   - Lọc bỏ các đa giác suy biến (degenerate $< 1\text{ px}^2$ hoặc $< 3$ điểm).
   - Lọc bỏ các đa giác rác $< 10\text{ px}^2$ sinh ra do click lỗi khi gán nhãn thủ công.

---

## 2. Hướng dẫn sử dụng

### 2.1. Chạy chế độ kiểm toán (Dry Run - Không ghi đè)
```bash
python source-tool/polygon-cleaner/clean_and_remap.py --dry-run
```

### 2.2. Chạy làm sạch và ghi đè trực tiếp (In-place)
```bash
python source-tool/polygon-cleaner/clean_and_remap.py --in-place
```

### 2.3. Xuất kết quả sang một thư mục mới
```bash
python source-tool/polygon-cleaner/clean_and_remap.py --output-dir data/cleaned_labels/
```
