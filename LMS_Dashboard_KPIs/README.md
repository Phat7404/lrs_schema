# BỘ CHỈ SỐ ĐÁNH GIÁ (KPIs) CHO DASHBOARD HỆ THỐNG LMS
## Learning Analytics & Educational Measurement Framework

---

## 📋 GIỚI THIỆU

Tài liệu này trình bày bộ chỉ số đánh giá toàn diện cho dashboard hệ thống quản lý học tập (LMS) dành cho giáo dục phổ thông và đại học tại Việt Nam. Các chỉ số được xây dựng dựa trên:

- **Nghiên cứu quốc tế**: Các bài báo từ Scopus, Web of Science, Springer, Elsevier
- **Khung đánh giá giáo dục**: OECD, UNESCO, EU, World Bank
- **Mô hình phân tích**: Learning Analytics, Educational Data Mining, Teacher Evaluation

---

## 🎯 MỤC ĐÍCH VÀ PHẠM VI

### Mục tiêu Dashboard
Dashboard được thiết kế để đánh giá nghiệp vụ sư phạm và hiệu quả dạy – học ở các cấp độ:
- **Giảng viên / Giáo viên**: Năng lực sư phạm, hoạt động giảng dạy
- **Người học**: Học sinh, sinh viên
- **Môn học / Khóa học**: Hiệu quả thiết kế và triển khai
- **Nhà trường / Khoa**: Quản lý và chiến lược giáo dục

### Dữ liệu Thu thập
- Log truy cập hệ thống
- Hoạt động học tập (xem bài, nộp bài, làm quiz, thảo luận)
- Kết quả đánh giá (điểm số, completion, feedback)
- Thời lượng học tập, mức độ tương tác
- xAPI statements (nếu có tích hợp LRS)

---

## 📊 CẤU TRÚC BỘ CHỈ SỐ

Bộ chỉ số được tổ chức thành **4 nhóm chính**:

### [1️⃣ Chỉ số Đánh giá Giảng viên / Giáo viên](./01_Chi_So_Giang_Vien.md)
**15 chỉ số** đánh giá năng lực sư phạm và hoạt động giảng dạy trên LMS
- Hoạt động giảng dạy
- Thiết kế nội dung học liệu
- Tương tác với người học
- Đánh giá và phản hồi

### [2️⃣ Chỉ số Đánh giá Người học](./02_Chi_So_Nguoi_Hoc.md)
**18 chỉ số** đánh giá engagement, tiến độ, kết quả và hành vi học tập
- Mức độ tham gia (Engagement)
- Tiến độ học tập (Progress)
- Kết quả học tập (Achievement)
- Hành vi học tập (Learning Behavior)

### [3️⃣ Chỉ số Đánh giá Quá trình Dạy – Học](./03_Chi_So_Qua_Trinh_Day_Hoc.md)
**12 chỉ số** đánh giá thiết kế học phần, tương tác và đánh giá liên tục
- Thiết kế học phần
- Tương tác sư phạm
- Đánh giá và phản hồi liên tục
- Hiệu quả học tập

### [4️⃣ Chỉ số Đánh giá Môi trường LMS & Học tập Số](./04_Chi_So_Moi_Truong_LMS.md)
**10 chỉ số** đánh giá hạ tầng, sẵn sàng số và trải nghiệm người dùng
- Hạ tầng và khả năng truy cập
- Mức độ sẵn sàng số
- Trải nghiệm người dùng
- Hiệu suất hệ thống

---

## 📚 NGUỒN THAM KHẢO HỌC THUẬT

Toàn bộ chỉ số được xây dựng dựa trên hơn **60 nghiên cứu quốc tế** từ:

### Cơ sở dữ liệu học thuật
- **Scopus** - Elsevier
- **Web of Science** - Clarivate Analytics
- **SpringerLink** - Springer Nature
- **ScienceDirect** - Elsevier

### Tổ chức giáo dục quốc tế
- **OECD** - Organisation for Economic Co-operation and Development
- **UNESCO** - United Nations Educational, Scientific and Cultural Organization
- **European Commission** - EU Education & Training
- **World Bank** - Education Global Practice

### Danh sách đầy đủ
Xem file: **[Tài liệu Tham khảo](./05_Tai_Lieu_Tham_Khao.md)**

---

## 💡 HƯỚNG DẪN SỬ DỤNG

### Cho Nhà phát triển Dashboard
1. Đọc từng nhóm chỉ số để hiểu yêu cầu nghiệp vụ
2. Xác định dữ liệu cần thiết từ LMS/LRS
3. Thiết kế data model và ETL pipeline
4. Xây dựng visualization components
5. Implement alerts và notifications

### Cho Nhà nghiên cứu / Sinh viên
1. Sử dụng làm tài liệu tham khảo cho chương Learning Analytics
2. Trích dẫn các nguồn học thuật trong luận văn
3. Áp dụng framework cho nghiên cứu thực nghiệm
4. Tùy chỉnh KPIs theo bối cảnh cụ thể

### Cho Quản lý Giáo dục
1. Hiểu các chỉ số đánh giá chất lượng dạy học
2. Thiết lập mục tiêu cải tiến (benchmarks)
3. Theo dõi và đánh giá hiệu quả giảng dạy
4. Ra quyết định dựa trên dữ liệu

---

## 🔗 CẤU TRÚC THỨ MỤC

```
LMS_Dashboard_KPIs/
├── README.md                          # File này
├── 01_Chi_So_Giang_Vien.md           # 15 KPIs giảng viên
├── 02_Chi_So_Nguoi_Hoc.md            # 18 KPIs người học
├── 03_Chi_So_Qua_Trinh_Day_Hoc.md    # 12 KPIs quá trình dạy học
├── 04_Chi_So_Moi_Truong_LMS.md       # 10 KPIs môi trường LMS
├── 05_Tai_Lieu_Tham_Khao.md          # Danh sách tài liệu tham khảo
└── 06_Phu_Luc.md                      # Công thức chi tiết, ví dụ ứng dụng
```

---

## 📈 TỔNG QUAN CHỈ SỐ

| Nhóm chỉ số | Số lượng | Định lượng | Định tính |
|-------------|----------|------------|-----------|
| Giảng viên  | 15       | 12         | 3         |
| Người học   | 18       | 15         | 3         |
| Quá trình   | 12       | 9          | 3         |
| Môi trường  | 10       | 7          | 3         |
| **TỔNG**    | **55**   | **43**     | **12**    |

---

## 🎓 KHUNG LÝ THUYẾT

Bộ KPIs được xây dựng dựa trên các mô hình lý thuyết:

1. **TPACK Framework** (Mishra & Koehler, 2006) - Đánh giá năng lực công nghệ sư phạm
2. **Community of Inquiry (CoI)** (Garrison et al., 2000) - Đánh giá tương tác học tập
3. **Self-Regulated Learning (SRL)** (Zimmerman, 2002) - Đánh giá hành vi tự học
4. **Technology Acceptance Model (TAM)** (Davis, 1989) - Đánh giá chấp nhận công nghệ
5. **Learning Analytics Framework** (Siemens & Long, 2011) - Phân tích dữ liệu học tập

---

## ⚙️ ỨNG DỤNG THỰC TẾ

### Nền tảng LMS hỗ trợ
- ✅ **Moodle** (phổ biến nhất tại VN)
- ✅ **Canvas LMS**
- ✅ **Google Classroom** (với API integration)
- ✅ **Microsoft Teams for Education**
- ✅ **Custom LMS** (với xAPI/SCORM support)

### Công nghệ triển khai
- **Backend**: Python (pandas, scikit-learn), Node.js
- **Visualization**: PowerBI, Tableau, D3.js, Chart.js
- **Database**: PostgreSQL, MongoDB, InfluxDB
- **Real-time**: WebSocket, Apache Kafka

---

## 📧 LIÊN HỆ & ĐÓNG GÓP

Tài liệu này được xây dựng cho mục đích nghiên cứu và giáo dục.

**Phiên bản**: 1.0  
**Ngày cập nhật**: 16/01/2026  
**Tác giả**: Dashboard LMS Research Team

---

## 📖 BẮT ĐẦU

👉 **[Bắt đầu với Nhóm 1: Chỉ số Giảng viên](./01_Chi_So_Giang_Vien.md)**

---

*Tài liệu này tuân thủ các tiêu chuẩn học thuật quốc tế và có thể được sử dụng cho nghiên cứu, đào tạo và triển khai thực tế.*
