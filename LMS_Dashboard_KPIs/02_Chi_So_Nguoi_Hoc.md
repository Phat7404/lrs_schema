# 2️⃣ CHỈ SỐ ĐÁNH GIÁ NGƯỜI HỌC

[← Quay lại README](./README.md)

---

## TỔNG QUAN

Nhóm chỉ số này đánh giá mức độ tham gia, tiến độ, kết quả và hành vi học tập của người học (học sinh, sinh viên) trên LMS, bao gồm:
- Mức độ tham gia (Engagement)
- Tiến độ học tập (Progress)
- Kết quả học tập (Achievement)
- Hành vi học tập (Learning Behavior)

**Tổng số**: 18 chỉ số (15 định lượng + 3 định tính)

---

## A. MỨC ĐỘ THAM GIA (ENGAGEMENT)

### KPI 2.1: Tần suất Đăng nhập của Người học

**Mô tả nghiệp vụ**: Số lần người học truy cập LMS, phản ánh mức độ chủ động tham gia học tập trực tuyến.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Login Frequency = Tổng số lần login / Số tuần trong kỳ học
  ```
- **Dữ liệu LMS**: 
  - `user_login_history` với `user_id`, `login_timestamp`
  - Filter: `user_role = 'student'`
- **Mục đích trên dashboard**:
  - Phát hiện sớm sinh viên "mất tích"
  - Cảnh báo nếu không login > 5 ngày
  - Phân loại nhóm người học: Active / At-risk / Dropout risk
- **Ngưỡng đánh giá**:
  - Highly engaged: ≥ 4 lần/tuần
  - Moderately engaged: 2-3 lần/tuần
  - At-risk: < 2 lần/tuần
- **Nguồn tham khảo**: 
  - Kuh, G. D. (2009). "What student affairs professionals need to know about student engagement". *Journal of College Student Development*, 50(6), 683-706.
  - DOI: https://doi.org/10.1353/csd.0.0099

---

### KPI 2.2: Thời lượng Học tập Trực tuyến (Time on Task)

**Mô tả nghiệp vụ**: Tổng thời gian người học dành cho các hoạt động học tập trên LMS, chỉ báo quan trọng dự đoán kết quả học tập.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Weekly Time on Task = SUM(session_duration) per week (hours)
  
  Lọc: session_duration > 2 phút và < 6 giờ (loại outliers)
  ```
- **Dữ liệu LMS**: 
  - `session_log`: `session_start`, `session_end`, `user_id`
  - `activity_log`: time spent on specific resources
  - xAPI: `duration` từ xAPI statements
- **Mục đích trên dashboard**:
  - So sánh với khuyến nghị (ví dụ: 5-8 giờ/tuần)
  - Phát hiện "zombie learners" (login nhưng không hoạt động)
  - Liên hệ với kết quả học tập
- **Ngưỡng đánh giá**:
  - Optimal: 6-10 giờ/tuần
  - Low engagement: < 4 giờ/tuần
  - Excessive: > 15 giờ/tuần (có thể gặp khó khăn)
- **Nguồn tham khảo**: 
  - Rienties, B., & Toetenel, L. (2016). "The impact of learning design on student behaviour". *Computers & Education*, 103, 76-90.
  - DOI: https://doi.org/10.1016/j.compedu.2016.09.008

---

### KPI 2.3: Tỷ lệ Hoàn thành Tài liệu (Resource Completion Rate)

**Mô tả nghiệp vụ**: Phần trăm tài liệu học tập (video, bài đọc, SCORM) được người học hoàn thành so với tổng số tài liệu bắt buộc.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Completion Rate = (Số tài liệu đã complete / Tổng số tài liệu required) × 100%
  
  Complete: > 90% nội dung hoặc xAPI: completed/passed
  ```
- **Dữ liệu LMS**: 
  - `resource_tracking`: `resource_id`, `user_id`, `completion_status`
  - SCORM: `cmi.core.lesson_status = "completed"`
  - Video: watched ≥ 80% duration
- **Mục đích trên dashboard**:
  - Theo dõi tiến độ học từng chủ đề
  - Phát hiện tài liệu "bị bỏ qua"
  - Cảnh báo sớm nếu completion < 60%
- **Ngưỡng đánh giá**:
  - On-track: ≥ 80%
  - Needs support: 50-79%
  - Falling behind: < 50%
- **Nguồn tham khảo**: 
  - Kizilcec, R. F., et al. (2013). "Deconstructing disengagement: analyzing learner subpopulations in massive open online courses". *LAK '13: 3rd International Conference on Learning Analytics*.
  - DOI: https://doi.org/10.1145/2460296.2460330

---

### KPI 2.4: Tỷ lệ Tham gia Thảo luận (Discussion Participation Rate)

**Mô tả nghiệp vụ**: Mức độ đóng góp của người học vào các diễn đàn, thảo luận nhóm, phản ánh khả năng collaborative learning.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Participation Rate = (Số SV có ≥ 1 post / Tổng số SV trong lớp) × 100%
  
  Hoặc đo sâu hơn:
  Quality Participation = Weighted(số post, số reply, upvotes, word count)
  ```
- **Dữ liệu LMS**: 
  - `forum_posts`: `post_id`, `author_id`, `post_type` (new thread vs reply)
  - `discussion_analytics`: likes, replies received
- **Mục đích trên dashboard**:
  - Khuyến khích active learning
  - Phát hiện "lurkers" (chỉ đọc không viết)
  - Đánh giá nhóm collaborative
- **Ngưỡng đánh giá**:
  - Highly participatory: ≥ 75% SV tham gia
  - Moderately participatory: 50-74%
  - Low participation: < 50%
- **Nguồn tham khảo**: 
  - Hew, K. F., et al. (2010). "Student contribution in asynchronous online discussion". *Instructional Science*, 38(6), 571-606.
  - DOI: https://doi.org/10.1007/s11251-008-9087-0

---

### KPI 2.5: Chỉ số Tương tác với Giảng viên (Student-Teacher Interaction Index)

**Mô tả nghiệp vụ**: Tần suất người học chủ động liên hệ GV qua tin nhắn, câu hỏi forum, office hours online.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Interaction Index = (Số tin nhắn gửi GV + Số câu hỏi posted) / Số tuần
  ```
- **Dữ liệu LMS**: 
  - `messages`: sender = student, recipient = teacher
  - `forum_posts`: tag = "question_for_instructor"
  - `virtual_office_hours_attendance`
- **Mục đích trên dashboard**:
  - Đánh giá sự chủ động tìm sự hỗ trợ
  - Phát hiện SV "im lặng" cần quan tâm
  - Đo lường accessibility của GV
- **Ngưỡng đánh giá**:
  - Proactive: ≥ 1 tương tác/tuần
  - Moderate: 1-2 tương tác/tháng
  - Passive: < 1 tương tác/tháng
- **Nguồn tham khảo**: 
  - Jaggars, S. S., & Xu, D. (2016). "How do online course design features influence student performance?". *Computers & Education*, 95, 270-284.
  - DOI: https://doi.org/10.1016/j.compedu.2016.01.014

---

##  B. TIẾN ĐỘ HỌC TẬP (PROGRESS)

### KPI 2.6: Tỷ lệ Hoàn thành Khóa học (Course Completion Rate)

**Mô tả nghiệp vụ**: Phần trăm người học hoàn thành toàn bộ yêu cầu của khóa học, chỉ số quan trọng nhất đo lường retention.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Completion Rate = (Số SV pass course / Số SV enroll ban đầu) × 100%
  
  Pass: đạt ≥ 50% điểm + hoàn thành ≥ 80% activities
  ```
- **Dữ liệu LMS**: 
  - `course_enrollments`: `enrollment_date`, `completion_status`, `final_grade`
  - `course_completion_criteria`: checklist activities + grade threshold
- **Mục đích trên dashboard**:
  - Đo lường success rate của course
  - So sánh giữa các cohorts
  - Early warning cho dropout risk
- **Ngưỡng đánh giá**:
  - Excellent: ≥ 85%
  - Good: 70-84%
  - Concerning: < 70%
- **Nguồn tham khảo**: 
  - Xu, D., & Jaggars, S. S. (2014). "Performance gaps between online and face-to-face courses". *Distance Education*, 35(3), 357-377.
  - DOI: https://doi.org/10.1080/01587919.2015.955262

---

### KPI 2.7: Tiến độ So với Kế hoạch (Progress vs. Timeline)

**Mô tả nghiệp vụ**: Đánh giá người học có đúng tiến độ so với lộ trình học tập được thiết kế hay bị chậm/vượt trước.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Progress Index = (% hoàn thành thực tế / % hoàn thành dự kiến) × 100%
  
  Ví dụ: Tuần 5/10, dự kiến 50%, thực tế 60% → PI = 120% (ahead)
  ```
- **Dữ liệu LMS**: 
  - `learning_path_progress`: expected milestones vs actual
  - `adaptive_learning_timeline`
  - So sánh `completed_activities_date` với `scheduled_date`
- **Mục đích trên dashboard**:
  - Realtime tracking tiến độ cá nhân
  - Adaptive recommendations
  - Cảnh báo fall-behind sớm
- **Ngưỡng đánh giá**:
  - Ahead: Progress Index > 110%
  - On-track: 90-110%
  - Behind: < 90% (cần can thiệp)
- **Nguồn tham khảo**: 
  - Teasley, S. D. (2017). "Student facing dashboards: One size fits all?". *Technology, Knowledge and Learning*, 22(3), 377-384.
  - DOI: https://doi.org/10.1007/s10758-017-9314-3

---

### KPI 2.8: Tốc độ Hoàn thành Bài học (Module Completion Velocity)

**Mô tả nghiệp vụ**: Thời gian trung bình để hoàn thành mỗi module/chương, giúp dự đoán khả năng hoàn thành khóa học.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Velocity = Trung bình(completion_date - start_date) per module (days)
  
  So sánh với estimated time: 7 days/module
  ```
- **Dữ liệu LMS**: 
  - `module_tracking`: `module_id`, `user_id`, `started_at`, `completed_at`
  - Tính median velocity để tránh outliers
- **Mục đích trên dashboard**:
  - Dự báo thời gian hoàn thành course
  - Phát hiện "stuck points" (module mất quá nhiều thời gian)
  - Personalized pacing recommendations
- **Ngưỡng đánh giá**:
  - Fast learner: ≤ estimated time
  - On-pace: 100-120% estimated time
  - Struggling: > 150% estimated time
- **Nguồn tham khảo**: 
  - Ferguson, R., & Clow, D. (2015). "Consistent commitment: patterns of engagement across time in massive open online courses". *Journal of Learning Analytics*, 2(3), 55-80.
  - DOI: https://doi.org/10.18608/jla.2015.23.5

---

## C. KẾT QUẢ HỌC TẬP (ACHIEVEMENT)

### KPI 2.9: Điểm Trung bình Tích lũy (Cumulative GPA)

**Mô tả nghiệp vụ**: Điểm số trung bình của tất cả các bài kiểm tra, assignment, quiz trên LMS.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Cumulative GPA = Σ(điểm bài tập × trọng số) / Σ trọng số
  
  Thang điểm: 0-10 hoặc 0-100
  ```
- **Dữ liệu LMS**: 
  - `gradebook`: `assignment_id`, `user_id`, `score`, `max_score`, `weight`
  - Tính weighted average
- **Mục đích trên dashboard**:
  - Theo dõi academic performance
  - Xếp hạng và phân nhóm người học
  - Liên hệ với engagement metrics
- **Ngưỡng đánh giá**:
  - Excellent: ≥ 8.5/10
  - Good: 7.0-8.4/10
  - Pass: 5.0-6.9/10
  - At-risk: < 5.0/10
- **Nguồn tham khảo**: 
  - Richardson, M., et al. (2012). "Psychological correlates of university students' academic performance". *Psychological Bulletin*, 138(2), 353-387.
  - DOI: https://doi.org/10.1037/a0026838

---

### KPI 2.10: Tỷ lệ Nộp bài Đúng hạn (On-time Submission Rate)

**Mô tả nghiệp vụ**: Phần trăm bài tập được nộp trước hoặc đúng deadline, phản ánh tính tổ chức và kỷ luật học tập.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  On-time Rate = (Số bài nộp đúng giờ / Tổng số bài assignment) × 100%
  
  Đúng giờ: submission_time ≤ deadline
  ```
- **Dữ liệu LMS**: 
  - `assignment_submissions`: `submission_timestamp`, `due_date`
  - Tính cho từng SV và trung bình lớp
- **Mục đích trên dashboard**:
  - Đánh giá time management skill
  - Dự đoán academic success
  - Reminder notifications cho late submitters
- **Ngưỡng đánh giá**:
  - Excellent: ≥ 90%
  - Good: 75-89%
  - Needs improvement: < 75%
- **Nguồn tham khảo**: 
  - You, J. W. (2016). "Identifying significant indicators using LMS data to predict course achievement in online learning". *Internet and Higher Education*, 29, 23-30.
  - DOI: https://doi.org/10.1016/j.iheduc.2015.11.003

---

### KPI 2.11: Tỷ lệ Đạt ở Lần thi Đầu tiên (First Attempt Pass Rate)

**Mô tả nghiệp vụ**: Phần trăm quiz/test được pass ngay lần làm đầu tiên, chỉ báo sự chuẩn bị và nắm vững kiến thức.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  First Attempt Pass = (Số quiz pass lần 1 / Tổng số quiz attempted) × 100%
  
  Pass: score ≥ passing threshold (thường 60-70%)
  ```
- **Dữ liệu LMS**: 
  - `quiz_attempts`: `quiz_id`, `user_id`, `attempt_number`, `score`
  - Filter: `attempt_number = 1`
- **Mục đích trên dashboard**:
  - Đánh giá chất lượng tự học
  - Phát hiện nhu cầu review trước khi thi
  - So sánh hiệu quả các phương pháp học
- **Ngưỡng đánh giá**:
  - Well-prepared: ≥ 80%
  - Moderately prepared: 60-79%
  - Under-prepared: < 60%
- **Nguồn tham khảo**: 
  - Gikandi, J. W., et al. (2011). "Online formative assessment in higher education: A review". *Computers & Education*, 57(4), 2333-2351.
  - DOI: https://doi.org/10.1016/j.compedu.2011.06.004

---

### KPI 2.12: Xu hướng Cải thiện Điểm số (Grade Improvement Trend)

**Mô tả nghiệp vụ**: Đánh giá sự tiến bộ qua thời gian, so sánh điểm các assignment/quiz từ đầu đến cuối kỳ.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Improvement Trend = (Điểm TB 4 tuần cuối - Điểm TB 4 tuần đầu) / Điểm TB 4 tuần đầu × 100%
  
  Positive trend: > +10%
  ```
- **Dữ liệu LMS**: 
  - `gradebook` với `submission_date`, `score`
  - Time series analysis: Linear regression slope
- **Mục đích trên dashboard**:
  - Ghi nhận "most improved students"
  - Phát hiện downward trend sớm
  - Đánh giá hiệu quả interventions
- **Ngưỡng đánh giá**:
  - Strong improvement: > +20%
  - Moderate improvement: +5% to +20%
  - Declining: < 0%
- **Nguồn tham khảo**: 
  - Macfadyen, L. P., & Dawson, S. (2010). "Mining LMS data to develop an 'early warning system'". *Computers & Education*, 54(2), 588-599.
  - DOI: https://doi.org/10.1016/j.compedu.2009.09.008

---

## D. HÀNH VI HỌC TẬP (LEARNING BEHAVIOR)

### KPI 2.13: Mức độ Tự Điều chỉnh Học tập (Self-Regulated Learning Index)

**Mô tả nghiệp vụ**: Đo lường khả năng lập kế hoạch, theo dõi tiến độ và điều chỉnh phương pháp học của người học.

- **Loại chỉ số**: Định lượng (kết hợp định tính)
- **Công thức tính**: 
  ```
  SRL Index = Weighted score of:
  - Planning behaviors (30%): tạo study schedule, set goals
  - Monitoring (40%): check progress dashboard, review feedback
  - Adjusting (30%): redo quiz, access extra resources after poor performance
  
  Thang điểm: 1-100
  ```
- **Dữ liệu LMS**: 
  - `goal_setting_log`: student-set milestones
  - `dashboard_access`: frequency of checking own progress
  - `reattempt_patterns`: retry after failure
  - Survey: SRL questionnaire (Zimmerman, 2002)
- **Mục đích trên dashboard**:
  - Phát triển metacognitive skills
  - Personalized coaching
  - Dự đoán long-term success
- **Ngưỡng đánh giá**:
  - Highly self-regulated: ≥ 75/100
  - Moderately self-regulated: 50-74/100
  - Needs scaffolding: < 50/100
- **Nguồn tham khảo**: 
  - Zimmerman, B. J. (2002). "Becoming a self-regulated learner". *Theory Into Practice*, 41(2), 64-70.
  - DOI: https://doi.org/10.1207/s15430421tip4102_2

---

### KPI 2.14: Chỉ số Học tập Chủ động (Active Learning Index)

**Mô tả nghiệp vụ**: Đánh giá mức độ người học tham gia các hoạt động yêu cầu tư duy cao (phân tích, tổng hợp, đánh giá) thay vì chỉ tiêu thụ thụ động.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Active Learning = (Số hoạt động active / Tổng số hoạt động) × 100%
  
  Active activities: Discussion, case study, project, peer review, 
                     problem-solving, simulation
  Passive: Video watching, reading only
  ```
- **Dữ liệu LMS**: 
  - `activity_log` với `activity_type` taxonomy
  - Bloom's Taxonomy mapping: Remember (passive) → Create (active)
  - xAPI verbs: "created", "evaluated", "discussed" vs "viewed", "read"
- **Mục đích trên dashboard**:
  - Khuyến khích deeper learning
  - So sánh với course design intentions
  - Liên hệ với retention of knowledge
- **Ngưỡng đánh giá**:
  - Highly active: ≥ 60% active learning
  - Balanced: 40-59%
  - Passive dominant: < 40%
- **Nguồn tham khảo**: 
  - Prince, M. (2004). "Does active learning work? A review of the research". *Journal of Engineering Education*, 93(3), 223-231.
  - DOI: https://doi.org/10.1002/j.2168-9830.2004.tb00809.x

---

### KPI 2.15: Mô hình Thời gian Học tập (Learning Time Pattern)

**Mô tả nghiệp vụ**: Phân tích khi nào người học thường hoạt động (sáng/chiều/tối, ngày thường/cuối tuần) để hiểu learning behavior và phát hiện cramming.

- **Loại chỉ số**: Định tính (mô tả pattern)
- **Công thức tính**: 
  ```
  Pattern Analysis:
  - % time spent per day of week
  - % time spent per time of day (morning/afternoon/evening/night)
  - Clustered learning vs Distributed learning
  ```
- **Dữ liệu LMS**: 
  - `session_log`: `login_time`, `session_duration`
  - Heatmap: day × hour
  - Detect cramming: > 50% learning trong 48h trước deadline
- **Mục đích trên dashboard**:
  - Phát hiện last-minute cramming (không hiệu quả)
  - Khuyến khích spaced practice
  - Personalized scheduling recommendations
- **Ngưỡng đánh giá**:
  - Optimal: distributed practice (< 20% hoạt động cùng 1 ngày)
  - Cramming: > 50% time trong 2 ngày trước deadline
- **Nguồn tham khảo**: 
  - Kang, S. H. K. (2016). "Spaced repetition promotes efficient and effective learning". *Policy Insights from Behavioral and Brain Sciences*, 3(1), 12-19.
  - DOI: https://doi.org/10.1177/2372732215624708

---

### KPI 2.16: Tỷ lệ Tìm kiếm Tài nguyên Bổ sung (Resource-Seeking Behavior)

**Mô tả nghiệp vụ**: Mức độ người học chủ động tìm kiếm thêm tài liệu, video, link ngoài khóa học để mở rộng kiến thức.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Resource-Seeking = (Số tài liệu optional accessed / Tổng tài liệu optional) × 100%
  
  Hoặc: Số external links clicked, library database accessed
  ```
- **Dữ liệu LMS**: 
  - `resource_tracking` với `resource_type = 'optional'` hoặc `'supplementary'`
  - `external_link_clicks`
  - Integration: Library system API
- **Mục đích trên dashboard**:
  - Nhận diện motivated learners
  - Đánh giá intellectual curiosity
  - Correlation với high achievement
- **Ngưỡng đánh giá**:
  - Highly motivated: ≥ 50% optional resources
  - Moderately curious: 25-49%
  - Minimal seeking: < 25%
- **Nguồn tham khảo**: 
  - Kizilcec, R. F., et al. (2017). "Self-regulated learning strategies predict learner behavior". *LAK '17: Learning Analytics & Knowledge*.
  - DOI: https://doi.org/10.1145/3027385.3027402

---

### KPI 2.17: Điểm Collaboration trong Nhóm Học tập

**Mô tả nghiệp vụ**: Đánh giá mức độ đóng góp và làm việc nhóm hiệu quả trong các dự án/assignment nhóm.

- **Loại chỉ số**: Định tính (số hóa từ peer assessment)
- **Công thức tính**: 
  ```
  Collaboration Score = Trung bình:
  - Peer rating (40%): đánh giá từ thành viên nhóm
  - Contribution metrics (30%): Edit count, upload count trong group workspace
  - Communication (30%): Số tin nhắn trong group chat
  
  Thang điểm: 1-5
  ```
- **Dữ liệu LMS**: 
  - `peer_assessment_responses`: rubric items về teamwork
  - `group_wiki_edits`, `shared_document_contributions`
  - `group_forum_posts`
- **Mục đích trên dashboard**:
  - Phát hiện "social loafers"
  - Ghi nhận team leaders
  - Phát triển 21st century skills
- **Ngưỡng đánh giá**:
  - Excellent collaborator: ≥ 4.0/5.0
  - Good team player: 3.0-3.9/5.0
  - Needs improvement: < 3.0/5.0
- **Nguồn tham khảo**: 
  - Strijbos, J. W., & Weinberger, A. (2010). "Emerging and scripted roles in computer-supported collaborative learning". *Computers in Human Behavior*, 26(4), 491-494.
  - DOI: https://doi.org/10.1016/j.chb.2009.08.006

---

### KPI 2.18: Chỉ số Kiên trì (Persistence/Grit Index)

**Mô tả nghiệp vụ**: Đo lường mức độ không bỏ cuộc khi gặp khó khăn, thể hiện qua việc thử lại sau thất bại, tìm kiếm trợ giúp.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Persistence = Score based on:
  - Reattempt failed quizzes/assignments (40%)
  - Access help resources after poor performance (30%)
  - Continue despite low early grades (30%)
  
  Thang điểm: 0-100
  ```
- **Dữ liệu LMS**: 
  - `quiz_attempts`: reattempt count after fail
  - `help_seeking_log`: forum posts, tutor session after low score
  - Retention after receiving < 50% on first major assignment
- **Mục đích trên dashboard**:
  - Dự đoán dropout risk (low grit = high risk)
  - Interventions cho "giving up" patterns
  - Celebrate growth mindset
- **Ngưỡng đánh giá**:
  - High grit: ≥ 75/100
  - Moderate grit: 50-74/100
  - Low grit (dropout risk): < 50/100
- **Nguồn tham khảo**: 
  - Duckworth, A. L., et al. (2007). "Grit: Perseverance and passion for long-term goals". *Journal of Personality and Social Psychology*, 92(6), 1087-1101.
  - DOI: https://doi.org/10.1037/0022-3514.92.6.1087

---

## TỔNG KẾT NHÓM 2

### Các chỉ số cốt lõi (Core KPIs) - Priority Tier 1
1. **KPI 2.6** - Course Completion Rate (quan trọng nhất)
2. **KPI 2.9** - Cumulative GPA (outcome measure)
3. **KPI 2.1** - Login Frequency (early warning)
4. **KPI 2.7** - Progress vs Timeline (actionable)

### Chỉ số dự đoán (Predictive KPIs) - Priority Tier 2
- **KPI 2.2, 2.3, 2.10** - Predict success/dropout
- **KPI 2.13, 2.18** - Predict long-term outcomes

### Chỉ số phát triển (Developmental KPIs) - Priority Tier 3
- **KPI 2.14, 2.16, 2.17** - Develop 21st century skills

### Mô hình Dashboard Student View
**Student-facing Dashboard** nên hiển thị:
- **Current Status**: KPI 2.1, 2.2, 2.3, 2.7, 2.9
- **Warnings**: KPI 2.7 (behind), KPI 2.10 (late submissions)
- **Recommendations**: Dựa trên KPI 2.13 (SRL), 2.15 (time pattern)
- **Achievements**: KPI 2.12 (improvement), badges

**Instructor Dashboard** nên có:
- **Class Overview**: Trung bình tất cả KPIs
- **At-Risk Students**: Low KPI 2.1, 2.2, 2.3, 2.6
- **High Performers**: Top 10% theo KPI 2.9 + engagement

---

## NGUỒN THAM KHẢO CHÍNH

Ngoài các trích dẫn cụ thể, nhóm KPI này dựa trên:

1. **Kuh, G. D., et al. (2010)**. *Student Success in College: Creating Conditions That Matter*. Jossey-Bass.
   - ISBN: 978-0470599099

2. **Arnold, K. E., & Pistilli, M. D. (2012)**. "Course signals at Purdue: Using learning analytics to increase student success". *LAK '12*, 267-270.
   - DOI: https://doi.org/10.1145/2330601.2330666

3. **Tinto, V. (2017)**. "Through the eyes of students". *Journal of College Student Retention*, 19(3), 254-269.
   - DOI: https://doi.org/10.1177/1521025115621917

4. **UNESCO (2021)**. *Digital Learning and Transformation of Education*. 
   - Link: https://www.unesco.org/en/digital-education

---

**Tiếp theo**: [3️⃣ Chỉ số Đánh giá Quá trình Dạy – Học →](./03_Chi_So_Qua_Trinh_Day_Hoc.md)

[← Quay lại README](./README.md)
