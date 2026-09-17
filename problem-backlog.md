# Problem backlog

Những chỗ gặp trong lúc gán nhãn mà **guideline chưa trả lời được**, cộng các pain point về công cụ.

Ghi ngay khi gặp, kể cả lúc chưa biết xử lý thế nào. Một edge case không được ghi lại thì
mỗi người sẽ tự xử lý theo một kiểu — và đó là nguồn lớn nhất của nhãn không nhất quán.

> Các mục bên dưới là **ví dụ**, tên và link CVAT đều giả. Mẫu trống để copy nằm cuối file.

## Danh sách

| Mã | Tóm tắt | Loại | Mục guideline | Trạng thái | Kết quả |
|---|---|---|---|---|---|
| [P-001](#p-001) | Người ngồi sau xe máy: box riêng hay gộp với người lái | Guideline mơ hồ | §3.2 | ✅ Đã chốt | [QĐ-001](so-quyet-dinh.md#qđ-001) |
| [P-002](#p-002) | Xe bị che khuất hơn một nửa ở hậu cảnh xa | Guideline chưa nói tới | §3.4 | ↗️ Hỏi Coach/BTC | Tạm áp dụng [QĐ-003](so-quyet-dinh.md#qđ-003) |
| [P-003](#p-003) | Phải vẽ lại box y hệt qua nhiều frame liên tiếp | Pain point công cụ | — | ✅ Đã chốt | [QĐ-003](so-quyet-dinh.md#qđ-003) & [auto-annotator](source-tool/auto-annotator/) |
| [P-004](#p-004) | Vẽ tay hàng trăm BBox đường phố rất chậm và dễ sót biển/đèn ở xa | Pain point công cụ | §2, §3, §7 | ✅ Đã chốt | [QĐ-003](so-quyet-dinh.md#qđ-003) & [auto-annotator](source-tool/auto-annotator/) |
| [P-005](#p-005) | Phân đoạn ngữ nghĩa bị phân mảnh khi dùng đa giác và cần trích xuất RLE Mask | Pain point công cụ | §1, §2 | ✅ Đã chốt | [QĐ-004](so-quyet-dinh.md#qđ-004) & [semantic-segmenter](source-tool/semantic-segmenter/) |

**Loại**

| Loại | Nghĩa là |
|---|---|
| Guideline chưa nói tới | Tình huống không có trong guideline |
| Guideline mơ hồ | Đọc guideline ra được hai cách hiểu trở lên |
| Guideline mâu thuẫn | Hai mục trong guideline nói ngược nhau |
| Pain point công cụ | Guideline rõ, nhưng làm trên CVAT chậm hoặc dễ sai |

**Trạng thái:** 🔴 Mở · 🗣️ Đang bàn · ↗️ Hỏi BTC · ✅ Đã chốt (trỏ sang QĐ) · 🛠️ Làm tool (trỏ sang `source-tool/`) · ⚪ Bỏ (ghi lý do)

---

## P-001

**Người ngồi sau xe máy: box riêng hay gộp chung với người lái**

- **Loại:** Guideline mơ hồ
- **Mục guideline:** §3.2 — "mỗi người một bounding box"
- **Người phát hiện:** Tống Thanh Danh (02299) · 15/09/2026
- **Link CVAT:**
  - https://cvat.note.transformerlabs.ai/tasks/149/jobs/1447?frame=5 — hai người ngồi trên xe máy
  - https://cvat.note.transformerlabs.ai/tasks/149/jobs/1447?frame=12 — người ngồi sau chỉ lộ đầu và vai
- **Mô tả:** §3.2 nói mỗi người một box, nhưng hình minh hoạ trong guideline lại vẽ một box cho cả xe máy lẫn người trên xe.
- **Các cách hiểu:**
  1. Theo câu chữ: người ngồi sau có box `rider` hoặc `pedestrian` riêng.
  2. Theo hình minh hoạ: không vẽ box riêng cho ai đang ngồi trên xe, gộp chung xe.
- **Xử lý tạm trong lúc chờ:** vẽ box riêng cho từng người và gắn tag `can_xem_lai` để dễ lọc ra sửa.
- **Kết quả:** ✅ [QĐ-001](so-quyet-dinh.md#qđ-001)

## P-002

**Xe bị che khuất hơn một nửa ở hậu cảnh xa**

- **Loại:** Guideline chưa nói tới
- **Mục guideline:** §3.4 — chỉ nói về vật thể bị cắt ở mép ảnh (truncated), không nói về bị che khuất (occluded)
- **Người phát hiện:** Phạm Hoàng Anh (02128) · 16/09/2026
- **Link CVAT:**
  - https://cvat.note.transformerlabs.ai/tasks/149/jobs/1447?frame=14 — ô tô đỗ sau xe tải lớn, chỉ thò ra khoảng 30% phần đầu xe
  - https://cvat.note.transformerlabs.ai/tasks/149/jobs/1451?frame=10 — xe máy sau hàng rào/cột điện, lộ dưới 40%
- **Mô tả:** Không rõ có gán nhãn vật thể bị che khuất nặng không, và nếu có thì bounding box ôm phần nhìn thấy hay ước lượng cả phần bị che.
- **Các cách hiểu:**
  1. Bỏ qua khi lộ dưới 50% diện tích.
  2. Luôn gán nếu nhận diện được class, box chỉ ôm sát phần nhìn thấy và bật thuộc tính `occluded = true`.
  3. Luôn gán, box vẽ phỏng đoán ôm cả phần bị che khuất (Amodal BBox).
- **Xử lý tạm trong lúc chờ:** Tạm dừng các frame có tranh chấp ở Job 1451; chuyển các frame khác gán theo hướng 2 (ôm sát phần nhìn thấy, bật `occluded = true` theo [QĐ-003](so-quyet-dinh.md#qđ-003)).
- **Kết quả:** ↗️ Đã đưa vào câu hỏi nộp Mentor Duty ngày 17/09/2026 để xin giải đáp từ Lab Coach.

## P-003

**Phải vẽ lại box y hệt qua nhiều frame liên tiếp**

- **Loại:** Pain point công cụ
- **Mục guideline:** —
- **Người phát hiện:** Vũ Việt Long (02341) · 16/09/2026
- **Link CVAT:** https://cvat.note.transformerlabs.ai/tasks/149/jobs/1447?frame=0 — frame 0–10, xe ô tô đỗ ven đường đứng yên
- **Mô tả:** Ảnh chụp từ camera tĩnh hoặc xe dừng đèn đỏ, nhiều phương tiện đỗ bên đường xuất hiện y nguyên ở hàng loạt frame. Thao tác vẽ tay từng box lặp lại gây mất 40% tổng thời lượng.
- **Hướng đang cân nhắc:**
  1. Dùng chế độ Track sẵn có của CVAT (khi nạp sequence video).
  2. Sử dụng tool `auto-annotator` chạy suy luận hàng loạt và đẩy trực tiếp qua REST API.
- **Kết quả:** ✅ [QĐ-003](so-quyet-dinh.md#qđ-003) — Triển khai giải pháp 2 thông qua tool [`source-tool/auto-annotator/`](source-tool/auto-annotator/).

## P-004

**Vẽ tay hàng trăm BBox đường phố rất chậm và dễ sót biển/đèn ở xa**

- **Loại:** Pain point công cụ
- **Mục guideline:** §2 (Taxonomy 10 classes), §3.1 (Truncated & Occluded), §7 (Completeness)
- **Người phát hiện:** Lê Đức Mạnh (02122) · 17/09/2026
- **Link CVAT:** https://cvat.note.transformerlabs.ai/tasks/149/jobs/1447 — Job 1447 gồm 25 ảnh giao thông đô thị dày đặc
- **Mô tả:** Trong cảnh đường phố có mật độ phương tiện và biển báo cao, việc vẽ tay thủ công từng box cho hàng chục ảnh tốn hàng giờ đồng hồ, đồng thời rất dễ bỏ sót các đèn/biển giao thông nhỏ ở xa (vi phạm tiêu chí Completeness). Ngoài ra việc tích thủ công thuộc tính `truncated` và `occluded` dễ bị quên.
- **Hướng đang cân nhắc:**
  1. Viết tool tự động hoá gán nhãn sơ bộ (Pre-annotation) bằng mô hình YOLOv8 trên ONNX Runtime, tự động kết nối qua CVAT REST API để đẩy box và tự động gán `truncated` (chạm mép) và `occluded` (chồng lấn).
- **Kết quả:** Đã triển khai tool hoàn chỉnh tại [`source-tool/auto-annotator/`](source-tool/auto-annotator/).

## P-005

**Phân đoạn ngữ nghĩa bị phân mảnh khi dùng đa giác và cần trích xuất RLE Mask**

- **Loại:** Pain point công cụ
- **Mục guideline:** §1 (Phạm vi & nguyên tắc), §2 (Danh sách 19 class Cityscapes)
- **Người phát hiện:** Lê Đức Mạnh (02122) · 17/09/2026
- **Link CVAT:** https://cvat.note.transformerlabs.ai/tasks/203/jobs/1663 — Job 1663 Semantic Segmentation (25 frames)
- **Mô tả:** Trong tài liệu `Semantic_Segmentation_Annotation_Guideline.pdf`, quy định phân đoạn 19 class Cityscapes. Ban đầu khi gọi CVAT REST API mặc định trả về 10 nhãn do pagination (`page_size=10`). Khi truy vấn với `page_size=100`, Job 1663 thực tế có đầy đủ 31 nhãn (bao gồm toàn bộ các lớp nền `road`, `sidewalk`, `building`, `sky`, `vegetation`, `wall`, `fence`, `pole`, `terrain` và các đối tượng). Ngoài ra, việc dùng đa giác (polygon) cho phân đoạn ngữ nghĩa gây phân mảnh hàng trăm mảnh nhỏ và răng cưa.
- **Hướng đang cân nhắc:**
  1. Sử dụng định dạng Bitmask / RLE Mask bản địa của CVAT (`type: "mask"`).
  2. Xây dựng pipeline lai (Hybrid SegFormer B0 + YOLO11m BDD100k) với bộ nội suy Bilinear Logits để loại bỏ răng cưa và cứu các vùng xe bị lóa sáng/mờ kính.
  3. Gộp các lớp nền thành 1 mask thống nhất duy nhất cho mỗi lớp (Z-order = 0), các đối tượng tiền cảnh tách instance (Z-order = 1).
- **Kết quả:** Đã triển khai tool hoàn chỉnh tại [`source-tool/semantic-segmenter/`](source-tool/semantic-segmenter/) và upload thành công 882 clean masks lên Job 1663.

---

## Mẫu để copy

```markdown
## P-NNN

**Tóm tắt một dòng**

- **Loại:** Guideline chưa nói tới | Guideline mơ hồ | Guideline mâu thuẫn | Pain point công cụ
- **Mục guideline:** §
- **Người phát hiện:** @ · dd/mm/yyyy
- **Link CVAT:** (bỏ trống nếu không có)
  - https://…/tasks/<id>/jobs/<id>?frame=<n> — frame này có gì
- **Mô tả:**
- **Các cách hiểu:** (với pain point công cụ thì ghi **Hướng đang cân nhắc:**)
  1.
  2.
- **Xử lý tạm trong lúc chờ:**
- **Kết quả:** 🔴 Mở
```

Nhớ thêm một dòng vào bảng **Danh sách** ở đầu file.
