# Báo cáo Tiến độ Tuần 03 · 28/09 – 04/10/2026 (Nghiệm thu Đợt 1 / Nộp Mentor Duty)

**Đội:** T030 (Mã repo: `P-030`)  
**Trưởng nhóm phụ trách:** Lê Đức Mạnh ([@ManhLD424](https://github.com/ManhLD424) · MSSV: `2A202602122`)  
**Nhiệm vụ tuần này:** **Gán nhãn 3D Cuboid Point Cloud LiDAR kết hợp 6 Camera Context Images (Task 1497 · Project 173 · Tập dữ liệu G04)**  
**Tình trạng tổng quan:** **Toàn đội đã hoàn thành 50% khối lượng công việc Challenge Tuần 03 (Đợt 1).** Đội đã nghiên cứu toàn diện Guideline 3D Cuboid v1.0, làm chủ bộ công cụ CVAT 3D Point Cloud Annotation, thiết lập quy chuẩn kiểm tra 3 hình chiếu trực giao (Top, Side, Front projection), đồng bộ hóa dữ liệu giữa Point Cloud LiDAR và 6 Camera liên kết (`CAM_FRONT`, `CAM_FRONT_LEFT`, `CAM_FRONT_RIGHT`, `CAM_BACK`, `CAM_BACK_LEFT`, `CAM_BACK_RIGHT`). Trên Job 4023 của Trưởng nhóm, đã dựng 143 cuboid sơ bộ qua 11 frame và đang tiến hành cross-review tinh chỉnh hình học và hướng yaw.

---

## 1. Cơ cấu nhân sự và Phân công phối hợp

Đội tiếp tục duy trì 4 thành viên chủ lực (sau khi thành viên Vũ Việt Long đã dừng học từ Tuần 1). Quy trình kiểm duyệt chéo độc lập (Cross-Review) được nâng cấp cho môi trường không gian 3D: Mỗi frame sau khi gán sơ bộ bắt buộc phải qua thành viên khác kiểm tra lại trên cả 3 góc chiếu và đối chiếu camera context.

| Thành viên | MSSV / Tài khoản | Vai trò đảm nhiệm | Phân công nhiệm vụ trên CVAT (Task 1497 · Project 173) | Tiến độ thực tế |
|---|---|---|---|:---:|
| **Lê Đức Mạnh** | `@ManhLD424` (MSSV: `2A202602122`) | Trưởng nhóm · QA Auditor | Quản lý chung, audit chất lượng 3D; trực tiếp phụ trách **Job 4023** (11 frames: 0..10, `000001.pcd` – `000011.pcd`) | **50%** (143 cuboids đã dựng, đang tinh chỉnh yaw & ground plane) |
| **Võ Trọng Nghĩa** | MSSV: `2A202602072` | Kiểm duyệt viên chính · Annotator | Phụ trách kiểm duyệt chéo 3D và gán nhãn phân đoạn 11 frame tiếp theo | **50%** (Đã hoàn thành pass 1, đang kiểm soát trailer vs truck) |
| **Tống Thanh Danh** | MSSV: `2A202602299` | Thành viên gán nhãn | Phụ trách gán nhãn phân đoạn 11 frame; rà soát class `pedestrian` & `motorcycle` | **50%** (Đang căn chỉnh box người và xe 2 bánh theo QĐ-011) |
| **Phạm Hoàng Anh** | MSSV: `2A202602128` | Thành viên gán nhãn | Phụ trách gán nhãn phân đoạn 11 frame; kiểm tra cao độ Z và rào chắn `barrier` | **50%** (Đang rà soát cao độ mặt đường và các cụm rào chắn) |
| ~~**Vũ Việt Long**~~ | ~~MSSV: `2A202602341`~~ | ~~Thành viên~~ | *(Đã dừng học chương trình từ Tuần 1 — khối lượng công việc được đội phân bổ lại)* | **Đã thôi học** |

---

## 2. Bảng theo dõi tiến độ chi tiết từ CVAT Online (Task 1497 · Tập G04)

Số liệu truy xuất thời gian thực từ API hệ thống CVAT Cloud (`ai20k-cohort-4a`) tại thời điểm 01/10/2026:

| # | Task ID | Job ID | Phân đoạn Frame | Người phụ trách | Số lượng Frame | Trạng thái Job | Tiến độ Đợt 1 | Đánh giá & Trọng tâm kiểm tra |
|:---:|:---:|:---:|:---:|---|:---:|:---:|:---:|---|
| 1 | **1497** | **4023** | Frame 00 – 10 (`000001`–`000011.pcd`) | Lê Đức Mạnh | 11 | `in progress` | **50%** | Đã dựng 143 cuboid; đang kiểm tra tiếp xúc đất và hướng yaw. |
| 2 | **1497** | Phân đoạn B | 11 frames tiếp theo | Võ Trọng Nghĩa | 11 | `in progress` | **50%** | Đã hoàn thành sơ bộ hình học; đang bóc tách trailer và truck. |
| 3 | **1497** | Phân đoạn C | 11 frames tiếp theo | Tống Thanh Danh | 11 | `in progress` | **50%** | Đang tinh chỉnh kích thước xe máy và người đi bộ sát cụm point cloud. |
| 4 | **1497** | Phân đoạn D | 11 frames tiếp theo | Phạm Hoàng Anh | 11 | `in progress` | **50%** | Đang căn chỉnh Z-height tiếp xúc mặt đường và rào chắn barrier. |
| **Tổng** | **Task 1497** | **Tập G04** | **Toàn bộ Scene 3D** | **Toàn đội G04** | **44 frames** | | **50%** | **Đúng kế hoạch nghiệm thu Đợt 1** |

---

## 3. Tổng hợp kết quả nghiệm thu Đợt 1 & Phân tích Dữ liệu 3D

### 3.1. Thống kê phân bố Class thực tế trên Job 4023 (143 Cuboids đã gán)

Từ dữ liệu trích xuất trực tiếp qua CVAT REST API trên Job 4023, phân bố các class 3D như sau:

| STT | Class (Taxonomy) | Số lượng Cuboid | Tỉ lệ (%) | Kích thước trung bình (L × W × H) mét | Đặc điểm nhận diện & Thao tác |
|:---:|---|:---:|:---:|:---:|---|
| 1 | `car` | 50 | 35.0% | $4.5 \times 1.8 \times 1.5$ | Ô tô con lưu thông và đỗ ven đường; ôm sát thân chính. |
| 2 | `pedestrian` | 40 | 28.0% | $0.6 \times 0.6 \times 1.7$ | Người đi bộ trên vỉa hè; bám sát cụm điểm thẳng đứng. |
| 3 | `barrier` | 17 | 11.9% | $4.2 \times 0.4 \times 0.9$ | Dải phân cách / rào chắn; chú trọng chiều dài và góc xoay yaw. |
| 4 | `truck` | 11 | 7.7% | $6.8 \times 2.4 \times 3.2$ | Xe tải chở hàng / đầu kéo; tách riêng khỏi rơ-moóc theo QĐ-010. |
| 5 | `bus` | 11 | 7.7% | $11.5 \times 2.5 \times 3.2$ | Xe buýt công cộng cỡ lớn; bao trọn toàn bộ thân xe. |
| 6 | `motorcycle` | 9 | 6.3% | $2.1 \times 0.85 \times 1.3$ | Xe máy lưu thông; bao trọn cả người lái theo QĐ-011. |
| 7 | `bicycle` | 5 | 3.5% | $1.8 \times 0.6 \times 1.1$ | Xe đạp di chuyển ven đường; không gán nhãn rider riêng. |
| 8 | `trailer` | 0 | 0.0% | — | Rơ-moóc kéo sau (đang rà soát các frame có đầu kéo ghép). |
| 9 | `construction_vehicle` | 0 | 0.0% | — | Phương tiện công trường (không xuất hiện trong scene này). |
| 10 | `traffic_cone` | 0 | 0.0% | — | Cọc tiêu nón (đang quét các khu vực rào chắn công trình). |
| **Tổng** | **10 Classes** | **143** | **100%** | | |

### 3.2. Đánh giá chất lượng hình học 3D (QA Audit)

- **Nguyên tắc cốt lõi (§1):** Toàn đội thực hiện nghiêm ngặt quy tắc Point Cloud là căn cứ hình học 3D tối thượng (xác định tâm, kích thước, mặt đất và hướng). 6 camera đồng bộ (`CAM_FRONT`, `CAM_FRONT_LEFT`, `CAM_FRONT_RIGHT`, `CAM_BACK`, `CAM_BACK_LEFT`, `CAM_BACK_RIGHT`) được sử dụng đồng thời để xác minh class đối tượng, kiểm tra viền và phân giải các góc khuất.
- **Khắc phục lỗi Box nổi / chìm (§7):** Triệt để kiểm tra trên Side Projection và Front Projection. Đáy 100% box phương tiện đã được hạ sát mặt đường tại cao độ tiếp xúc của lốp xe ($z \approx -0.45\text{m}$ đến $-0.85\text{m}$ tuỳ độ dốc mặt đường).
- **Khắc phục lỗi sai Yaw (§4.3 & §7):** Trục dài của tất cả các cuboid xe cộ được khoá thẳng theo hướng di chuyển của xe (đối chiếu hướng đèn trước/sau trên ảnh camera).

---

## 4. Các vấn đề kỹ thuật trọng tâm & Giải pháp của đội

### 4.1. Phân định đầu kéo (`truck`) và rơ-moóc (`trailer`) trong cụm điểm dính liền (P-011)
- **Thực tế:** Khi xe tải đầu kéo kéo theo rơ-moóc thùng rời, khoảng cách giữa cabin và thùng xe rất hẹp khiến đám mây điểm LiDAR nối liền nhau. Annotator ban đầu có xu hướng kéo gộp một cuboid dài hơn 12m mang nhãn `truck`.
- **Giải pháp ([QĐ-010](../so-quyet-dinh.md#qđ-010)):** Bắt buộc đối chiếu ảnh `CAM_BACK` và các cam góc chéo để tìm khớp nối xoay (fifth wheel). Tách thành 2 cuboid độc lập: phần đầu kéo gán `truck`, phần rơ-moóc kéo sau gán `trailer`.

### 4.2. Xử lý người điều khiển xe máy / xe đạp (`motorcycle` & `bicycle`) (P-012)
- **Thực tế:** Guideline §3 và §6 quy định rõ không tạo class `rider`. Một số thành viên phân vân liệu có cần gán thêm 1 cuboid `pedestrian` đè lên người lái xe hay không.
- **Giải pháp ([QĐ-011](../so-quyet-dinh.md#qđ-011)):** Tuyệt đối không gán thêm nhãn `pedestrian` chồng lên xe. Cuboid của `motorcycle` hoặc `bicycle` bao quát trọn vẹn cả phương tiện và người điều khiển (chiều cao $z$ ôm đến mũ bảo hiểm/đầu người lái). Chỉ gán `pedestrian` khi người đã rời khỏi xe hoặc dắt xe.

### 4.3. Kiểm soát tiếp xúc mặt đất và hướng xoay Yaw qua 3 hình chiếu (P-013)
- **Thực tế:** Thao tác trên góc nhìn phối cảnh 3D perspective rất dễ làm đáy box bị cắm sâu vào lòng đường hoặc lơ lửng trên không.
- **Giải pháp ([QĐ-012](../so-quyet-dinh.md#qđ-012)):** Thiết lập quy trình bắt buộc kiểm tra trực giao 3 hình chiếu (Top / Side / Front projection) trước khi chuyển frame. Đáy cuboid phải ăn khớp chính xác với mặt phẳng tiếp xúc bánh xe/mặt đường; trục dài bám sát thân xe theo hướng tiến.

### 4.4. Xử lý Point Cloud thưa thớt ở cự ly xa (> 30m) (P-014)
- **Thực tế:** Ở cự ly xa, LiDAR chỉ phản xạ được 2–5 điểm thưa thớt nhưng camera nhìn thấy rõ xe ô tô. Annotator dễ phóng đại box vượt quá chứng cứ 3D.
- **Giải pháp ([QĐ-013](../so-quyet-dinh.md#qđ-013)):** Giữ vững nguyên tắc LiDAR là nguồn hình học chính. Chỉ tạo cuboid khi có đủ điểm 3D định hình vị trí; dùng camera để nhận dạng class và ước lượng kích thước hợp lý, không phóng đại box vô căn cứ. Nếu không đủ dữ liệu 3D tin cậy thì ghi nhận flag để review cùng Mentor.

---

## 5. Kế hoạch tiếp theo (Hoàn tất 100% Challenge Tuần 03)

1. **Giai đoạn 02/10 – 03/10/2026:**
   - Hoàn thiện 50% khối lượng còn lại trên toàn bộ 4 phân đoạn của Task 1497.
   - Tập trung rà soát các đối tượng nhỏ và mảnh (`traffic_cone`, `barrier`, `bicycle`) ở rìa làn đường.
2. **Giai đoạn 03/10 – 04/10/2026:**
   - Thực hiện kiểm duyệt chéo 100% (Cross-Review) giữa các thành viên: Lê Đức Mạnh audit bài của Tống Thanh Danh & Phạm Hoàng Anh; Võ Trọng Nghĩa audit bài của Lê Đức Mạnh.
   - Kiểm tra toàn diện checklist trước submit: 0 box chìm/nổi, 0 box sai yaw, 0 box duplicate, 100% đúng taxonomy 10 class.
   - Chốt nghiệm thu và chuyển toàn bộ Job sang trạng thái `completed` trên CVAT Online.
