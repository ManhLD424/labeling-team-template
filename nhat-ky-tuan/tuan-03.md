# Báo cáo Tiến độ Tuần 03 · 28/09 – 04/10/2026 (Nghiệm thu Hoàn tất Challenge / Nộp Mentor Duty)

**Đội:** T030 (Mã repo: `P-030`)  
**Trưởng nhóm phụ trách:** Lê Đức Mạnh ([@ManhLD424](https://github.com/ManhLD424) · MSSV: `2A202602122`)  
**Nhiệm vụ tuần này:** **Gán nhãn 3D Cuboid Point Cloud LiDAR kết hợp 6 Camera Context Images (Task 1497 · Project 173 · Tập dữ liệu G04)**  
**Tình trạng tổng quan:** **Toàn đội đã hoàn thành 100% Challenge gán nhãn 3D Cuboid Tuần 03 trên Task 1497 (Tập G04) và vượt qua khâu kiểm duyệt chất lượng.** Tất cả các Job được giao trên hệ thống CVAT Online đều đã hoàn tất và chuyển sang trạng thái `completed`. Đội đã làm chủ trọn vẹn quy trình gán nhãn 3D không gian, bám sát bộ 6 camera đồng bộ (`CAM_FRONT`, `CAM_FRONT_LEFT`, `CAM_FRONT_RIGHT`, `CAM_BACK`, `CAM_BACK_LEFT`, `CAM_BACK_RIGHT`), liên kết chuỗi đối tượng theo thời gian (3D Temporal Tracking) và triệt tiêu toàn diện các lỗi box nổi/chìm hoặc sai góc xoay yaw qua quy chuẩn kiểm tra 3 hình chiếu trực giao.

---

## 1. Cơ cấu nhân sự và Phân công hoàn tất

Đội tiếp tục thực hiện nghiêm ngặt quy trình kiểm duyệt chéo độc lập (Cross-Review), cam kết tính khách quan: không thành viên nào tự nghiệm thu bài do chính mình gán. Đối với dữ liệu 3D Point Cloud, khâu review yêu cầu kiểm tra kỹ lưỡng trên cả 3 góc chiếu (Top, Side, Front) kết hợp đối soát góc nhìn tương ứng trên 6 camera context.

| Thành viên | MSSV / Tài khoản | Vai trò đảm nhiệm | Phân công nhiệm vụ trên CVAT (Task 1497 · Project 173) | Tình trạng thực tế |
|---|---|---|---|:---:|
| **Lê Đức Mạnh** | `@ManhLD424` (MSSV: `2A202602122`) | Trưởng nhóm · QA Auditor | Quản lý chung, audit chất lượng 3D; trực tiếp phụ trách **Job 4023** (11 frames: 0..10, `000001.pcd` – `000011.pcd`) | **Hoàn thành 100%** (`completed` trên CVAT) |
| **Võ Trọng Nghĩa** | MSSV: `2A202602072` | Kiểm duyệt viên chính · Annotator | Gán nhãn phân đoạn 11 frame tiếp theo; phụ trách kiểm duyệt chéo 3D toàn đội | **Hoàn thành 100%** (`completed` trên CVAT) |
| **Tống Thanh Danh** | MSSV: `2A202602299` | Thành viên gán nhãn | Gán nhãn phân đoạn 11 frame; phụ trách chuẩn hóa các class `pedestrian`, `motorcycle`, `bicycle` | **Hoàn thành 100%** (`completed` trên CVAT) |
| **Phạm Hoàng Anh** | MSSV: `2A202602128` | Thành viên gán nhãn | Gán nhãn phân đoạn 11 frame; phụ trách kiểm soát cao độ Z mặt đường và rào chắn `barrier` | **Hoàn thành 100%** (`completed` trên CVAT) |
| ~~**Vũ Việt Long**~~ | ~~MSSV: `2A202602341`~~ | ~~Thành viên~~ | *(Đã dừng học chương trình từ Tuần 1 — khối lượng công việc được đội chia đều gánh vác)* | **Đã thôi học** |

---

## 2. Bảng theo dõi tiến độ chi tiết từ CVAT Online (Task 1497 · Tập G04)

Số liệu kiểm toán thực tế và truy xuất trực tiếp từ hệ thống CVAT Cloud (`ai20k-cohort-4a`) tại thời điểm nghiệm thu hoàn tất ngày 04/10/2026:

| # | Task ID | Job ID | Phân đoạn Frame | Người phụ trách | Số lượng Frame | Đối tượng Tracked | Trạng thái Job | Đánh giá & Tình trạng nghiệm thu |
|:---:|:---:|:---:|:---:|---|:---:|:---:|:---:|---|
| 1 | **1497** | **4023** | Frame 00 – 10 (`000001`–`000011.pcd`) | Lê Đức Mạnh | 11 | 21 tracks (141 cuboids) | `completed` | **Đã nghiệm thu:** Đủ 11 frame, liên kết track mượt mà, đáy box tiếp xúc chuẩn mặt đất. |
| 2 | **1497** | Phân đoạn B | 11 frames tiếp theo | Võ Trọng Nghĩa | 11 | Đầy đủ trackings | `completed` | **Đã nghiệm thu:** Đã bóc tách trailer và truck chính xác, yaw chuẩn theo hướng chuyển động. |
| 3 | **1497** | Phân đoạn C | 11 frames tiếp theo | Tống Thanh Danh | 11 | Đầy đủ trackings | `completed` | **Đã nghiệm thu:** Chuẩn hóa toàn bộ người đi bộ và xe 2 bánh bao trọn người lái theo QĐ-011. |
| 4 | **1497** | Phân đoạn D | 11 frames tiếp theo | Phạm Hoàng Anh | 11 | Đầy đủ trackings | `completed` | **Đã nghiệm thu:** Cao độ Z tiếp xúc chuẩn mặt đường trên toàn bộ rào chắn và phương tiện. |
| **Tổng** | **Task 1497** | **Tập G04** | **Toàn bộ Scene 3D** | **Toàn đội G04** | **44 frames** | **100% Tracked** | `completed` | **Hoàn thành 100% Challenge Tuần 03** |

---

## 3. Tổng hợp kết quả nghiệm thu kỹ thuật & Phân tích Dữ liệu 3D

### 3.1. Thống kê theo dõi đối tượng (3D Object Tracking) trên Job 4023

Dữ liệu trên Job 4023 được lưu trữ dưới dạng chuỗi tracking liên tục theo thời gian, giúp bảo toàn ID thực thể xuyên suốt các frame point cloud liên tiếp:

- **Tổng số luồng đối tượng được theo dõi (Tracks):** **21 tracks**
- **Tổng số 3D Cuboids xuyên suốt 11 frame:** **141 cuboids**

Phân bố chi tiết theo từng Class (Taxonomy):

| STT | Class | Số lượng Tracks | Số lượng Cuboids | Tỉ lệ (%) | Kích thước trung bình (L × W × H) mét | Ghi chú kỹ thuật |
|:---:|---|:---:|:---:|:---:|:---:|---|
| 1 | `pedestrian` | 11 | 74 | 52.4% | $0.62 \times 0.60 \times 1.72$ | Người đi bộ theo nhóm và đơn lẻ trên vỉa hè; bám sát cụm điểm thẳng đứng. |
| 2 | `car` | 8 | 55 | 38.1% | $4.55 \times 1.82 \times 1.50$ | Ô tô con lưu thông và dừng đỗ; trục dài bám sát hướng tiến của xe. |
| 3 | `bus` | 1 | 11 | 4.8% | $11.50 \times 2.50 \times 3.20$ | Xe buýt công cộng cỡ lớn di chuyển dọc hành lang đường chính; tracking 11/11 frame. |
| 4 | `truck` | 1 | 1 | 4.8% | $6.80 \times 2.40 \times 3.20$ | Xe tải chở hàng xuất hiện ở frame đầu; tách rời khỏi rơ-moóc theo QĐ-010. |
| **Tổng** | **Job 4023** | **21 tracks** | **141 cuboids** | **100%** | | **Trạng thái: Completed** |

Phân bố cuboids theo từng khung hình:
- Frame 00 (`000001.pcd`): 11 cuboids
- Frame 01 (`000002.pcd`): 12 cuboids
- Frame 02 (`000003.pcd`): 13 cuboids
- Frame 03 (`000004.pcd`): 13 cuboids
- Frame 04 (`000005.pcd`): 20 cuboids (mật độ phương tiện và người đi bộ đông nhất)
- Frame 05 (`000006.pcd`): 18 cuboids
- Frame 06 (`000007.pcd`): 18 cuboids
- Frame 07 (`000008.pcd`): 10 cuboids
- Frame 08 (`000009.pcd`): 9 cuboids
- Frame 09 (`000010.pcd`): 4 cuboids (khu vực chuyển tiếp)
- Frame 10 (`000011.pcd`): 13 cuboids

### 3.2. Tiêu chuẩn chất lượng đạt được (QA Audit)

- **First-pass Yield:** Đạt **100%** trên toàn bộ các frame sau vòng kiểm duyệt chéo.
- **Khóa mặt đất (Ground Plane Alignment - [QĐ-012](../so-quyet-dinh.md#qđ-012)):** Triệt tiêu hoàn toàn lỗi box chìm dưới mặt đường hoặc lơ lửng trên không. 100% đáy box phương tiện và người đi bộ tiếp xúc chuẩn xác với mặt phẳng phản xạ mặt đường trên cả Side Projection và Front Projection ($z \approx -0.45\text{m}$ đến $-0.85\text{m}$).
- **Khóa góc xoay (Yaw Alignment):** Trục dài của tất cả các cuboid phương tiện được căn chỉnh chuẩn xác theo hướng chuyển động, đối chiếu với hướng đầu xe/đèn chiếu sáng trên 6 camera context, loại bỏ dứt điểm lỗi quay ngang box 90° hoặc ngược 180°.
- **Phân tách thực thể rõ ràng ([QĐ-010](../so-quyet-dinh.md#qđ-010)):** Tách rời dứt khoát xe đầu kéo (`truck`) và phần rơ-moóc (`trailer`), không để tồn tại box gộp quá khổ sai lệch kích thước chuẩn.
- **Tuân thủ Taxonomy ([QĐ-011](../so-quyet-dinh.md#qđ-011)):** Tuyệt đối không tạo class `rider` hoặc gán nhãn `pedestrian` chồng đè lên người đang điều khiển xe máy/xe đạp; bao trọn toàn bộ khối phương tiện và người lái.
- **Camera-LiDAR Fusion ([QĐ-013](../so-quyet-dinh.md#qđ-013)):** Ưu tiên dữ liệu hình học 3D của LiDAR làm căn cứ cốt lõi; sử dụng 6 camera làm cơ sở đối soát phân loại class và định hình biên, không vẽ box suy đoán khi không có phản xạ 3D hợp lý.

---

## 4. Các vấn đề kỹ thuật trọng tâm & Giải pháp của đội

### 4.1. Phân định đầu kéo (`truck`) và rơ-moóc (`trailer`) trong cụm điểm dính liền (P-011)
- **Thực tế:** Chùm điểm LiDAR giữa cabin xe đầu kéo và thùng rơ-moóc phía sau dính liền nhau do khoảng cách hẹp, dễ dẫn đến việc gán gộp 1 box dài > 12m mang nhãn `truck`.
- **Giải pháp ([QĐ-010](../so-quyet-dinh.md#qđ-010)):** Đối chiếu ảnh `CAM_BACK` và các cam góc chéo để xác định khớp nối xoay (fifth wheel). Tách thành 2 cuboid độc lập: phần đầu kéo gán `truck`, phần rơ-moóc kéo sau gán `trailer`.

### 4.2. Xử lý người điều khiển xe máy / xe đạp (`motorcycle` & `bicycle`) (P-012)
- **Thực tế:** Người lái xe nhô cao trên yên xe khiến annotator phân vân có cần tạo thêm 1 box `pedestrian` đè lên xe hay không.
- **Giải pháp ([QĐ-011](../so-quyet-dinh.md#qđ-011)):** Tuyệt đối không tạo box `pedestrian` chồng lên xe. Cuboid của `motorcycle` hoặc `bicycle` bao trọn cả phương tiện và người điều khiển (chiều cao $z$ ôm đến đỉnh mũ bảo hiểm). Chỉ gán `pedestrian` khi người đã rời khỏi xe hoặc dắt bộ.

### 4.3. Kiểm soát tiếp xúc mặt đất và hướng xoay Yaw qua 3 hình chiếu (P-013)
- **Thực tế:** Thao tác trên góc nhìn phối cảnh 3D perspective dễ làm đáy box bị cắm sâu vào lòng đường hoặc lơ lửng trên không.
- **Giải pháp ([QĐ-012](../so-quyet-dinh.md#qđ-012)):** Thiết lập quy trình bắt buộc kiểm tra trực giao 3 hình chiếu (Top / Side / Front projection) trước khi hoàn tất frame. Đáy cuboid phải tiếp xúc chính xác với mặt đường tại điểm bánh xe/mặt đất; trục dài bám sát thân xe theo hướng tiến.

### 4.4. Xử lý Point Cloud thưa thớt ở cự ly xa (> 30m) (P-014)
- **Thực tế:** Ở cự ly xa, LiDAR chỉ phản xạ 2–5 điểm thưa thớt trong khi camera nhìn thấy rõ xe ô tô. Annotator dễ phóng đại box vượt quá chứng cứ 3D.
- **Giải pháp ([QĐ-013](../so-quyet-dinh.md#qđ-013)):** Giữ vững nguyên tắc LiDAR là nguồn hình học chính. Chỉ tạo cuboid khi có đủ điểm 3D định hình vị trí; dùng camera để nhận dạng class và ước lượng kích thước hợp lý, không phóng đại box vô căn cứ.

---

## 5. Kế hoạch chốt nộp Tuần 03 & Phương hướng Tuần 04

1. **Chốt nộp Tuần 03:**
   - Toàn bộ 4 phân đoạn thuộc Task 1497 (Tập G04) đã chuyển trạng thái hoàn tất (`completed`) trên CVAT Online.
   - Nộp báo cáo tiến độ và trình bày kết quả nghiệm thu 100% cùng các quyết định kỹ thuật chuẩn hóa (QĐ-010 đến QĐ-013) với Mentor.
2. **Kế hoạch cho Tuần 04:**
   - Tiếp tục duy trì kỷ luật phối hợp 4 thành viên và văn hóa kiểm duyệt chéo khách quan.
   - Sẵn sàng tiếp nhận các dạng bài toán annotation nâng cao tiếp theo từ Ban tổ chức chương trình.
   - Đóng gói các kinh nghiệm thao tác trực giao 3D thành tài liệu hướng dẫn nội bộ của đội.
