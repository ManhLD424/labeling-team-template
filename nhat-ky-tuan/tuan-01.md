# Nhật ký tuần 01 · 14/09 – 20/09/2026

**Đội:** T030 (Repo: `P-030`)  
**Lead tuần này:** Lê Đức Mạnh ([@ManhLD424](https://github.com/ManhLD424) · MSSV: `2A202602122`)  
**Dữ liệu / Task CVAT:**
- **Task 149 (BBox, Polyline, Polygon Drivable Area):** [Task 149 / Job 1447](https://cvat.note.transformerlabs.ai/tasks/149/jobs/1447) (25 frames đường phố)
- **Task 203 (Semantic Segmentation 19 Classes Cityscapes):** [Task 203 / Job 1663](https://cvat.note.transformerlabs.ai/tasks/203/jobs/1663) (25 frames phân đoạn ngữ nghĩa)

---

## 1. Thành viên và phân công (Buddy System)

Mô hình vận hành: **3 IT + 2 Phi IT** kết hợp cơ chế kèm cặp 1-1 và kiểm duyệt chéo (Cross-Review), cam kết **không ai tự review bài của chính mình**:

| Thành viên | MSSV / Handle | Vai trò chính | Phân công tuần 1 |
|---|---|---|---|
| Lê Đức Mạnh | `@ManhLD424` (MSSV: `02122`) | Lead · Quality Auditor · Tool Dev | Điều phối chung, giữ Sổ quyết định, code tool, Audit xác suất 20% mọi job, phụ trách Job 1447 & 1663 |
| Võ Trọng Nghĩa | MSSV: `02072` | Reviewer 1 · Buddy · Annotator | Buddy kèm cặp Tống Thanh Danh; Review 100% Job 1450; Gán Job 1448 (25 ảnh) |
| Vũ Việt Long | MSSV: `02341` | Reviewer 2 · Buddy · Annotator | Buddy kèm cặp Phạm Hoàng Anh; Review 100% Job 1451; Gán Job 1449 (25 ảnh) |
| Tống Thanh Danh | MSSV: `02299` | Annotator chuyên trách | Gán Job 1450 (25 ảnh BBox & Lane); phối hợp với Buddy Võ Trọng Nghĩa |
| Phạm Hoàng Anh | MSSV: `02128` | Annotator chuyên trách | Gán Job 1451 (25 ảnh BBox & Lane); phối hợp với Buddy Vũ Việt Long |

---

## 2. Tiến độ công việc chi tiết

| # | Nội dung công việc | Annotator | Reviewer | Hoàn thành | Ghi chú & Kết quả |
|---|---|---|---|---|---|
| 1 | Nghiên cứu Annotation Guideline v1.0 (§2 Taxonomy, §3 Rules, §7 Completeness) | Cả đội | Lê Đức Mạnh | ✅ 100% | Thống nhất quy chuẩn nhận diện 10 class BBox, thuộc tính `truncated`/`occluded` |
| 2 | Nghiên cứu Semantic Segmentation Guideline (19 class Cityscapes, Rule 01/02/03) | Cả đội | Lê Đức Mạnh | ✅ 100% | Nắm vững Zero Overlap, Strict Visibility và ranh giới các class nền |
| 3 | **Job 1447 (Task 149)** — 25 ảnh giao thông đô thị dày đặc | Lê Đức Mạnh | Võ Trọng Nghĩa | ✅ 100% | 333 annotations (BBox/Polyline/Polygon). Ứng dụng `auto-annotator` YOLO11m BDD100k, rà soát 100% |
| 4 | **Job 1663 (Task 203)** — 25 ảnh Semantic Segmentation | Lê Đức Mạnh | Vũ Việt Long | ✅ 100% | 734 clean masks RLE. Ứng dụng `semantic-segmenter` (SegFormer B2 + YOLO11x-seg), loại bỏ răng cưa |
| 5 | **Job 1448 (Task 149)** — 25 ảnh đường phố đô thị | Võ Trọng Nghĩa | Vũ Việt Long | 🟡 70% | Đang hoàn thiện các ca xe nhỏ và biển báo ở xa theo §7 Completeness |
| 6 | **Job 1449 (Task 149)** — 25 ảnh đường phố đô thị | Vũ Việt Long | Võ Trọng Nghĩa | 🟡 60% | Đang gán Polygon drivable area và Polyline phân làn |
| 7 | **Job 1450 (Task 149)** — 25 ảnh đường phố đô thị | Tống Thanh Danh | Võ Trọng Nghĩa | 🟡 50% | Đã gán 13/25 ảnh; Buddy Võ Trọng Nghĩa review chéo, trả 2 ảnh sửa theo QĐ-001 (người ngồi sau xe máy) |
| 8 | **Job 1451 (Task 149)** — 25 ảnh đường phố đô thị | Phạm Hoàng Anh | Vũ Việt Long | ⛔ 40% | Tạm dừng ở frame 10 do gặp nhiều xe bị che khuất > 50%, chờ hướng dẫn [P-002](../problem-backlog.md#p-002) |
| 9 | Xây dựng bộ công cụ tự động hóa [`source-tool/`](../source-tool/) | Lê Đức Mạnh | Cả đội | ✅ 100% | Hoàn thành `auto-annotator`, `semantic-segmenter`, `browser-copilot` |

*Quy ước:* ✅ Xong và đã qua review nghiệm thu · 🟡 Đang thực hiện · ⛔ Bị chặn (đang chờ giải quyết) · ⬜ Chưa bắt đầu

---

## 3. Tổng kết số liệu (Summary Metrics)

- **Tổng tiến độ gán nhãn:** Đã hoàn thành sơ bộ **80 / 125 ảnh (64%)** trên toàn bộ các task được phân công.
- **Tỉ lệ đạt chuẩn review lần đầu (First-pass Yield):** **89.5%** (Reviewer kiểm tra mẫu và trả lại 8 ảnh có lỗi nhỏ về mép box hoặc sót đèn tín hiệu ở xa; annotator đã tiếp thu và sửa đổi 100%).
- **Edge cases phát hiện:** 5 vấn đề ([P-001](../problem-backlog.md#p-001) đến [P-005](../problem-backlog.md#p-005)).
- **Quyết định đã chốt:** 4 quyết định ([QĐ-001](../so-quyet-dinh.md#qđ-001) đến [QĐ-004](../so-quyet-dinh.md#qđ-004)).

---

## 4. Vướng mắc & Rào cản (Blockers & Pain points)

1. **Vướng mắc về Guideline (P-002):** Trường hợp vật thể (xe ô tô/xe máy) bị che khuất trên 50% ở hậu cảnh xa. Guideline §3.4 chỉ nêu vật thể cắt ở mép ảnh (truncated) mà chưa định lượng cụ thể ngưỡng che khuất (occlusion threshold) để xác định khi nào thì bỏ qua và khi nào bắt buộc vẽ box.
   - *Tạm thời:* Đội đã chốt [QĐ-001](../so-quyet-dinh.md#qđ-001) & [QĐ-003](../so-quyet-dinh.md#qđ-003): Vẫn vẽ box ôm sát phần nhìn thấy nếu mắt thường nhận diện được loại phương tiện và bật `occluded = true`. Cần Coach/Mentor xác nhận để chuẩn hóa cho cả đợt.
2. **Pain point về công cụ & Tốc độ gán nhãn (P-004, P-005):** Thao tác vẽ tay từng bounding box và phân đoạn đa giác (polygon) cho hàng chục ảnh giao thông rất tốn thời gian (30-45 phút/ảnh), dễ gây mỏi mắt dẫn đến bỏ sót vật thể nhỏ ở xa (vi phạm Completeness §7).
   - *Giải pháp đội đã làm:* Đội đã chủ động xây dựng bộ công cụ AI Pre-annotation trên ONNX Runtime (`auto-annotator` cho BBox và `semantic-segmenter` cho 19-class Cityscapes) giúp tăng tốc độ gán nhãn lên 5-10 lần, chuyển vai trò từ gán thủ công sang kiểm duyệt chất lượng.

---

## 5. Kế hoạch tuần 02

1. Nhận giải đáp từ Mentor/Coach về ca P-002, hoàn thiện nốt 100% các frame bị chặn ở Job 1451.
2. Đẩy toàn bộ tiến độ các Job 1448, 1449, 1450, 1451 lên **✅ 100% qua review**.
3. Phổ biến quy trình chạy `auto-annotator` cho các thành viên IT trong đội để hỗ trợ các bạn Phi IT tăng tốc độ xử lý các đợt dữ liệu tiếp theo.
4. Nâng chỉ số First-pass Yield của đội lên trên **95%**.

