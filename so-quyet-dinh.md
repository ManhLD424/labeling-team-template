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
| [QĐ-005](#qđ-005) | Chuẩn hóa Taxonomy và tự động ánh xạ Alias Class (28->0, 29->8, 30->9) | 17/09/2026 | [P-006](problem-backlog.md#p-006) | Hiệu lực |
| [QĐ-006](#qđ-006) | Lọc bỏ tự động đa giác rác (< 10 px²) và khuyến nghị dùng cọ Brush Mask | 17/09/2026 | [P-007](problem-backlog.md#p-007) | Hiệu lực |
| [QĐ-007](#qđ-007) | Quy tắc phân định Tường rào (`wall`) vs Tòa nhà (`building`) và ranh giới Bờ kè đá | 17/09/2026 | [P-008](problem-backlog.md#p-008) | Hiệu lực |
| [QĐ-008](#qđ-008) | Ưu tiên bảo toàn chuỗi động học giải phẫu chi trên khi người lái vặn mình | 22/09/2026 | [P-009](problem-backlog.md#p-009) | Tạm áp dụng |
| [QĐ-009](#qđ-009) | Quy tắc xử lý chi dưới và khớp cổ chân bị che khuất trong cabin xe | 23/09/2026 | [P-010](problem-backlog.md#p-010) | Hiệu lực |
| [QĐ-010](#qđ-010) | Tách rời 2 cuboid riêng biệt cho `truck` và `trailer` kết hợp đối chiếu camera | 28/09/2026 | [P-011](problem-backlog.md#p-011) | Hiệu lực |
| [QĐ-011](#qđ-011) | Quy tắc gán trọn khối cho `motorcycle` và `bicycle` bao gồm cả người lái | 29/09/2026 | [P-012](problem-backlog.md#p-012) | Hiệu lực |
| [QĐ-012](#qđ-012) | Quy trình bắt buộc kiểm tra 3 hình chiếu (Top/Side/Front) để khoá mặt đất và Yaw | 29/09/2026 | [P-013](problem-backlog.md#p-013) | Hiệu lực |
| [QĐ-013](#qđ-013) | Nguyên tắc ưu tiên hình học LiDAR làm nguồn chính và đối soát camera context | 30/09/2026 | [P-014](problem-backlog.md#p-014) | Hiệu lực |

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
- **Người tham gia:** Lê Đức Mạnh (chốt), Võ Trọng Nghĩa, Vũ Việt Long
- **Xuất phát từ:** [P-003](problem-backlog.md#p-003) và [P-004](problem-backlog.md#p-004)
- **Bối cảnh:** Vẽ tay hàng trăm bounding box trên CVAT tốn quá nhiều thời gian và thường xuyên bỏ sót các biển báo nhỏ ở xa (§7 Completeness) hoặc quên bật thuộc tính `truncated`/`occluded` (§3.1).
- **Các phương án đã cân nhắc:**
  1. *Gán nhãn hoàn toàn thủ công bằng tay 100%* — quá tải cho thành viên, chất lượng giảm sút khi làm nhiều giờ liên tục. Loại.
  2. *Phát triển pipeline AI Pre-annotation tự động hóa bằng YOLO11m BDD100k ONNX kết hợp phân tích tọa độ* — mô hình phát hiện bao quát 10 class giao thông, thuật toán tự động tính toán tiếp xúc biên ảnh (`truncated`) và chồng lấn IoU (`occluded`), đẩy trực tiếp qua CVAT REST API, thành viên chuyển sang vai trò rà soát chất lượng. **Chọn.**
- **Quyết định:** Sử dụng công cụ `auto-annotator` trong `source-tool/` để sinh nhãn sơ bộ cho các job BBox dày đặc. Annotator và Reviewer rà soát 100% kết quả trước khi chốt job.
- **Việc phải làm theo:**
  - [x] Đã áp dụng thành công cho Job 1447 (sinh 333 annotations chất lượng cao) (Lê Đức Mạnh)
  - [ ] Đóng gói script dễ chạy cho toàn đội sử dụng từ tuần 2 (Lê Đức Mạnh)
- **Trạng thái:** Hiệu lực

## QĐ-004

**Chuẩn hóa RLE Mask, Zero Overlap và phân tầng Z-order cho Semantic Segmentation**

- **Ngày:** 17/09/2026
- **Người tham gia:** Lê Đức Mạnh (chốt), Võ Trọng Nghĩa, Vũ Việt Long
- **Xuất phát từ:** [P-005](problem-backlog.md#p-005)
- **Bối cảnh:** Việc sử dụng đa giác (polygon) cho phân đoạn ngữ nghĩa 19 class Cityscapes gây phân mảnh hàng trăm mảnh nhỏ, răng cưa biên, và dễ tạo khe hở vi phạm Rule 01 (Zero Overlap).
- **Các phương án đã cân nhắc:**
  1. *Dùng đa giác Polygon thủ công* — khó ghép nối các vùng nền lớn (road, sidewalk, building, sky), biên mép bị răng cưa nặng. Loại.
  2. *Sử dụng định dạng Bitmask / RLE Mask bản địa của CVAT (`type: "mask"`)* kết hợp mô hình SegFormer B2 nội suy Bilinear Logits và YOLO11x-seg retina: gộp toàn bộ nền lớn thành 1 mask thống nhất (Z-order = 0), các đối tượng tiền cảnh tách thành từng ca thể độc lập (Z-order = 1). **Chọn.**
- **Quyết định:** Mọi tác vụ Semantic Segmentation phải tuân thủ chuẩn RLE Mask, phân tầng Z-order rõ ràng, đảm bảo tuyệt đối không có pixel nào bị chồng lấn giữa 2 class (Rule 01) và không suy đoán phần bị che khuất (Rule 02).
- **Việc phải làm theo:**
  - [x] Đã chạy nghiệm thu thành công 734 masks cho Job 1663 (Lê Đức Mạnh)
  - [x] Lưu trữ bộ ảnh overlay trực quan tại `vis_clean_masks_1663/` để phục vụ báo cáo Mentor
- **Trạng thái:** Hiệu lực

## QĐ-005

**Chuẩn hóa Taxonomy và tự động ánh xạ Alias Class (28->0, 29->8, 30->9)**

- **Ngày:** 17/09/2026
- **Người tham gia:** Lê Đức Mạnh (chốt), Võ Trọng Nghĩa, Tống Thanh Danh, Vũ Việt Long
- **Xuất phát từ:** [P-006](problem-backlog.md#p-006)
- **Bối cảnh:** Danh sách cấu hình nhãn trên CVAT xuất hiện đồng thời cả bộ nhãn chuẩn BDD100K gốc (dấu cách) và bộ nhãn YOLO/COCO (gạch dưới). Bạn Tống Thanh Danh gán 91 đối tượng theo nhãn alias ở cuối danh sách (21x `person` - 28, 36x `traffic_light` - 29, 34x `traffic_sign` - 30), gây lệch định danh class khi huấn luyện hoặc tính IoU.
- **Các phương án đã cân nhắc:**
  1. *Yêu cầu thành viên sửa thủ công 91 đối tượng trên CVAT* — tốn kém thời gian và dễ sửa sót. Loại.
  2. *Viết tool tự động chuẩn hóa ID và ánh xạ alias (`clean_and_remap.py`)* — đồng nhất 100% dữ liệu tự động, loại bỏ rủi ro con người. **Chọn.**
- **Quyết định:** Toàn đội thống nhất quy chuẩn class ID gốc: `0: pedestrian`, `8: traffic light`, `9: traffic sign`. Triển khai script `source-tool/polygon-cleaner/clean_and_remap.py` để tự động hóa kiểm định và remap 100% tệp nhãn của các thành viên.
- **Việc phải làm theo:**
  - [x] Viết công cụ `clean_and_remap.py` trong `source-tool/polygon-cleaner/` (Lê Đức Mạnh)
  - [x] Phổ biến cho các thành viên quy tắc chọn nhãn đúng trên CVAT (Võ Trọng Nghĩa)
- **Trạng thái:** Hiệu lực

## QĐ-006

**Lọc bỏ tự động đa giác rác (< 10 px²) và khuyến nghị dùng cọ Brush Mask**

- **Ngày:** 17/09/2026
- **Người tham gia:** Lê Đức Mạnh (chốt), Võ Trọng Nghĩa, Vũ Việt Long, Tống Thanh Danh
- **Xuất phát từ:** [P-007](problem-backlog.md#p-007)
- **Bối cảnh:** Trong 2.916 đa giác gán tay của tập G04, có tới 914 đa giác (31.3%) diện tích `< 10 px²` và 58 đa giác suy biến `< 1 px²` do thao tác vẽ tay tỉ mỉ các tán cây (`vegetation`) và viền nhà (`building`). Các đa giác rác này làm giảm điểm mAP và tăng thời gian tải ảnh.
- **Các phương án đã cân nhắc:**
  1. *Giữ nguyên toàn bộ đa giác rác* — gây nhiễu dữ liệu và phạt điểm khi benchmark. Loại.
  2. *Lọc bỏ tự động bằng ngưỡng diện tích `min_area = 10.0 px²`* và khuyến nghị annotator dùng công cụ cọ Brush hoặc AI Segmentation. **Chọn.**
- **Quyết định:** Áp dụng ngưỡng lọc tự động: Loại bỏ mọi đa giác có diện tích `< 10 px²` hoặc `< 3` đỉnh. Hướng dẫn thành viên nhóm G04 chuyển sang dùng công cụ Brush trên CVAT để tô vùng nền lớn thay vì vẽ đa giác con.
- **Việc phải làm theo:**
  - [x] Tích hợp logic lọc diện tích vào `clean_and_remap.py` (Lê Đức Mạnh)
  - [x] Hướng dẫn bạn Danh thao tác với cọ Brush trên CVAT (Võ Trọng Nghĩa)
- **Trạng thái:** Hiệu lực

## QĐ-007

**Quy tắc phân định Tường rào (`wall`) vs Tòa nhà (`building`) và ranh giới Bờ kè đá**

- **Ngày:** 17/09/2026
- **Người tham gia:** Lê Đức Mạnh (chốt), Võ Trọng Nghĩa, Tống Thanh Danh, Phạm Hoàng Anh
- **Xuất phát từ:** [P-008](problem-backlog.md#p-008)
- **Bối cảnh:** Khung cảnh đường dốc đô thị (G04_S001) xuất hiện bờ kè đá lớn chống sạt lở giáp chân tường nhà dân sát mép vỉa hè. Annotator gặp khó khăn trong việc phân biệt đâu là `wall`, đâu là `building`, và gờ đảo bộ hành gán là gì.
- **Các phương án đã cân nhắc:**
  1. *Gộp toàn bộ bờ kè đá vào `building`* — sai bản chất cấu trúc hạ tầng giao thông. Loại.
  2. *Phân tách theo chức năng kết cấu không gian* — rõ ràng, trực quan, đúng chuẩn Cityscapes. **Chọn.**
- **Quyết định:**
  - *Tường (`wall` - Class 22)*: Bờ kè đá chống sạt lở độc lập ngoài trời, tường rào hoa sắt xây gạch bao quanh khu đất.
  - *Tòa nhà (`building` - Class 21)*: Kết cấu kín có mái che, tường nhà ở, cửa sổ, ban công.
  - *Vỉa hè (`sidewalk` - Class 20)*: Toàn bộ mặt hè dành cho người đi bộ, bao gồm cả gờ đảo bộ hành nổi cao viền sọc đen trắng.
  - *Địa hình (`terrain` - Class 26)*: Dải đất/cỏ tự nhiên dốc không có cây cao.
- **Việc phải làm theo:**
  - [x] Áp dụng chuẩn này cho 25 ảnh nhóm G04 (Tống Thanh Danh)
  - [x] Lưu trữ ảnh minh chứng `issue_p008_wall_vs_building_boundary.jpg` vào kho tài liệu đội (Võ Trọng Nghĩa)
- **Trạng thái:** Hiệu lực

## QĐ-008

**Ưu tiên bảo toàn chuỗi động học giải phẫu chi trên khi người lái vặn mình**

- **Ngày:** 22/09/2026
- **Người tham gia:** Lê Đức Mạnh (chốt), Võ Trọng Nghĩa, Tống Thanh Danh, Phạm Hoàng Anh
- **Xuất phát từ:** [P-009](problem-backlog.md#p-009)
- **Bối cảnh:** Khi người lái vặn mình hoặc đưa tay phải bắt chéo sang nửa trái khung hình, nếu máy móc áp dụng quy tắc R/L theo toạ độ màn hình sẽ làm gãy chuỗi động học cánh tay (vai phải nối khuỷu tay trái).
- **Các phương án đã cân nhắc:**
  1. *Đổi tên điểm hoàn toàn theo nửa trái/phải màn hình* — làm sai lệch nghiêm trọng topology xương cơ thể, khiến mô hình học ra dáng người bị dị tật. Loại.
  2. *Quy ước R/L ban đầu dựa trên vị trí khớp gốc (vai/hông), toàn bộ chuỗi chi (khuỷu, cổ tay) kế thừa theo khớp gốc đó* — bảo toàn tính liên tục của xương và tương thích mô hình Pose Estimation. **Chọn.**
- **Quyết định:** Luôn bảo toàn chuỗi xương liên tục: Cánh tay bắt đầu từ vai nào thì khuỷu tay và cổ tay đó mang nhãn của bên đó, bất kể bàn tay đó có vươn qua đường trung tuyến sang nửa bên kia của khung hình.
- **Việc phải làm theo:**
  - [x] Áp dụng cho các job HumanPose-17 (Võ Trọng Nghĩa, Tống Thanh Danh)
  - [x] Nộp câu hỏi xác nhận chính thức với Mentor trong buổi Mentor Duty ngày 24/09/2026 (Lê Đức Mạnh)
- **Trạng thái:** Tạm áp dụng

## QĐ-009

**Quy tắc xử lý chi dưới và khớp cổ chân bị che khuất trong cabin xe**

- **Ngày:** 23/09/2026
- **Người tham gia:** Lê Đức Mạnh (chốt), Võ Trọng Nghĩa, Tống Thanh Danh
- **Xuất phát từ:** [P-010](problem-backlog.md#p-010)
- **Bối cảnh:** Trong cabin xe ô tô, chi dưới người lái thường xuyên bị che khuất hoàn toàn sau bảng điều khiển, vô-lăng hoặc thành ghế. Mô hình gợi ý thường sinh lỗi trôi dạt điểm gối và cổ chân lên sàn xe hoặc cần số.
- **Các phương án đã cân nhắc:**
  1. *Cố ước lượng vị trí chân theo tỉ lệ giải phẫu dù không nhìn thấy chi* — sai số lên tới hơn 100px và làm loãng hàm loss hồi quy toạ độ của mô hình. Loại.
  2. *Tuân thủ nghiêm ngặt quy tắc Guideline §3.3 và §4.1: Chỉ gán `Occluded` khi thấy nếp quần định hình đường đùi/cẳng chân; nếu hoàn toàn không có dấu vết thị giác hoặc bị cắt khỏi khung hình thì dứt khoát đánh `Outside`* — chuẩn xác, trung thực, tránh ném điểm bừa bãi. **Chọn.**
- **Quyết định:** Tuyệt đối không đặt điểm gối/cổ chân lên ghế, cần số hay sàn xe. Chỉ đánh `Occluded` khi nhìn thấy đường đùi/cẳng chân qua quần để ước lượng theo trục chi; nếu chi dưới khuất hẳn sau táp-lô hoặc bị mép ảnh cắt thì đánh `Outside`.
- **Việc phải làm theo:**
  - [x] Áp dụng nghiệm thu cho 15 ảnh của Job 2559 & 2563 (Võ Trọng Nghĩa)
  - [ ] Rà soát 100% khi thực hiện các job còn lại của Task 430 & Task 431 (Lê Đức Mạnh, Tống Thanh Danh, Phạm Hoàng Anh)
- **Trạng thái:** Hiệu lực

## QĐ-010

**Tách rời 2 cuboid riêng biệt cho `truck` và `trailer` kết hợp đối chiếu camera (3D Cuboid)**

- **Ngày:** 28/09/2026
- **Người tham gia:** Lê Đức Mạnh (chốt), Võ Trọng Nghĩa, Tống Thanh Danh, Phạm Hoàng Anh
- **Xuất phát từ:** [P-011](problem-backlog.md#p-011)
- **Bối cảnh:** Trong đám mây điểm 3D, các xe tải đầu kéo chở rơ-moóc có phần nối liền mạch, dễ gây nhầm lẫn dẫn đến việc annotator kéo gộp một box duy nhất dài hơn 12m.
- **Các phương án đã cân nhắc:**
  1. *Gộp chung thành 1 box `truck`* — vi phạm guideline §3 và §6, làm sai lệch phân phối kích thước chuẩn của mô hình 3D Object Detection. Loại.
  2. *Tách rời 2 box độc lập: box `truck` cho đầu kéo và box `trailer` cho phần kéo sau* — tuân thủ taxonomy, mô tả chính xác từng thực thể vật lý. **Chọn.**
- **Quyết định:** Luôn tách thành 2 cuboid độc lập khi phát hiện xe đầu kéo có rơ-moóc thùng rời. Sử dụng kết hợp các camera góc rộng (`CAM_BACK`, `CAM_FRONT_LEFT`, `CAM_FRONT_RIGHT`) để xác định chính xác khe hở khớp nối (fifth wheel).
- **Việc phải làm theo:**
  - [x] Áp dụng kiểm duyệt chéo trên các Job của Task 1497 (Toàn đội)
- **Trạng thái:** Hiệu lực

## QĐ-011

**Quy tắc gán trọn khối cho `motorcycle` và `bicycle` bao gồm cả người lái (3D Cuboid)**

- **Ngày:** 29/09/2026
- **Người tham gia:** Lê Đức Mạnh (chốt), Võ Trọng Nghĩa, Tống Thanh Danh
- **Xuất phát từ:** [P-012](problem-backlog.md#p-012)
- **Bối cảnh:** Người điều khiển xe máy/xe đạp tạo thành một khối điểm cao gắn liền với phương tiện. Cần làm rõ quy tắc tránh việc gán thêm nhãn `pedestrian` chồng đè.
- **Các phương án đã cân nhắc:**
  1. *Tạo thêm 1 box `pedestrian` bao quanh người lái* — vi phạm nguyên tắc "Gán phương tiện, không tạo class rider riêng", gây duplicate và chồng lấn bounding box 3D vô nghĩa. Loại.
  2. *Chỉ tạo đúng 1 cuboid `motorcycle` hoặc `bicycle` bao trọn cả phương tiện và người điều khiển* — chuẩn xác theo Guideline §3 và §6. **Chọn.**
- **Quyết định:** Không bao giờ tạo box `pedestrian` đè lên xe khi người đang ngồi điều khiển xe máy hoặc xe đạp. Box của phương tiện phải có chiều cao $z$ ôm trọn đến đỉnh mũ bảo hiểm/đầu người lái. Chỉ gán `pedestrian` riêng biệt khi người đó đã bước xuống dắt xe hoặc tách rời khỏi phương tiện.
- **Việc phải làm theo:**
  - [x] Quán triệt toàn đội khi annotate các phương tiện 2 bánh (Tống Thanh Danh, Phạm Hoàng Anh)
- **Trạng thái:** Hiệu lực

## QĐ-012

**Quy trình bắt buộc kiểm tra 3 hình chiếu (Top/Side/Front) để khoá mặt đất và Yaw**

- **Ngày:** 29/09/2026
- **Người tham gia:** Lê Đức Mạnh (chốt), Võ Trọng Nghĩa, Phạm Hoàng Anh
- **Xuất phát từ:** [P-013](problem-backlog.md#p-013)
- **Bối cảnh:** Annotator chỉ nhìn góc nhìn 3D chính hoặc Top-down view nên thường bỏ qua độ cao $z$ và góc xoay yaw, dẫn đến lỗi box chìm dưới mặt đường hoặc xoay ngang thân xe.
- **Các phương án đã cân nhắc:**
  1. *Chỉ chỉnh nhanh trên phối cảnh 3D perspective* — thao tác nhanh nhưng tỉ lệ lỗi box nổi/chìm lên tới 40%. Loại.
  2. *Quy trình chuẩn hoá 3 bước trực giao: Khởi tạo trên Top-down -> Căn chỉnh độ cao và tiếp xúc đất trên Side/Front projection -> Khóa Yaw bám trục dài* — bảo đảm tính chính xác tuyệt đối của hình học 3D. **Chọn.**
- **Quyết định:** Bắt buộc 100% cuboid trước khi chuyển frame phải được kiểm tra qua cửa sổ trực giao Side Projection và Front Projection. Đáy cuboid phải tiếp xúc chính xác với mặt đường tại điểm bánh xe/chân đế; trục dài của box hướng thẳng theo hướng chuyển động của phương tiện.
- **Việc phải làm theo:**
  - [x] Áp dụng làm tiêu chí QA Audit số 1 trong biên bản nghiệm thu (Lê Đức Mạnh, Võ Trọng Nghĩa)
- **Trạng thái:** Hiệu lực

## QĐ-013

**Nguyên tắc ưu tiên hình học LiDAR làm nguồn chính và đối soát camera context**

- **Ngày:** 30/09/2026
- **Người tham gia:** Lê Đức Mạnh (chốt), Võ Trọng Nghĩa, Tống Thanh Danh, Phạm Hoàng Anh
- **Xuất phát từ:** [P-014](problem-backlog.md#p-014)
- **Bối cảnh:** Ở khoảng cách xa (> 30m), đám mây điểm thưa thớt khiến annotator dễ bị ảnh hưởng bởi ảnh 2D camera mà kéo box quá lớn hoặc đặt sai vị trí 3D.
- **Các phương án đã cân nhắc:**
  1. *Ước lượng box theo ảnh 2D camera bất kể điểm LiDAR* — sai lệch cự ly chiều sâu (depth) nghiêm trọng vì ảnh 2D thiếu thông tin chiều sâu $z$. Loại.
  2. *Point cloud là nguồn chính xác định hình học 3D; 6 camera dùng để xác nhận class, hướng và kiểm tra biên* — tuân thủ đúng nguyên tắc cốt lõi Guideline §1 và §4.4. **Chọn.**
- **Quyết định:** Point Cloud LiDAR là nguồn quyết định vị trí, kích thước và tâm box 3D; 6 camera đóng vai trò bổ trợ nhận dạng chủng loại (class) và hỗ trợ ước lượng. Tuyệt đối không tạo cuboid khi không có cơ sở điểm phản xạ 3D hợp lý trong Point Cloud. Các trường hợp điểm quá thưa không đủ căn cứ phải ghi lại để xin ý kiến Reviewer/Mentor.
- **Việc phải làm theo:**
  - [x] Áp dụng cho toàn bộ các frame có vùng điểm thưa trong Task 1497 (Toàn đội)
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
