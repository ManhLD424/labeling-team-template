# Báo cáo Tiến độ Tuần 02 · 21/09 – 27/09/2026 (Nghiệm thu Challenge Tuần)

**Đội:** T030 (Mã repo: `P-030`)  
**Trưởng nhóm phụ trách:** Lê Đức Mạnh ([@ManhLD424](https://github.com/ManhLD424) · MSSV: `2A202602122`)  
**Nhiệm vụ tuần này:** **VinFast HumanPose-17 Body Keypoints Challenge (Task 430 & Task 431)**  
**Tình trạng tổng quan:** Đã hoàn thành **100% (60 / 60 ảnh)** trên toàn bộ 8 Job của Task 430 & Task 431 trên hệ thống CVAT Online. Đã xử lý triệt để 100% các điểm lỗi dồn tại toạ độ (0, 0), chuẩn hóa toàn bộ cờ che khuất (`occluded`) và ra ngoài (`outside`), đồng bộ hóa chuỗi động học xương người lái cabin xe. Toàn bộ các gói annotation định dạng chuẩn CVAT 1.1 (`.zip`) đã được trích xuất sẵn sàng cho nộp bài và đối soát.

---

## 1. Cơ cấu nhân sự và Phân công hoàn tất

Đội đã thực hiện nghiêm ngặt quy trình kiểm duyệt chéo (Cross-Review), cam kết tính khách quan độc lập. Trưởng nhóm trực tiếp tiếp quản và xử lý dứt điểm các Job của thành viên thôi học (Job 2560 & Job 2564), đồng thời hỗ trợ rà soát kỹ thuật trên các Job pre-label.

| Thành viên | MSSV / Tài khoản | Vai trò đảm nhiệm | Phân công nhiệm vụ trên CVAT (Task 430 & 431) | Tình trạng thực tế |
|---|---|---|---|:---:|
| **Lê Đức Mạnh** | `@ManhLD424` (MSSV: `2A202602122`) | Trưởng nhóm · QA Auditor | Quản lý chung, audit schema; tiếp nhận và hoàn tất Job 2560 (5 ảnh), Job 2564 (10 ảnh), rà soát Job 2558 & 2562 | **Hoàn thành 100%** (Đã nghiệm thu trên CVAT) |
| **Võ Trọng Nghĩa** | MSSV: `2A202602072` | Kiểm duyệt viên chính · Annotator | Gán Job 2559 (5 ảnh Pose B) & Job 2563 (10 ảnh Pose A); phụ trách review bài toàn đội | **Hoàn thành 100%** (15/15 ảnh, đã nghiệm thu) |
| **Tống Thanh Danh** | MSSV: `2A202602299` | Thành viên gán nhãn | Gán Job 2558 (5 ảnh Pose B) & Job 2562 (10 ảnh Pose A) | **Hoàn thành 100%** (15/15 ảnh, đã nghiệm thu) |
| **Phạm Hoàng Anh** | MSSV: `2A202602128` | Thành viên gán nhãn | Gán Job 2561 (5 ảnh Pose B) & Job 2565 (10 ảnh Pose A) | **Hoàn thành 100%** (15/15 ảnh, đã nghiệm thu) |
| ~~**Vũ Việt Long**~~ | ~~MSSV: `2A202602341`~~ | ~~Thành viên~~ | *(Đã dừng học chương trình từ Tuần 1 — bàn giao hoàn toàn cho Lê Đức Mạnh)* | **Đã thôi học** (Đã bù đắp xong) |

---

## 2. Bảng theo dõi tiến độ thực tế từ CVAT Online API (Task 430 & Task 431)

Số liệu kiểm toán thực tế và truy xuất trực tiếp từ API CVAT Cloud (`ai20k-cohort-4a`) sau khi nghiệm thu hoàn tất:

| # | Task ID | Tên Task & Nội dung | Job ID | Người thực hiện | Khối lượng | Skeletons | Keypoints | Điểm lỗi (0,0) | Trạng thái Job |
|---|---|---|:---:|---|:---:|:---:|:---:|:---:|:---:|
| 1 | **Task 430** | `W2-POSE-G4-T1` (Vẽ 17 keypoint từ đầu) | **2558** | Tống Thanh Danh | 5 ảnh (F0–4) | 5 | 85 | 0 | `completed` |
| 2 | **Task 430** | `W2-POSE-G4-T1` (Vẽ 17 keypoint từ đầu) | **2559** | Võ Trọng Nghĩa | 5 ảnh (F5–9) | 5 | 85 | 0 | `completed` |
| 3 | **Task 430** | `W2-POSE-G4-T1` (Vẽ 17 keypoint từ đầu) | **2560** | Lê Đức Mạnh *(nhận thay)* | 5 ảnh (F10–14) | 5 | 85 | 0 | `completed` |
| 4 | **Task 430** | `W2-POSE-G4-T1` (Vẽ 17 keypoint từ đầu) | **2561** | Phạm Hoàng Anh | 5 ảnh (F15–19) | 5 | 85 | 0 | `completed` |
| 5 | **Task 431** | `W2-POSEPRE-G4-T1` (Sửa 17 keypoint pre-label) | **2562** | Tống Thanh Danh | 10 ảnh (F0–9) | 10 | 170 | 0 | `completed` |
| 6 | **Task 431** | `W2-POSEPRE-G4-T1` (Sửa 17 keypoint pre-label) | **2563** | Võ Trọng Nghĩa | 10 ảnh (F10–19) | 10 | 170 | 0 (đã dọn) | `completed` |
| 7 | **Task 431** | `W2-POSEPRE-G4-T1` (Sửa 17 keypoint pre-label) | **2564** | Lê Đức Mạnh *(nhận thay)* | 10 ảnh (F20–29) | 10 | 170 | 0 | `completed` |
| 8 | **Task 431** | `W2-POSEPRE-G4-T1` (Sửa 17 keypoint pre-label) | **2565** | Phạm Hoàng Anh | 10 ảnh (F30–39) | 10 | 170 | 0 | `completed` |
| **Tổng** | | **Toàn bộ Challenge Tuần 02** | **8 Jobs** | **Toàn đội G04** | **60 ảnh** | **60** | **1,020** | **0** | **100% Hoàn thành** |

---

## 3. Tổng hợp kết quả nghiệm thu kỹ thuật

- **Tổng số ảnh toàn đội đã chốt nghiệm thu:** **60 / 60 ảnh** (Đạt **100%** khối lượng Challenge tuần).
- **Chỉ tiêu chất lượng (QA Audit):**
  - Đã quét sạch toàn bộ các điểm pre-label bị vứt ở toạ độ góc (0, 0): trên Job 2564 (10 điểm), Job 2562 (12 điểm) và Job 2560 (dựng mới 100% 5 skeleton, 85 điểm).
  - Khớp nối động học chi trên tuân thủ đúng định danh vai tương ứng khi tài xế vặn người qua đường trung tuyến ([QĐ-008](../so-quyet-dinh.md#qđ-008)).
  - Chi dưới (gối, cổ chân) sau vô-lăng và bảng táp-lô được gắn đúng vị trí suy luận giải phẫu học và bật cờ `occluded = 1`, triệt để không đặt điểm vào chân ga/thành ghế vô căn cứ ([QĐ-009](../so-quyet-dinh.md#qđ-009)).
  - Các điểm tai phía xa bị che khuất bởi hộp sọ được định vị đúng thái dương và gán cờ `outside = 1` hoặc `occluded = 1` thay vì thả trôi toạ độ.

---

## 4. Danh mục File Archive (.zip) cung cấp phục vụ nộp bài & đối soát

Các file nén định dạng chuẩn **CVAT for images 1.1** (bên trong chứa file `annotations.xml` chuẩn cấu trúc task/image/skeleton/points):

1. **Job 2560 (Task 430 - Frames 10 đến 14):**
   - File: `d:/Project/VinPrj/w2_export_zips/Job_2560_Task430_Frames10-14_VuVietLong_CVAT1.1.zip`
   - Nội dung: 5 skeletons, 85 points, dựng mới hoàn toàn cho phân đoạn của thành viên vắng mặt.
2. **Job 2564 (Task 431 - Frames 20 đến 29):**
   - File: `d:/Project/VinPrj/w2_export_zips/Job_2564_Task431_Frames20-29_VuVietLong_CVAT1.1.zip`
   - Nội dung: 10 skeletons, 170 points, hiệu chỉnh sạch 100% điểm (0,0) và chuẩn hóa cờ khuất.
3. **Job 2562 (Task 431 - Frames 00 đến 09):**
   - File: `d:/Project/VinPrj/w2_export_zips/Job_2562_Task431_Frames00-09_LeManh_CVAT1.1.zip`
   - Nội dung: 10 skeletons, 170 points, hiệu chỉnh 12 điểm dồn (0,0) và các mắt/tai bị khuất.
4. **Job 2558 (Task 430 - Frames 00 đến 04):**
   - File: `d:/Project/VinPrj/w2_export_zips/Job_2558_Task430_Frames00-04_LeManh_CVAT1.1.zip`
   - Nội dung: 5 skeletons, 85 points, nghiệm thu hoàn chỉnh.
