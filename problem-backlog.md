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
| [P-006](#p-006) | Lệch taxonomy nhãn CVAT giữa BDD100k và YOLO format (`person`, `traffic_light`, `traffic_sign`) | Guideline mơ hồ | §2, Taxonomy | ✅ Đã chốt | [QĐ-005](so-quyet-dinh.md#qđ-005) & [polygon-cleaner](source-tool/polygon-cleaner/) |
| [P-007](#p-007) | Phân mảnh đa giác và 914 đa giác rác siêu nhỏ (< 10 px²) khi gán nhãn thủ công | Pain point công cụ | Rule 01, §2 | ✅ Đã chốt | [QĐ-006](so-quyet-dinh.md#qđ-006) & [polygon-cleaner](source-tool/polygon-cleaner/) |
| [P-008](#p-008) | Tranh chấp ranh giới Tường bờ kè (`wall`) vs Tòa nhà (`building`) vs Vỉa hè (`sidewalk`) | Guideline chưa nói tới | Rule 01, Rule 03 | ✅ Đã chốt | [QĐ-007](so-quyet-dinh.md#qđ-007) |

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
## P-006

**Lệch taxonomy nhãn CVAT giữa BDD100k và YOLO format (`person`, `traffic_light`, `traffic_sign`)**

- **Loại:** Guideline mơ hồ
- **Mục guideline:** §2 (Taxonomy nhãn đối tượng và quy ước định danh)
- **Người phát hiện:** Tống Thanh Danh (02299) & Người kiểm duyệt Võ Trọng Nghĩa (02072) · 17/09/2026
- **Link CVAT & Minh chứng:**
  - https://cvat.note.transformerlabs.ai/tasks/203/jobs/1663?frame=7 — Frame G04_S008 xuất hiện đồng thời người đi bộ, đèn tín hiệu và biển báo
  - Minh chứng hình ảnh: ![Minh chứng P-006](submissions/w1-segmentation-G04-Danh/docs_images/issue_p006_taxonomy_alias.jpg)
- **Mô tả:** Trong tập gán nhãn Semantic Segmentation G04, khi kiểm tra 25 frame của bạn Tống Thanh Danh, phát hiện:
  1. Có 21 đối tượng được gán Class 28 (`person`) thay vì Class 0 (`pedestrian`).
  2. Có 36 đối tượng được gán Class 29 (`traffic_light` có gạch dưới) thay vì Class 8 (`traffic light` có dấu cách).
  3. Có 34 đối tượng được gán Class 30 (`traffic_sign` có gạch dưới) thay vì Class 9 (`traffic sign` có dấu cách).
  - *Nguyên nhân:* Giao diện CVAT khi nạp cấu hình nhãn YOLO xuất hiện đồng thời cả bộ nhãn BDD100K chuẩn và nhãn YOLO alias. Thành viên mới cuộn xuống dưới và chọn các nhãn có gạch dưới hoặc nhãn `person`, dẫn đến lệch class ID hoàn toàn khi huấn luyện hoặc tính IoU/mAP.
- **Các cách hiểu:**
  1. Giữ nguyên theo nhãn mà CVAT cho phép chọn -> Gây lỗi không đồng nhất dữ liệu giữa các thành viên trong đội.
  2. Bắt buộc sửa tay từng đối tượng trên CVAT -> Rất mất thời gian (91 đối tượng).
  3. Sử dụng script tự động remap đồng bộ 100% về mã chuẩn (`28 -> 0`, `29 -> 8`, `30 -> 9`).
- **Xử lý tạm trong lúc chờ:** Ban hành quy chuẩn chọn nhãn nội bộ và áp dụng script remap.
- **Kết quả:** ✅ [QĐ-005](so-quyet-dinh.md#qđ-005) & Công cụ [`source-tool/polygon-cleaner/`](source-tool/polygon-cleaner/).

## P-007

**Phân mảnh đa giác và 914 đa giác rác siêu nhỏ (< 10 px²) khi gán nhãn thủ công**

- **Loại:** Pain point công cụ
- **Mục guideline:** Rule 01 (Zero Overlap), §2 (Danh mục phân đoạn)
- **Người phát hiện:** Tống Thanh Danh (02299) & QA Auditor Lê Đức Mạnh (02122) · 17/09/2026
- **Link CVAT & Minh chứng:**
  - https://cvat.note.transformerlabs.ai/tasks/203/jobs/1663?frame=0 — Frame G04_S001 có tới 221 đa giác thủ công
  - Minh chứng hình ảnh: ![Minh chứng P-007](submissions/w1-segmentation-G04-Danh/docs_images/issue_p007_tiny_polygons_fragmentation.jpg)
- **Mô tả:** Khi gán nhãn Semantic Segmentation bằng công cụ Polygon thủ công trên CVAT:
  1. Toàn bộ 25 frame của Danh có tới **914 / 2.916 đa giác (chiếm 31.3%)** có diện tích siêu nhỏ `< 10 px²`, trong đó có **58 đa giác suy biến (degenerate)** diện tích `< 1 px²`.
  2. Các lớp nền diện tích lớn như `vegetation` (630 đa giác) và `building` (586 đa giác) bị chia nhỏ thành hàng chục mảnh vụn rời rạc do tán cây, dây điện và cột đèn che cắt ngang.
  - Việc vẽ tay hàng trăm mảnh vụn này gây mỏi mắt, thao tác click đúp tạo ra nhiều điểm trượt (slivers) làm giảm độ chính xác và gây nặng nề khi nạp dữ liệu.
- **Hướng đang cân nhắc:**
  1. Viết script tự động tính diện tích pixel và lọc bỏ toàn bộ các đa giác rác `< 10 px²` và đa giác suy biến `< 1 px²`.
  2. Phổ biến cho annotator chuyển sang sử dụng cọ Brush (Mask RLE) hoặc công cụ AI `semantic-segmenter` đã được đội xây dựng.
- **Kết quả:** ✅ [QĐ-006](so-quyet-dinh.md#qđ-006) & Công cụ [`source-tool/polygon-cleaner/`](source-tool/polygon-cleaner/).

## P-008

**Tranh chấp ranh giới Tường bờ kè (`wall`) vs Tòa nhà (`building`) vs Vỉa hè (`sidewalk`)**

- **Loại:** Guideline chưa nói tới
- **Mục guideline:** Rule 01 (Zero Overlap), Rule 03 (Strict Boundary)
- **Người phát hiện:** Tống Thanh Danh (02299) & Người kiểm duyệt Võ Trọng Nghĩa (02072) · 17/09/2026
- **Link CVAT & Minh chứng:**
  - https://cvat.note.transformerlabs.ai/tasks/203/jobs/1663?frame=0 — Frame G04_S001 bờ kè đá giật cấp chân công trình bên phải
  - Minh chứng hình ảnh: ![Minh chứng P-008](submissions/w1-segmentation-G04-Danh/docs_images/issue_p008_wall_vs_building_boundary.jpg)
- **Mô tả:** Trong các khung cảnh đô thị miền núi hoặc đường dốc (như G04_S001, G04_S002, G04_S015), xuất hiện bờ kè đá lớn giật cấp để chống sạt lở nằm ngay dưới chân tường nhà dân sát mép đường. Annotator phân vân:
  1. Bờ kè đá gắn liền với kết cấu nhà nên gán là `building` hay tách riêng là `wall`?
  2. Dải đất/thảm cỏ hẹp bên trên bờ kè gán là `terrain` hay `vegetation`?
  3. Gờ đảo giao thông có vạch sơn đen trắng nổi cao giữa ngã ba gán `sidewalk` hay `road`?
- **Các cách hiểu:**
  1. Gộp toàn bộ bờ kè vào `building` vì nằm sát chân nhà dân.
  2. Tách bờ kè đá độc lập ngoài trời thành `wall`, kết cấu kín có tường gạch và mái nhà mới tính là `building`. Đảo giao thông bộ hành gán `sidewalk`.
- **Xử lý tạm trong lúc chờ:** Áp dụng theo hướng 2 theo thống nhất nội bộ.
- **Kết quả:** ✅ [QĐ-007](so-quyet-dinh.md#qđ-007).

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
