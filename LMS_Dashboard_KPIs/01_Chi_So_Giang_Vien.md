# 1️⃣ CHỈ SỐ ĐÁNH GIÁ GIẢNG VIÊN / GIÁO VIÊN

[← Quay lại README](./README.md)

---

## TỔNG QUAN

Nhóm chỉ số này đánh giá năng lực sư phạm và hoạt động giảng dạy của giảng viên/giáo viên trên LMS, bao gồm:
- Hoạt động giảng dạy tích cực
- Thiết kế nội dung học liệu số
- Tương tác với người học
- Đánh giá và phản hồi học tập

**Tổng số**: 15 chỉ số (12 định lượng + 3 định tính)

---

## A. HOẠT ĐỘNG GIẢNG DẠY TÍCH CỰC

### KPI 1.1: Tần suất Đăng nhập LMS của Giảng viên

**Mô tả nghiệp vụ**: Đo lường mức độ hiện diện và tích cực của giảng viên trên LMS thông qua số lần đăng nhập trong kỳ học.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Tần suất đăng nhập = Tổng số lần login / Số tuần trong kỳ học
  ```
- **Dữ liệu LMS**: 
  - Bảng `user_login_history`
  - Trường: `user_id`, `login_timestamp`, `session_duration`
- **Mục đích trên dashboard**:
  - Theo dõi sự hiện diện thường xuyên của GV
  - Cảnh báo sớm nếu GV không đăng nhập > 3 ngày
  - So sánh giữa các GV trong cùng khoa/bộ môn
- **Ngưỡng đánh giá**:
  - Xuất sắc: ≥ 5 lần/tuần
  - Tốt: 3-4 lần/tuần
  - Cần cải thiện: < 3 lần/tuần
- **Nguồn tham khảo**: 
  - Hrastinski, S. (2008). "Asynchronous and synchronous e-learning". *EDUCAUSE Quarterly*, 31(4), 51-55.
  - Link: https://er.educause.edu/articles/2008/11/asynchronous-and-synchronous-elearning

---

### KPI 1.2: Thời lượng Trực tuyến của Giảng viên

**Mô tả nghiệp vụ**: Thời gian giảng viên dành cho các hoạt động trên LMS, phản ánh mức độ đầu tư công sức vào giảng dạy trực tuyến.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Thời lượng trung bình = Tổng thời gian online (giờ) / Số tuần
  ```
- **Dữ liệu LMS**: 
  - `session_log` với `session_start`, `session_end`
  - Tính toán: `SUM(session_end - session_start) WHERE user_role = 'teacher'`
- **Mục đích trên dashboard**:
  - Đánh giá mức độ đầu tư thời gian
  - Phát hiện GV ít tham gia
  - Benchmark theo khoa/môn học
- **Ngưỡng đánh giá**:
  - Xuất sắc: ≥ 8 giờ/tuần
  - Tốt: 5-7 giờ/tuần
  - Cần cải thiện: < 5 giờ/tuần
- **Nguồn tham khảo**: 
  - Muilenburg, L. Y., & Berge, Z. L. (2005). "Student barriers to online learning". *Distance Education*, 26(1), 29-48.
  - DOI: https://doi.org/10.1080/01587910500081269

---

### KPI 1.3: Tỷ lệ Cập nhật Nội dung Học liệu

**Mô tả nghiệp vụ**: Đo lường tần suất cập nhật, bổ sung tài liệu, video, bài giảng để đảm bảo nội dung luôn mới và phù hợp.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Tỷ lệ cập nhật = (Số tài liệu được update trong tháng / Tổng số tài liệu) × 100%
  ```
- **Dữ liệu LMS**: 
  - Bảng `course_resources`
  - Trường: `resource_id`, `created_date`, `modified_date`, `version`
  - Điều kiện: `modified_date > created_date + 7 days`
- **Mục đích trên dashboard**:
  - Theo dõi việc cải tiến nội dung giảng dạy
  - Phát hiện nội dung "cũ" (không cập nhật > 6 tháng)
  - Khuyến khích GV cải tiến liên tục
- **Ngưỡng đánh giá**:
  - Tốt: ≥ 20% tài liệu được cập nhật/học kỳ
  - Trung bình: 10-20%
  - Cần cải thiện: < 10%
- **Nguồn tham khảo**: 
  - McGill, T. J., & Klobas, J. E. (2009). "A task–technology fit view of learning management system impact". *Computers & Education*, 52(2), 496-508.
  - DOI: https://doi.org/10.1016/j.compedu.2008.10.002

---

## B. THIẾT KẾ NỘI DUNG HỌC LIỆU SỐ

### KPI 1.4: Độ Đa dạng Định dạng Học liệu

**Mô tả nghiệp vụ**: Đánh giá mức độ phong phú của các loại tài liệu (PDF, video, interactive quiz, simulation) để đáp ứng đa dạng phong cách học tập.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Diversity Index = Số loại định dạng khác nhau sử dụng / Tổng số loại có thể (thường là 8-10)
  
  Ví dụ: {PDF, DOC, PPT, Video, Audio, SCORM, H5P, External Link} = 8 loại
  ```
- **Dữ liệu LMS**: 
  - `course_resources.resource_type`
  - Đếm `DISTINCT(resource_type)` theo `course_id` và `instructor_id`
- **Mục đích trên dashboard**:
  - Khuyến khích đa dạng hóa phương tiện
  - So sánh giữa các khóa học
  - Hỗ trợ Universal Design for Learning (UDL)
- **Ngưỡng đánh giá**:
  - Xuất sắc: ≥ 6 loại định dạng
  - Tốt: 4-5 loại
  - Cần cải thiện: ≤ 3 loại
- **Nguồn tham khảo**: 
  - Meyer, A., Rose, D. H., & Gordon, D. (2014). *Universal Design for Learning: Theory and Practice*. CAST Professional Publishing.
  - Link: http://udltheorypractice.cast.org/

---

### KPI 1.5: Chỉ số Độ Phủ Nội dung (Content Coverage Ratio)

**Mô tả nghiệp vụ**: Tỷ lệ giữa nội dung đã upload trên LMS so với kế hoạch giảng dạy (syllabus), đảm bảo đầy đủ kiến thức cho người học.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Coverage = (Số chủ đề đã có tài liệu / Tổng số chủ đề trong syllabus) × 100%
  ```
- **Dữ liệu LMS**: 
  - `course_syllabus.topics` (kế hoạch)
  - `course_resources.topic_tag` (thực tế)
  - Mapping giữa 2 bảng qua `topic_id`
- **Mục đích trên dashboard**:
  - Đảm bảo GV đã chuẩn bị đủ tài liệu
  - Cảnh báo nếu thiếu nội dung quan trọng
  - Theo dõi tiến độ upload trước kỳ học
- **Ngưỡng đánh giá**:
  - Đầy đủ: 100%
  - Tốt: ≥ 90%
  - Cần bổ sung: < 90%
- **Nguồn tham khảo**: 
  - Weller, M. (2007). *Virtual Learning Environments: Using, Choosing and Developing your VLE*. Routledge.
  - ISBN: 978-0415414302

---

## C. TƯƠNG TÁC VỚI NGƯỜI HỌC

### KPI 1.6: Thời gian Phản hồi Trung bình (Average Response Time)

**Mô tả nghiệp vụ**: Thời gian trung bình GV phản hồi câu hỏi, tin nhắn, bài nộp của sinh viên - yếu tố quan trọng tạo sự gắn kết.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Response Time = Trung bình(teacher_reply_time - student_post_time)
  
  Tính theo giờ hoặc ngày làm việc
  ```
- **Dữ liệu LMS**: 
  - `forum_posts`: `post_timestamp`, `parent_post_id`, `user_role`
  - `messages`: `sent_time`, `reply_time`, `sender_id`, `recipient_id`
  - `assignment_submissions`: `submitted_time`, `graded_time`
- **Mục đích trên dashboard**:
  - Theo dõi khả năng phản hồi kịp thời
  - Cảnh báo nếu > 48 giờ chưa phản hồi
  - Cải thiện trải nghiệm người học
- **Ngưỡng đánh giá**:
  - Xuất sắc: ≤ 24 giờ
  - Tốt: 24-48 giờ
  - Cần cải thiện: > 48 giờ
- **Nguồn tham khảo**: 
  - Hrastinski, S. (2009). "A theory of online learning as online participation". *Computers & Education*, 52(1), 78-82.
  - DOI: https://doi.org/10.1016/j.compedu.2008.06.009

---

### KPI 1.7: Tỷ lệ Đóng góp của GV trong Diễn đàn (Forum Contribution Rate)

**Mô tả nghiệp vụ**: Mức độ tham gia của GV trong các thảo luận trực tuyến để hướng dẫn, kích thích tư duy phản biện.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Contribution Rate = (Số bài post của GV / Tổng số bài post trong forum) × 100%
  
  Lý tưởng: 10-20% (không quá nhiều để SV tự thảo luận)
  ```
- **Dữ liệu LMS**: 
  - `forum_posts` với `author_id`, `author_role`
  - Đếm theo `course_id` và filter `role = 'teacher'`
- **Mục đích trên dashboard**:
  - Khuyến khích GV tham gia thảo luận
  - Cảnh báo nếu quá thụ động (< 5%) hoặc quá áp đảo (> 30%)
  - Đánh giá vai trò facilitator
- **Ngưỡng đánh giá**:
  - Cân bằng: 10-20%
  - Thụ động: < 10%
  - Quá chi phối: > 30%
- **Nguồn tham khảo**: 
  - Garrison, D. R., Anderson, T., & Archer, W. (2000). "Critical inquiry in a text-based environment: Computer conferencing in higher education". *The Internet and Higher Education*, 2(2-3), 87-105.
  - DOI: https://doi.org/10.1016/S1096-7516(00)00016-6

---

### KPI 1.8: Tỷ lệ Sử dụng Công cụ Giao tiếp Đồng bộ

**Mô tả nghiệp vụ**: Đo lường việc sử dụng các công cụ real-time (live chat, video conference) để tăng tương tác trực tiếp.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Usage Rate = (Số buổi live session / Tổng số tuần học) × 100%
  ```
- **Dữ liệu LMS**: 
  - `live_sessions`: `session_id`, `start_time`, `end_time`, `host_id`
  - `webinar_log`, `virtual_classroom_attendance`
  - Integration với Zoom/Teams qua API
- **Mục đích trên dashboard**:
  - Đánh giá blended learning approach
  - Khuyến khích tương tác real-time
  - Theo dõi xu hướng dạy học
- **Ngưỡng đánh giá**:
  - Blended learning: ≥ 50% tuần có live session
  - Moderately online: 25-50%
  - Fully asynchronous: < 25%
- **Nguồn tham khảo**: 
  - Bernard, R. M., et al. (2014). "A meta-analysis of blended learning and technology use in higher education". *Journal of Computing in Higher Education*, 26(1), 87-122.
  - DOI: https://doi.org/10.1007/s12528-013-9077-3

---

## D. ĐÁNH GIÁ VÀ PHẢN HỒI

### KPI 1.9: Tỷ lệ Chấm bài Đúng hạn

**Mô tả nghiệp vụ**: Phần trăm bài tập/bài kiểm tra được chấm trong khung thời gian cam kết với sinh viên.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  On-time Rate = (Số bài chấm đúng hạn / Tổng số bài nộp) × 100%
  
  Đúng hạn: graded_time ≤ submission_time + expected_grading_days
  ```
- **Dữ liệu LMS**: 
  - `assignment_submissions`: `submission_id`, `submitted_time`, `graded_time`
  - `assignment_settings`: `grading_deadline_days` (ví dụ: 7 ngày)
- **Mục đích trên dashboard**:
  - Theo dõi trách nhiệm chấm bài
  - Cảnh báo bài quá hạn chưa chấm
  - Cải thiện feedback loop
- **Ngưỡng đánh giá**:
  - Xuất sắc: ≥ 90%
  - Tốt: 75-89%
  - Cần cải thiện: < 75%
- **Nguồn tham khảo**: 
  - Nicol, D. J., & Macfarlane‐Dick, D. (2006). "Formative assessment and self‐regulated learning". *Studies in Higher Education*, 31(2), 199-218.
  - DOI: https://doi.org/10.1080/03075070600572090

---

### KPI 1.10: Chỉ số Chất lượng Phản hồi (Feedback Quality Score)

**Mô tả nghiệp vụ**: Đánh giá mức độ chi tiết, hữu ích của phản hồi GV dành cho từng bài làm sinh viên.

- **Loại chỉ số**: Định tính (có thể số hóa)
- **Công thức tính**: 
  ```
  Quality Score = Trung bình[(Độ dài phản hồi × 0.3) + 
                             (Có rubric chi tiết × 0.3) + 
                             (Có gợi ý cải tiến × 0.4)]
  
  Thang điểm: 1-5
  ```
- **Dữ liệu LMS**: 
  - `assignment_feedback`: `feedback_text`, `rubric_used`, `word_count`
  - NLP analysis: Sentiment, constructiveness
  - Survey sinh viên về chất lượng feedback
- **Mục đích trên dashboard**:
  - Khuyến khích feedback có giá trị
  - Phát hiện feedback "qua loa" (chỉ điểm số)
  - Training GV về assessment literacy
- **Ngưỡng đánh giá**:
  - Xuất sắc: ≥ 4.0/5.0
  - Tốt: 3.0-3.9/5.0
  - Cần cải thiện: < 3.0/5.0
- **Nguồn tham khảo**: 
  - Hattie, J., & Timperley, H. (2007). "The power of feedback". *Review of Educational Research*, 77(1), 81-112.
  - DOI: https://doi.org/10.3102/003465430298487

---

### KPI 1.11: Tần suất Đánh giá Hình thành (Formative Assessment Frequency)

**Mô tả nghiệp vụ**: Số lượng bài kiểm tra/quiz ngắn không tính điểm chính thức, giúp sinh viên tự đánh giá tiến độ.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Formative Frequency = Số quiz/poll/mini-test / Số tuần học
  ```
- **Dữ liệu LMS**: 
  - `quizzes` với `quiz_type = 'formative'` hoặc `weight = 0`
  - `polls`, `self_check_questions`
  - xAPI: `attempted` các ungraded activities
- **Mục đích trên dashboard**:
  - Khuyến khích assessment for learning
  - So sánh với summative assessment
  - Theo dõi continuous feedback
- **Ngưỡng đánh giá**:
  - Xuất sắc: ≥ 1 formative/tuần
  - Tốt: 1 formative/2 tuần
  - Cần bổ sung: < 1 formative/tháng
- **Nguồn tham khảo**: 
  - Black, P., & Wiliam, D. (2009). "Developing the theory of formative assessment". *Educational Assessment, Evaluation and Accountability*, 21(1), 5-31.
  - DOI: https://doi.org/10.1007/s11092-008-9068-5

---

## E. NĂNG LỰC CÔNG NGHỆ SƯ PHẠM

### KPI 1.12: Mức độ Sử dụng Công cụ LMS Nâng cao

**Mô tả nghiệp vụ**: Đánh giá việc khai thác các tính năng nâng cao của LMS (H5P, adaptive quiz, peer assessment, portfolio).

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Advanced Tool Usage = (Số công cụ nâng cao được sử dụng / Tổng số công cụ available) × 100%
  
  Công cụ nâng cao: Interactive content, Adaptive learning path, Peer review, 
                     Gamification, Analytics dashboard, API integration, etc.
  ```
- **Dữ liệu LMS**: 
  - `activity_modules` với `module_type`
  - Feature usage log: H5P activities, Workshop module, Badges, etc.
- **Mục đích trên dashboard**:
  - Đánh giá TPACK (Technology Pedagogy Content Knowledge)
  - Phát hiện nhu cầu đào tạo
  - Khuyến khích innovation
- **Ngưỡng đánh giá**:
  - Innovator: ≥ 50% công cụ nâng cao
  - Early Adopter: 30-49%
  - Basic User: < 30%
- **Nguồn tham khảo**: 
  - Koehler, M. J., & Mishra, P. (2009). "What is technological pedagogical content knowledge?". *Contemporary Issues in Technology and Teacher Education*, 9(1), 60-70.
  - Link: https://www.learntechlib.org/p/29544/

---

### KPI 1.13: Điểm Đánh giá của Sinh viên về Giảng dạy Trực tuyến

**Mô tả nghiệp vụ**: Kết quả khảo sát ý kiến sinh viên về năng lực giảng dạy của GV trên môi trường LMS.

- **Loại chỉ số**: Định tính (số hóa từ survey)
- **Công thức tính**: 
  ```
  Teacher Rating = Trung bình điểm từ student evaluation survey
  
  Các tiêu chí: Clarity, Responsiveness, Engagement, Fairness, Technical skill
  Thang điểm: 1-5 hoặc 1-10
  ```
- **Dữ liệu LMS**: 
  - `course_evaluation_responses`
  - `end_of_semester_survey`
  - Items: "Giảng viên phản hồi kịp thời", "Tài liệu rõ ràng", "Sử dụng công nghệ hiệu quả"
- **Mục đích trên dashboard**:
  - Đánh giá từ góc nhìn người học
  - Phản hồi để cải tiến giảng dạy
  - Ghi nhận GV xuất sắc
- **Ngưỡng đánh giá**:
  - Xuất sắc: ≥ 4.5/5.0
  - Tốt: 3.5-4.4/5.0
  - Cần cải thiện: < 3.5/5.0
- **Nguồn tham khảo**: 
  - Spooren, P., et al. (2013). "The validity of student evaluation of teaching in higher education". *Review of Educational Research*, 83(4), 598-642.
  - DOI: https://doi.org/10.3102/0034654313496870

---

## F. PHÁT TRIỂN CHUYÊN MÔN

### KPI 1.14: Số giờ Đào tạo Công nghệ Giáo dục

**Mô tả nghiệp vụ**: Thời gian GV tham gia các khóa học, workshop về EdTech, Learning Analytics, Online Pedagogy.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Training Hours = Tổng số giờ PD (Professional Development) về EdTech / năm học
  ```
- **Dữ liệu LMS**: 
  - `professional_development_log`
  - Certificate tracking system
  - External integration: Coursera, edX completion data
- **Mục đích trên dashboard**:
  - Theo dõi cam kết học tập liên tục của GV
  - Liên kết với chính sách đào tạo
  - Dự đoán năng lực công nghệ
- **Ngưỡng đánh giá**:
  - Xuất sắc: ≥ 20 giờ/năm
  - Tốt: 10-19 giờ/năm
  - Cần khuyến khích: < 10 giờ/năm
- **Nguồn tham khảo**: 
  - Lawless, K. A., & Pellegrino, J. W. (2007). "Professional development in integrating technology into teaching and learning". *Review of Educational Research*, 77(4), 575-614.
  - DOI: https://doi.org/10.3102/0034654307309921

---

### KPI 1.15: Chỉ số Đổi mới Sư phạm (Pedagogical Innovation Index)

**Mô tả nghiệp vụ**: Đánh giá mức độ thử nghiệm phương pháp mới (flipped classroom, PBL, gamification) trên LMS.

- **Loại chỉ số**: Định tính
- **Công thức tính**: 
  ```
  Innovation Score = Số hóa dựa trên:
  - Số phương pháp mới áp dụng (30%)
  - Báo cáo nghiên cứu hành động (30%)
  - Chia sẻ best practices (20%)
  - Feedback từ đồng nghiệp (20%)
  
  Thang điểm: 1-5
  ```
- **Dữ liệu LMS**: 
  - `teaching_method_tags` trong course metadata
  - `research_action_reports` do GV submit
  - Peer review scores từ Lesson Study
- **Mục đích trên dashboard**:
  - Khuyến khích innovation culture
  - Nhận diện teacher leader
  - Sharing community of practice
- **Ngưỡng đánh giá**:
  - Innovator: ≥ 4.0/5.0
  - Early Adopter: 3.0-3.9/5.0
  - Traditional: < 3.0/5.0
- **Nguồn tham khảo**: 
  - Fullan, M. (2007). *The New Meaning of Educational Change* (4th ed.). Teachers College Press.
  - ISBN: 978-0807747568

---

## TỔNG KẾT NHÓM 1

### Các chỉ số cốt lõi (Core KPIs)
1. **KPI 1.6** - Thời gian phản hồi (quan trọng nhất cho engagement)
2. **KPI 1.9** - Chấm bài đúng hạn (ảnh hưởng trực tiếp đến SV)
3. **KPI 1.13** - Đánh giá của sinh viên (outcome measure)

### Chỉ số bổ trợ (Supporting KPIs)
- Các KPI còn lại hỗ trợ đánh giá toàn diện

### Liên kết Dashboard
- **Realtime Alerts**: KPI 1.1, 1.6, 1.9 (cảnh báo ngay khi vi phạm ngưỡng)
- **Weekly Reports**: KPI 1.2, 1.3, 1.7, 1.11
- **Semester Reviews**: KPI 1.4, 1.5, 1.10, 1.12, 1.13, 1.14, 1.15
- **Comparative Analysis**: So sánh GV theo khoa, bộ môn, kinh nghiệm

---

## NGUỒN THAM KHẢO CHÍNH

Ngoài các nguồn đã trích dẫn ở từng KPI, nhóm chỉ số này còn dựa trên:

1. **OECD (2019)**. *TALIS 2018 Results: Teachers and School Leaders as Lifelong Learners*. 
   - Link: https://www.oecd.org/education/talis/

2. **UNESCO (2020)**. *Global Education Monitoring Report 2020: Inclusion and education*. 
   - Link: https://en.unesco.org/gem-report/

3. **Rienties, B., & Toetenel, L. (2016)**. "The impact of learning design on student behaviour, satisfaction and performance". *Computers & Education*, 103, 76-90.
   - DOI: https://doi.org/10.1016/j.compedu.2016.09.008

---

**Tiếp theo**: [2️⃣ Chỉ số Đánh giá Người học →](./02_Chi_So_Nguoi_Hoc.md)

[← Quay lại README](./README.md)
