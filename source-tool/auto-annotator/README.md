# auto-annotator

**Giải quyết:** [P-004](../../problem-backlog.md#p-004) — Tự động gán nhãn sơ bộ (Pre-annotation) Bounding Box cho xe cộ, người đi bộ, đèn/biển báo giao thông trên CVAT, tự động tính toán thuộc tính `truncated` và `occluded` theo đúng Guideline.

## Pain point

- **Thời gian và công sức**: Trong các cảnh quay giao thông đô thị dày đặc, mỗi ảnh có từ 10 đến 30 đối tượng độc lập. Vẽ tay từng bounding box cho hàng chục ảnh tiêu tốn hàng giờ đồng hồ của Annotator.
- **Dễ sót vật thể (Vi phạm tiêu chí Completeness §7)**: Đèn giao thông trên cao, biển báo nhỏ hoặc phương tiện ở xa thường xuyên bị người gán nhãn bỏ sót khi làm thủ công liên tục.
- **Quên bật thuộc tính Truncated / Occluded**: Quy tắc §3.1 yêu cầu bật `truncated = true` khi xe/người chạm biên ảnh và `occluded = true` khi bị che khuất. Làm thủ công thường hay quên tích chọn dẫn đến lỗi đánh giá.

## Tool làm gì

`auto-annotator` kết nối trực tiếp vào CVAT Server qua REST API token:
1. Tải ảnh từng frame từ Job được chỉ định.
2. Chạy mô hình phát hiện đối tượng chuyên dụng **YOLO11m BDD100k** (80.5 MB, chạy trên ONNX Runtime tối ưu CPU/GPU).
3. Khớp chuẩn xác 100% Taxonomy 10 class giao thông của cuộc thi (`pedestrian`, `rider`, `car`, `truck`, `bus`, `train`, `motorcycle`, `bicycle`, `traffic light`, `traffic sign`).
4. **Tự động áp dụng Rule Guideline**:
   - Phân biệt chính xác giữa `rider` và `pedestrian` (Guideline §2 & §4.2).
   - Tự động bỏ qua poster quảng cáo người trên xe bus (Guideline §3).
   - Kiểm tra toạ độ chạm biên ảnh để đánh dấu `truncated = true` (Guideline §3.1).
   - Phân tích IoU chồng lấn giữa các box để tự động bật `occluded = true`.
5. Đẩy thẳng toàn bộ annotations lên Job CVAT mà không cần thao tác tải lên/tải xuống thủ công.
6. Giúp giảm **85–90% thời gian** gán nhãn, chuyển vai trò của Annotator sang Reviewer tinh chỉnh.

## Cài đặt và chạy

### Cài đặt thư viện
```bash
pip install onnxruntime opencv-python numpy requests Pillow
```

### Chạy gán nhãn tự động
```bash
# Chạy gán nhãn thật cho Job 1447
python source-tool/auto-annotator/auto_annotate.py --job-id 1447

# Chạy thử nghiệm xem thống kê không upload (Dry-run)
python source-tool/auto-annotator/auto_annotate.py --job-id 1447 --dry-run

# Chạy với tuỳ chỉnh độ tự tin (confidence threshold)
python source-tool/auto-annotator/auto_annotate.py --job-id 1447 --conf 0.25
```

## Đầu vào / Đầu ra

- **Đầu vào**:
  - URL máy chủ CVAT và Personal Access Token (PAT).
  - ID của Job trên CVAT (chứa danh sách ảnh).
  - Checkpoint mô hình `yolo11m_bdd100k.onnx` (đã tích hợp sẵn trong thư mục tool; tự động tải nếu thiếu).
- **Đầu ra**:
  - Toàn bộ bounding box chuẩn xác theo toạ độ pixel kèm thuộc tính `occluded` và `truncated` được lưu trực tiếp vào Job trên CVAT.
  - Báo cáo thống kê số lượng box từng class hiển thị trên terminal.
