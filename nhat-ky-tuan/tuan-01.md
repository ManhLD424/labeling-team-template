# Báo cáo Tiến độ Tuần 01 · 14/09 – 20/09/2026 (Nộp Mentor Duty)

**Đội:** T030 (Mã repo: `P-030`)  
**Trưởng nhóm phụ trách:** Lê Đức Mạnh ([@ManhLD424](https://github.com/ManhLD424) · MSSV: `2A202602122`)  
**Tình trạng tổng quan:** **Toàn đội đã hoàn thành 100% Challenge gán nhãn tuần này và vượt qua khâu kiểm duyệt chất lượng.**

---

## 1. Cơ cấu nhân sự và Phân công phối hợp

Đội phân định rõ ràng trách nhiệm giữa ba vai trò: **Người gán nhãn (Annotator)**, **Người kiểm duyệt chất lượng (Reviewer)** và **Trưởng nhóm (Lead & QA Auditor)**. Quy trình vận hành áp dụng cơ chế kiểm duyệt chéo độc lập (Cross-Review), cam kết nguyên tắc khách quan: **không thành viên nào tự nghiệm thu bài do chính mình gán**.

| Thành viên | MSSV / Tài khoản | Vai trò đảm nhiệm | Nhiệm vụ chính Tuần 1 | Tình trạng |
|---|---|---|---|:---:|
| **Lê Đức Mạnh** | `@ManhLD424` (MSSV: `02122`) | Trưởng nhóm · Kiểm toán chất lượng · Phát triển công cụ | Điều phối chung, quản lý Sổ quyết định, viết công cụ tự động hóa; Audit xác suất các job; phụ trách chính Job 1447 & 1663 | **Hoàn thành 100%** |
| **Võ Trọng Nghĩa** | MSSV: `02072` | Kiểm duyệt viên chính · Gán nhãn | Phụ trách kiểm duyệt chất lượng bài của Tống Thanh Danh và Phạm Hoàng Anh; phụ trách gán Job 1448 | **Hoàn thành 100%** |
| ~~**Vũ Việt Long**~~ | ~~MSSV: `02341`~~ | ~~Thành viên~~ | *(Đã dừng việc theo học chương trình)* | **Đã thôi học** |
| **Tống Thanh Danh** | MSSV: `02299` | Thành viên gán nhãn | Đảm nhận gán nhãn tập Phân đoạn ngữ nghĩa G04 và Job 1450 | **Hoàn thành 100%** |
| **Phạm Hoàng Anh** | MSSV: `02128` | Thành viên gán nhãn | Đảm nhận gán nhãn Job 1451 | **Hoàn thành 100%** |

---

## 2. Bảng theo dõi tiến độ chi tiết

| # | Hạng mục công việc | Người thực hiện | Người kiểm duyệt | Tiến độ | Đánh giá chất lượng & Kết quả đạt được |
|---|---|---|---|:---:|---|
| 1 | Nghiên cứu Annotation Guideline v1.0 (§2 Danh mục nhãn, §3 Quy tắc hình học, §7 Tính đầy đủ) | Toàn đội | Lê Đức Mạnh | **100%** | Đã thống nhất tiêu chuẩn nhận diện 10 lớp đối tượng, quy cách gán nhãn xe cộ và các cờ thuộc tính `truncated` / `occluded`. |
| 2 | Nghiên cứu Semantic Segmentation Guideline (19 lớp Cityscapes, Quy tắc 01/02/03) | Toàn đội | Lê Đức Mạnh | **100%** | Nắm vững quy tắc Không chồng lấn (Zero Overlap), Bám sát biên nhìn thấy và phân định ranh giới các lớp nền. |
| 3 | **Job 1447 (Task 149)** — Giao thông đô thị mật độ cao (BBox, Lane, Area) | Lê Đức Mạnh | Võ Trọng Nghĩa | **100%** | **Đã nghiệm thu:** Toàn bộ bounding box chuẩn xác, làm sạch các box trùng lặp và rác, sửa xe tải thùng F35, gắn đủ thuộc tính `occluded` và `truncated`. |
| 4 | **Job 1663 (Task 203)** — Semantic Segmentation 19 lớp Cityscapes | Lê Đức Mạnh | Võ Trọng Nghĩa | **100%** | **Đã nghiệm thu:** Xóa sạch toàn bộ masks cũ bị phân mảnh; tái phân đoạn từ đầu đạt chuẩn RLE native, kiểm toán trực tiếp đạt **chính xác 0 pixel chồng lấn**. |
| 5 | **Tập G04 (Segmentation)** — Phân đoạn ngữ nghĩa thực tế | Tống Thanh Danh | Võ Trọng Nghĩa | **100%** | **Đã nghiệm thu:** Hoàn thành đầy đủ các đa giác phân đoạn; làm sạch toàn bộ nhãn alias và loại bỏ đa giác rác; lưu trữ tại `submissions/w1-segmentation-G04-Danh/`. |
| 6 | **Job 1448 (Task 149)** — Đường phố đô thị (BBox & Lane) | Võ Trọng Nghĩa | Lê Đức Mạnh | **100%** | **Đã nghiệm thu:** Hoàn tất toàn bộ đối tượng, đạt chuẩn tính đầy đủ của biển báo và phương tiện nhỏ ở xa. |
| 7 | **Job 1450 (Task 149)** — Đường phố đô thị (BBox & Lane) | Tống Thanh Danh | Võ Trọng Nghĩa | **100%** | **Đã nghiệm thu:** Hoàn tất toàn bộ đối tượng, chuẩn hóa các trường hợp xe máy chở người theo QĐ-001. |
| 8 | **Job 1451 (Task 149)** — Đường phố đô thị (BBox & Lane) | Phạm Hoàng Anh | Võ Trọng Nghĩa | **100%** | **Đã nghiệm thu:** Tháo gỡ điểm nghẽn che khuất theo QĐ-001 & QĐ-003; kiểm duyệt hoàn thiện đạt chuẩn chất lượng. |
| 9 | Xây dựng bộ công cụ hỗ trợ gán nhãn [`source-tool/`](../source-tool/) | Lê Đức Mạnh | Toàn đội | **100%** | Đưa vào sử dụng thực tế 3 công cụ: `auto-annotator` (hỗ trợ BBox sơ bộ), `semantic-segmenter` (phân đoạn ngữ nghĩa), `polygon-cleaner` (chuẩn hóa nhãn). |

---

## 3. Tổng hợp kết quả nghiệm thu

- **Tình trạng Challenge Tuần 01:** **Toàn đội đã hoàn thành 100% Challenge gán nhãn tuần này.**
- **Tiến độ CVAT:** 100% các Job được giao trên hệ thống CVAT đều đã hoàn thành và vượt qua khâu kiểm duyệt chéo độc lập, chuyển trạng thái hoàn tất (`completed`).
- **Chất lượng dữ liệu (First-pass Yield):** Đạt mức cao và ổn định; mọi lỗi phát hiện trong quá trình kiểm duyệt chéo đều được trao đổi và khắc phục dứt điểm trước khi chốt nghiệm thu.
- **Tài liệu quản trị chất lượng:**
  - Ghi nhận đầy đủ **8 vấn đề kỹ thuật** phát sinh thực tế ([P-001](../problem-backlog.md#p-001) đến [P-008](../problem-backlog.md#p-008)).
  - Thống nhất và ban hành **7 quyết định chuẩn hóa** ([QĐ-001](../so-quyet-dinh.md#qđ-001) đến [QĐ-007](../so-quyet-dinh.md#qđ-007)) làm căn cứ thực hành nhất quán cho cả đội.

---

## 4. Các vấn đề kỹ thuật trọng tâm & Giải pháp của đội

### 4.1. Biến động nhân sự
- Thành viên Vũ Việt Long đã dừng việc theo học chương trình.

### 4.2. Xử lý triệt để lỗi phân đoạn ngữ nghĩa trên Job 1663 (P-005)
- *Thực tế phát sinh:* Thuật toán tự động ban đầu chạy trên các cảnh thời tiết phức tạp (đường tuyết, cầu vượt thép) bị lỗi phân mảnh, sinh ra nhiều xe tải ảo trên tuyết và nhận diện nhầm dầm thép cầu vượt thành xe bus. Đồng thời việc trích xuất đa giác polygon gây răng cưa biên và vi phạm vùng đè pixel.
- *Xử lý của đội:*
  - Xóa sạch toàn bộ dữ liệu lỗi trên CVAT.
  - Tách bạch hoàn toàn: Cần gạt nước (`wiper`) và nội thất cabin xe đưa vào vùng không gán (`unannotated`); dầm cầu thép quy chuẩn về `building` theo Cityscapes; mặt đường phủ tuyết đưa về đúng `road`.
  - Áp dụng ma trận định danh thực thể độc lập (`inst_map`) phân tầng theo chiều sâu $y_2$ và xuất định dạng Bitmask / RLE Mask bản địa của CVAT.
  - Kết quả kiểm toán trực tiếp: **0 pixel chồng lấn (100% tuân thủ Rule 01 Zero Overlap)**, hình thái mask mịn, bám sát biên thực tế.

### 4.3. Đề xuất Mentor giải đáp ca vật thể bị che khuất nặng ở hậu cảnh xa (P-002)
- *Thực tế phát sinh:* Tại một số frame, xe ô tô hoặc xe máy ở xa bị che khuất trên 50-70% diện tích (chỉ nhô ra phần đầu xe hoặc một bánh xe). Guideline §3.4 mới chỉ đề cập trường hợp bị cắt mép ảnh (truncated) mà chưa định lượng cụ thể ngưỡng che khuất (occlusion threshold) để xác định khi nào bắt buộc gán và khi nào được phép bỏ qua.
- *Quy tắc tạm thời của đội:* Đội đã chốt theo [QĐ-001](../so-quyet-dinh.md#qđ-001) & [QĐ-003](../so-quyet-dinh.md#qđ-003): Nếu mắt thường nhận diện được chắc chắn loại phương tiện thì vẫn vẽ box bao sát phần nhìn thấy được và bắt buộc bật thuộc tính `occluded = true`.
- *Mục tiêu Mentor Duty:* Xin ý kiến phản hồi và xác nhận chính thức từ Mentor / Lab Coach để toàn đội áp dụng thống nhất cho các tuần dữ liệu tiếp theo.

### 4.4. Chuẩn hóa danh mục nhãn (P-006) và Lọc đa giác rác (P-007)
- *Thực tế phát sinh:* Trong quá trình gán nhãn tập G04, thành viên Tống Thanh Danh chọn nhãn theo tên alias ở cuối danh sách CVAT (như `person` thay vì `pedestrian`, `traffic_light` thay vì `traffic light`) và thao tác click tay tạo ra nhiều mẩu đa giác rác nhỏ $< 10\text{ px}^2$.
- *Xử lý của đội:* Ban hành [QĐ-005](../so-quyet-dinh.md#qđ-005) và [QĐ-006](../so-quyet-dinh.md#qđ-006); phát triển công cụ `clean_and_remap.py` tự động remap 100% về mã nhãn gốc chuẩn và lọc bỏ đa giác rác; hướng dẫn thành viên chuyển đổi thói quen sang dùng cọ Brush Mask trên CVAT.

---

## 5. Kế hoạch chốt nộp Tuần 01 & Phương hướng Tuần 02

1. **Trước 12:00 trưa ngày mai (Hạn chốt nộp bài Tuần 01):**
   - Rà soát toàn diện lần cuối 100% các Job trên CVAT, bảo đảm không còn Issue nào ở trạng thái Open.
   - Nộp báo cáo tiến độ và trình bày kết quả hoàn thành Challenge cùng các giải pháp công cụ tự động hóa với Mentor.
2. **Kế hoạch cho Tuần 02:**
   - Ổn định cơ cấu làm việc của đội gồm 4 thành viên.
   - Áp dụng các giải đáp từ Mentor cho ca P-002 vào bộ quy tắc nội bộ của đội.
   - Chuyển giao các script tự động hóa trong `source-tool/` để các thành viên có thể tự chạy kiểm tra lỗi trước khi gửi kiểm duyệt, nâng cao năng suất và chất lượng dữ liệu.
