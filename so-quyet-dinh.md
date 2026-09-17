# Sổ quyết định

Ghi lại những gì đội đã chốt, và **vì sao**. Ba tuần sau không ai còn nhớ vì sao box lại vẽ
kiểu này — người mới vào đội lại càng không.

**Quyết định đã ghi thì không sửa nội dung.** Đổi ý thì ghi một quyết định mới, và chuyển
trạng thái quyết định cũ thành *Bị thay bởi QĐ-xxx*. Nhờ vậy vẫn truy được vì sao các job
cũ được gán theo cách cũ.

> Các mục bên dưới là **ví dụ**. Mẫu trống để copy nằm cuối file.

## Danh sách

| Mã | Quyết định | Ngày | Xuất phát từ | Trạng thái |
|---|---|---|---|---|
| [QĐ-001](#qđ-001) | Người ngồi sau xe máy có box `rider`/`pedestrian` riêng | 15/09/2026 | [P-001](problem-backlog.md#p-001) | Hiệu lực |
| [QĐ-002](#qđ-002) | Reviewer trả nguyên job khi mẫu kiểm có trên 10% ảnh sai | 16/09/2026 | Quy trình QA Đội | Hiệu lực |
| [QĐ-003](#qđ-003) | Chuẩn hóa Pre-annotation bằng YOLO11m và logic tự động truncated/occluded | 17/09/2026 | [P-003](problem-backlog.md#p-003), [P-004](problem-backlog.md#p-004) | Hiệu lực |
| [QĐ-004](#qđ-004) | Chuẩn hóa RLE Mask, Zero Overlap và phân tầng Z-order cho Semantic Segmentation | 17/09/2026 | [P-005](problem-backlog.md#p-005) | Hiệu lực |

**Trạng thái:** Hiệu lực · Bị thay bởi QĐ-xxx · Huỷ (ghi lý do)

---

## QĐ-001

**Người ngồi sau xe máy có box `rider`/`pedestrian` riêng**

- **Ngày:** 15/09/2026
- **Người tham gia:** Lê Đức Mạnh (chốt), Võ Trọng Nghĩa, Vũ Việt Long, Tống Thanh Danh, Phạm Hoàng Anh
- **Xuất phát từ:** [P-001](problem-backlog.md#p-001)
- **Bối cảnh:** §3.2 của guideline nói mỗi người một box, nhưng hình minh hoạ lại vẽ chung một box cho cả xe máy lẫn người trên xe. Các annotator đang hiểu theo hai hướng khác nhau.
- **Các phương án đã cân nhắc:**
  1. *Gộp chung một box với xe* — vẽ nhanh hơn nhưng mất số lượng người trên xe, ảnh hưởng tiêu cực đến bài toán đếm lưu lượng giao thông. Loại.
  2. *Box riêng cho từng người* — tuân thủ câu chữ §3.2 và giữ toàn vẹn số người tham gia giao thông. **Chọn.**
- **Quyết định:** Mỗi người trên xe máy (người lái gán `rider`, người ngồi sau nếu không điều khiển gán theo phân loại guideline), kể cả người ngồi sau chỉ lộ đầu, có một box riêng. Box xe máy vẫn vẽ bao quát toàn bộ phương tiện như bình thường.
- **Việc phải làm theo:**
  - [x] Rà soát lại các frame có xe máy chở đôi ở Job 1447 và 1450 (Tống Thanh Danh)
  - [x] Thông báo và ghim quy tắc trong kênh trao đổi nội bộ của đội
- **Trạng thái:** Hiệu lực

## QĐ-002

**Reviewer trả nguyên job khi mẫu kiểm có trên 10% ảnh sai**

- **Ngày:** 16/09/2026
- **Người tham gia:** Lê Đức Mạnh (chốt), Võ Trọng Nghĩa, Vũ Việt Long
- **Xuất phát từ:** Quy trình đảm bảo chất lượng (QA) nội bộ
- **Bối cảnh:** Tránh tình trạng sửa lỗi rải rác từng ảnh khiến Reviewer làm thay công việc của Annotator, đồng thời nâng cao ý thức tự kiểm tra (Self-QC) của thành viên gán nhãn.
- **Các phương án đã cân nhắc:**
  1. *Sửa từng ảnh như cũ* — chấp nhận được với lỗi lẻ tẻ, nhưng nếu lỗi mang tính hệ thống (như sai nhãn hoặc lệch biên hàng loạt) thì reviewer tốn quá nhiều thời gian. Loại.
  2. *Kiểm ngẫu nhiên 20% ảnh, sai trên 10% thì trả nguyên job* — annotator tự rà soát lại toàn bộ job theo danh sách lỗi mẫu đã được chỉ ra. **Chọn.**
- **Quyết định:** Reviewer kiểm tra ngẫu nhiên 20% số ảnh trong mỗi job. Nếu phát hiện trên 10% số ảnh được kiểm mắc lỗi (vi phạm shape, nhãn hoặc thuộc tính) thì từ chối nghiệm thu, trả nguyên job kèm ghi chú lỗi để Annotator tự sửa toàn bộ trước khi nộp lại.
- **Việc phải làm theo:**
  - [x] Áp dụng bắt buộc cho mọi job do các thành viên nộp (Võ Trọng Nghĩa, Vũ Việt Long)
- **Trạng thái:** Hiệu lực

## QĐ-003

**Chuẩn hóa Pre-annotation bằng YOLO11m và logic tự động truncated/occluded**

- **Ngày:** 17/09/2026
- **Người tham gia:** @ManhLD424 (chốt), @thanh-vien-it2, @thanh-vien-it3
- **Xuất phát từ:** [P-003](problem-backlog.md#p-003) và [P-004](problem-backlog.md#p-004)
- **Bối cảnh:** Vẽ tay hàng trăm bounding box trên CVAT tốn quá nhiều thời gian và thường xuyên bỏ sót các biển báo nhỏ ở xa (§7 Completeness) hoặc quên bật thuộc tính `truncated`/`occluded` (§3.1).
- **Các phương án đã cân nhắc:**
  1. *Gán nhãn hoàn toàn thủ công bằng tay 100%* — quá tải cho thành viên, chất lượng giảm sút khi làm nhiều giờ liên tục. Loại.
  2. *Phát triển pipeline AI Pre-annotation tự động hóa bằng YOLO11m BDD100k ONNX kết hợp phân tích tọa độ* — mô hình phát hiện bao quát 10 class giao thông, thuật toán tự động tính toán tiếp xúc biên ảnh (`truncated`) và chồng lấn IoU (`occluded`), đẩy trực tiếp qua CVAT REST API, thành viên chuyển sang vai trò rà soát chất lượng. **Chọn.**
- **Quyết định:** Sử dụng công cụ `auto-annotator` trong `source-tool/` để sinh nhãn sơ bộ cho các job BBox dày đặc. Annotator và Reviewer rà soát 100% kết quả trước khi chốt job.
- **Việc phải làm theo:**
  - [x] Đã áp dụng thành công cho Job 1447 (sinh 333 annotations chất lượng cao) (@ManhLD424)
  - [ ] Đóng gói script dễ chạy cho toàn đội sử dụng từ tuần 2 (@ManhLD424)
- **Trạng thái:** Hiệu lực

## QĐ-004

**Chuẩn hóa RLE Mask, Zero Overlap và phân tầng Z-order cho Semantic Segmentation**

- **Ngày:** 17/09/2026
- **Người tham gia:** @ManhLD424 (chốt), @thanh-vien-it2, @thanh-vien-it3
- **Xuất phát từ:** [P-005](problem-backlog.md#p-005)
- **Bối cảnh:** Việc sử dụng đa giác (polygon) cho phân đoạn ngữ nghĩa 19 class Cityscapes gây phân mảnh hàng trăm mảnh nhỏ, răng cưa biên, và dễ tạo khe hở vi phạm Rule 01 (Zero Overlap).
- **Các phương án đã cân nhắc:**
  1. *Dùng đa giác Polygon thủ công* — khó ghép nối các vùng nền lớn (road, sidewalk, building, sky), biên mép bị răng cưa nặng. Loại.
  2. *Sử dụng định dạng Bitmask / RLE Mask bản địa của CVAT (`type: "mask"`)* kết hợp mô hình SegFormer B2 nội suy Bilinear Logits và YOLO11x-seg retina: gộp toàn bộ nền lớn thành 1 mask thống nhất (Z-order = 0), các đối tượng tiền cảnh tách thành từng ca thể độc lập (Z-order = 1). **Chọn.**
- **Quyết định:** Mọi tác vụ Semantic Segmentation phải tuân thủ chuẩn RLE Mask, phân tầng Z-order rõ ràng, đảm bảo tuyệt đối không có pixel nào bị chồng lấn giữa 2 class (Rule 01) và không suy đoán phần bị che khuất (Rule 02).
- **Việc phải làm theo:**
  - [x] Đã chạy nghiệm thu thành công 734 masks cho Job 1663 (@ManhLD424)
  - [x] Lưu trữ bộ ảnh overlay trực quan tại `vis_clean_masks_1663/` để phục vụ báo cáo Mentor
- **Trạng thái:** Hiệu lực

---

## Mẫu để copy

```markdown
## QĐ-NNN

**Quyết định trong một dòng**

- **Ngày:** dd/mm/yyyy
- **Người tham gia:** @ (chốt), @, @
- **Xuất phát từ:** [P-NNN](problem-backlog.md#p-nnn) | Họp tuần NN | …
- **Bối cảnh:** vì sao phải quyết định
- **Các phương án đã cân nhắc:**
  1. *Phương án* — ưu / nhược. Loại hoặc **Chọn.**
  2. *Phương án* — ưu / nhược. Loại hoặc **Chọn.**
- **Quyết định:** đủ rõ để người không dự họp vẫn làm đúng
- **Việc phải làm theo:**
  - [ ] việc (@người phụ trách)
- **Trạng thái:** Hiệu lực
```

Nhớ thêm một dòng vào bảng **Danh sách** ở đầu file, và đóng mục P-xxx tương ứng trong backlog.
