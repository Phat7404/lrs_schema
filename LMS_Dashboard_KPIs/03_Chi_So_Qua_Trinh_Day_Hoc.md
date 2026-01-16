# 3️⃣ CHỈ SỐ ĐÁNH GIÁ QUÁ TRÌNH DẠY – HỌC

[← Quay lại README](./README.md)

---

## TỔNG QUAN

Nhóm chỉ số này đánh giá chất lượng thiết kế, triển khai và hiệu quả của quá trình dạy học trên LMS ở cấp độ khóa học/môn học, bao gồm:
- Thiết kế học phần (Course Design)
- Tương tác sư phạm (Pedagogical Interaction)
- Đánh giá và phản hồi liên tục (Continuous Assessment)
- Hiệu quả học tập (Learning Effectiveness)

**Tổng số**: 12 chỉ số (9 định lượng + 3 định tính)

---

## A. THIẾT KẾ HỌC PHẦN

### KPI 3.1: Điểm Alignment với Chuẩn đầu ra (Learning Outcomes Alignment Score)

**Mô tả nghiệp vụ**: Đánh giá mức độ nhất quán giữa mục tiêu học tập (learning outcomes), nội dung, hoạt động và đánh giá theo Constructive Alignment (Biggs).

- **Loại chỉ số**: Định tính (số hóa qua rubric)
- **Công thức tính**: 
  ```
  Alignment Score = Trung bình:
  - Outcomes rõ ràng, đo được (Bloom's Taxonomy) (25%)
  - Activities match outcomes (25%)
  - Assessments test intended outcomes (30%)
  - Grading rubric reflects outcomes (20%)
  
  Thang điểm: 1-5
  ```
- **Dữ liệu LMS**: 
  - `course_syllabus`: learning_outcomes list
  - `course_activities`: mapping to outcomes via tags
  - `assessments`: outcome_assessed field
  - Expert review hoặc automated text analysis (NLP)
- **Mục đích trên dashboard**:
  - Quality assurance cho course design
  - Curriculum review và cải tiến
  - Accreditation compliance (chuẩn CDIO, AUN-QA)
- **Ngưỡng đánh giá**:
  - Well-aligned: ≥ 4.0/5.0
  - Moderately aligned: 3.0-3.9/5.0
  - Needs redesign: < 3.0/5.0
- **Nguồn tham khảo**: 
  - Biggs, J., & Tang, C. (2011). *Teaching for Quality Learning at University* (4th ed.). McGraw-Hill Education.
  - ISBN: 978-0335242757

---

### KPI 3.2: Tỷ lệ Cân đối Thời lượng Học liệu (Content Load Balance)

**Mô tả nghiệp vụ**: Đo lường sự phân bổ đều workload qua các tuần, tránh quá tải hoặc quá ít nội dung ở một thời điểm.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Balance Index = 1 - (Độ lệch chuẩn thời lượng các tuần / Thời lượng TB)
  
  Hoặc: Coefficient of Variation (CV) = StdDev / Mean
  CV < 0.3 = well balanced
  ```
- **Dữ liệu LMS**: 
  - Estimated time per week = Σ(reading time + video duration + assignment time)
  - `course_weekly_schedule`: workload_hours per week
  - Benchmark: 3 tín chỉ = 9 giờ/tuần (3 giờ lớp + 6 giờ tự học)
- **Mục đích trên dashboard**:
  - Phát hiện "peak weeks" quá tải
  - Điều chỉnh thiết kế course
  - Giảm cognitive overload
- **Ngưỡng đánh giá**:
  - Well-balanced: CV < 0.25
  - Moderately balanced: CV 0.25-0.4
  - Unbalanced: CV > 0.4
- **Nguồn tham khảo**: 
  - Kovanović, V., et al. (2016). "Does time-on-task estimation matter?". *Journal of Learning Analytics*, 3(3), 81-110.
  - DOI: https://doi.org/10.18608/jla.2016.33.6

---

### KPI 3.3: Mức độ Tương tác của Nội dung (Content Interactivity Level)

**Mô tả nghiệp vụ**: Tỷ lệ học liệu có tính tương tác (H5P, embedded quiz, simulation) so với nội dung tĩnh (PDF, video thường).

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Interactivity Ratio = (Số tài liệu interactive / Tổng số tài liệu) × 100%
  
  Interactive: H5P, branching scenarios, simulations, embedded quiz
  Static: PDF, plain video, plain text
  ```
- **Dữ liệu LMS**: 
  - `course_resources` với `resource_format`
  - Classification: interactive vs static vs semi-interactive (video với quiz)
- **Mục đích trên dashboard**:
  - Khuyến khích active learning design
  - So sánh với best practices (≥ 30% interactive)
  - Correlation với engagement
- **Ngưỡng đánh giá**:
  - Highly interactive: ≥ 40%
  - Moderately interactive: 20-39%
  - Mostly static: < 20%
- **Nguồn tham khảo**: 
  - Domagk, S., et al. (2010). "Interactivity in multimedia learning". *Educational Psychology Review*, 22(3), 309-326.
  - DOI: https://doi.org/10.1007/s10648-010-9127-7

---

## B. TƯƠNG TÁC SƯ PHẠM

### KPI 3.4: Chỉ số Community of Inquiry (CoI Index)

**Mô tả nghiệp vụ**: Đánh giá 3 yếu tố: Cognitive Presence, Social Presence, Teaching Presence theo mô hình CoI (Garrison et al., 2000).

- **Loại chỉ số**: Định tính (số hóa từ survey + log analysis)
- **Công thức tính**: 
  ```
  CoI Index = Trung bình:
  - Cognitive Presence (33%): Triggering → Exploration → Integration → Resolution
  - Social Presence (33%): Open communication, Group cohesion, Emotional expression
  - Teaching Presence (34%): Design, Facilitation, Direct instruction
  
  Thang điểm: 1-5 (từ survey CoI hoặc content analysis)
  ```
- **Dữ liệu LMS**: 
  - Survey: CoI questionnaire (34 items, 5-point Likert)
  - Forum post analysis: Sentiment, cognitive verbs, social pronouns
  - Instructor activity logs
- **Mục đích trên dashboard**:
  - Đánh giá chất lượng online learning community
  - Cải thiện thiết kế tương tác
  - Dự đoán satisfaction và learning outcomes
- **Ngưỡng đánh giá**:
  - Strong community: ≥ 4.0/5.0
  - Developing community: 3.0-3.9/5.0
  - Weak community: < 3.0/5.0
- **Nguồn tham khảo**: 
  - Garrison, D. R., Anderson, T., & Archer, W. (2000). "Critical inquiry in a text-based environment". *The Internet and Higher Education*, 2(2-3), 87-105.
  - DOI: https://doi.org/10.1016/S1096-7516(00)00016-6
  - CoI Framework: https://coi.athabascau.ca/

---

### KPI 3.5: Tỷ lệ Tương tác Đa chiều (Multi-directional Interaction Rate)

**Mô tả nghiệp vụ**: Đo lường mức độ tương tác không chỉ GV-SV mà còn SV-SV, SV-Nội dung theo Moore's Theory of Transactional Distance.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Interaction Distribution:
  - Teacher-Student: % forum replies from teacher
  - Student-Student: % peer-to-peer discussion threads
  - Student-Content: % time on interactive resources
  
  Balanced course: 20-30% T-S, 40-50% S-S, 30-40% S-C
  ```
- **Dữ liệu LMS**: 
  - `forum_posts`: author_role, parent_post author_role
  - `interaction_logs`: actor, verb, object taxonomy
  - Social Network Analysis: density, centrality
- **Mục đích trên dashboard**:
  - Tránh teacher-centric approach
  - Khuyến khích peer learning
  - Optimize course design
- **Ngưỡng đánh giá**:
  - Balanced: S-S interaction > 40%
  - Teacher-dominant: T-S > 50%
  - Content-only: S-C > 70% (ít tương tác)
- **Nguồn tham khảo**: 
  - Moore, M. G. (1993). "Theory of transactional distance". *Theoretical Principles of Distance Education*, 22-38.
  - Link: https://www.c3l.uni-oldenburg.de/cde/media/readings/moore93.pdf

---

### KPI 3.6: Tần suất Phản hồi Kịp thời (Timely Feedback Frequency)

**Mô tả nghiệp vụ**: Số lần người học nhận được phản hồi (automated hoặc từ GV) trong vòng 24-48 giờ sau hoạt động học tập.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Timely Feedback Rate = (Số hoạt động có feedback ≤ 48h / Tổng hoạt động) × 100%
  
  Hoạt động: quiz, assignment submission, forum post
  ```
- **Dữ liệu LMS**: 
  - `quiz_feedback`: immediate (automated)
  - `assignment_submissions`: graded_time - submitted_time ≤ 48 hours
  - `forum_replies`: reply_time - post_time
- **Mục đích trên dashboard**:
  - Đảm bảo feedback loop nhanh
  - Motivate người học
  - Critical for formative assessment
- **Ngưỡng đánh giá**:
  - Excellent: ≥ 80% timely feedback
  - Good: 60-79%
  - Needs improvement: < 60%
- **Nguồn tham khảo**: 
  - Shute, V. J. (2008). "Focus on formative feedback". *Review of Educational Research*, 78(1), 153-189.
  - DOI: https://doi.org/10.3102/0034654307313795

---

## C. ĐÁNH GIÁ VÀ PHẢN HỒI LIÊN TỤC

### KPI 3.7: Tỷ lệ Đánh giá Hình thành vs Tổng kết (Formative vs Summative Ratio)

**Mô tả nghiệp vụ**: Cân đối giữa đánh giá để học (ungraded/low-stakes) và đánh giá kết quả (high-stakes exams).

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  F/S Ratio = Số formative assessments / Số summative assessments
  
  Hoặc theo trọng số:
  Formative Weight = (Tổng % điểm formative / Total grade) × 100%
  
  Best practice: 40-60% formative, 40-60% summative
  ```
- **Dữ liệu LMS**: 
  - `assessments` với `assessment_type` và `weight`
  - Formative: quiz < 5% grade, self-check, practice test
  - Summative: midterm, final, major assignments
- **Mục đích trên dashboard**:
  - Khuyến khích assessment for learning
  - Balance accountability và learning support
  - Align với modern pedagogy
- **Ngưỡng đánh giá**:
  - Balanced: 40-60% formative weight
  - Summative-dominant: < 30% formative
  - Formative-rich: > 60% formative
- **Nguồn tham khảo**: 
  - Wiliam, D., & Thompson, M. (2007). "Integrating assessment with instruction". *Handbook of Research on Learning and Instruction*, 53-82.
  - DOI: https://doi.org/10.4324/9780203839089.ch4

---

### KPI 3.8: Mức độ Đa dạng Phương pháp Đánh giá (Assessment Diversity Index)

**Mô tả nghiệp vụ**: Số lượng các hình thức đánh giá khác nhau được sử dụng (MCQ, essay, project, presentation, peer review, portfolio).

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Diversity = Số loại assessment method khác nhau / Tổng số phương pháp có thể
  
  Phương pháp: MCQ, Short answer, Essay, Project, Presentation, 
               Peer assessment, Self-assessment, Portfolio, Practical/Lab
  Tổng thường: ~9 phương pháp
  ```
- **Dữ liệu LMS**: 
  - `assessments.assessment_method`
  - Count DISTINCT methods per course
- **Mục đích trên dashboard**:
  - Khuyến khích authentic assessment
  - Đáp ứng đa dạng learning styles
  - Avoid over-reliance on MCQ
- **Ngưỡng đánh giá**:
  - Highly diverse: ≥ 5 phương pháp
  - Moderately diverse: 3-4 phương pháp
  - Limited: ≤ 2 phương pháp
- **Nguồn tham khảo**: 
  - Gulikers, J. T., et al. (2004). "A five-dimensional framework for authentic assessment". *Educational Technology Research and Development*, 52(3), 67-86.
  - DOI: https://doi.org/10.1007/BF02504676

---

### KPI 3.9: Chỉ số Sử dụng Rubric (Rubric Usage Rate)

**Mô tả nghiệp vụ**: Tỷ lệ assignment/project có rubric chấm điểm rõ ràng, giúp người học hiểu tiêu chí đánh giá.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Rubric Usage = (Số assignment có rubric / Tổng số assignment) × 100%
  
  "Có rubric": rubric được publish trước deadline, ≥ 3 criteria
  ```
- **Dữ liệu LMS**: 
  - `assignments.rubric_id` IS NOT NULL
  - `rubrics`: criteria count, published before due_date
- **Mục đích trên dashboard**:
  - Promote transparency trong đánh giá
  - Giảm perceived unfairness
  - Support self-assessment
- **Ngưỡng đánh giá**:
  - Excellent: ≥ 90% assignments có rubric
  - Good: 70-89%
  - Needs improvement: < 70%
- **Nguồn tham khảo**: 
  - Andrade, H., & Du, Y. (2005). "Student perspectives on rubric-referenced assessment". *Practical Assessment, Research & Evaluation*, 10(5), 1-11.
  - Link: https://scholarworks.umass.edu/pare/vol10/iss1/5/

---

## D. HIỆU QUẢ HỌC TẬP

### KPI 3.10: Tỷ lệ Đạt Chuẩn đầu ra (Learning Outcomes Achievement Rate)

**Mô tả nghiệp vụ**: Phần trăm người học đạt được các chuẩn đầu ra (PLOs/CLOs) của môn học ở mức tối thiểu.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  LO Achievement = (Số SV đạt ≥ 70% mỗi LO / Tổng số SV) × 100%
  
  Đo qua: Mapping assessment items → LOs, tính điểm TB cho mỗi LO
  ```
- **Dữ liệu LMS**: 
  - `learning_outcomes_assessment`: student_id, outcome_id, score
  - `assessment_items.outcome_mapping`
  - Aggregate score per outcome per student
- **Mục đích trên dashboard**:
  - Program assessment & accreditation
  - Identify weak outcomes → revise teaching
  - Compare cohorts over time
- **Ngưỡng đánh giá**:
  - Excellent: ≥ 80% đạt tất cả LOs
  - Acceptable: 60-79%
  - Needs intervention: < 60%
- **Nguồn tham khảo**: 
  - Suskie, L. (2018). *Assessing Student Learning: A Common Sense Guide* (3rd ed.). Jossey-Bass.
  - ISBN: 978-1119426738

---

### KPI 3.11: Tỷ lệ Retention (Course Retention Rate)

**Mô tả nghiệp vụ**: Phần trăm người học vẫn còn tích cực tham gia đến cuối khóa học, không bỏ học giữa chừng.

- **Loại chỉ số**: Định lượng
- **Công thức tính**: 
  ```
  Retention Rate = (Số SV complete hoặc active cuối kỳ / Số SV enroll đầu kỳ) × 100%
  
  Active: login trong 2 tuần cuối hoặc nộp assignment cuối
  ```
- **Dữ liệu LMS**: 
  - `course_enrollments`: enrollment_date, withdrawal_date, last_access_date
  - Retention = không có withdrawal_date VÀ last_access gần cuối kỳ
- **Mục đích trên dashboard**:
  - Course quality indicator
  - Identify at-risk students sớm
  - Compare teaching methods/instructors
- **Ngưỡng đánh giá**:
  - Excellent: ≥ 90%
  - Good: 80-89%
  - Concerning: < 80%
- **Nguồn tham khảo**: 
  - Tinto, V. (2006). "Research and practice of student retention: What next?". *Journal of College Student Retention*, 8(1), 1-19.
  - DOI: https://doi.org/10.2190/4YNU-4TMB-22DJ-AN4W

---

### KPI 3.12: Điểm Hài lòng của Người học (Student Satisfaction Score)

**Mô tả nghiệp vụ**: Kết quả khảo sát cuối khóa về mức độ hài lòng với thiết kế, nội dung, giảng dạy và LMS experience.

- **Loại chỉ số**: Định tính (số hóa từ survey)
- **Công thức tính**: 
  ```
  Satisfaction Score = Trung bình từ end-of-course survey
  
  Các câu hỏi:
  - Course design và organization (25%)
  - Quality of content và materials (25%)
  - Instructor effectiveness (25%)
  - LMS usability và support (25%)
  
  Thang điểm: 1-5 hoặc 1-10
  ```
- **Dữ liệu LMS**: 
  - `course_evaluation_survey`: Likert scale responses
  - Open-ended comments (sentiment analysis)
  - Net Promoter Score (NPS): "Recommend course to others?"
- **Mục đích trên dashboard**:
  - Overall course quality measure
  - Instructor performance feedback
  - Continuous improvement
- **Ngưỡng đánh giá**:
  - Highly satisfied: ≥ 4.0/5.0
  - Satisfied: 3.5-3.9/5.0
  - Needs improvement: < 3.5/5.0
- **Nguồn tham khảo**: 
  - Rienties, B., et al. (2015). "Understanding academic performance of international students". *Higher Education*, 70(3), 511-528.
  - DOI: https://doi.org/10.1007/s10734-014-9838-0

---

## TỔNG KẾT NHÓM 3

### KPIs Thiết kế (Design Quality) - Pre-course
- **KPI 3.1** - Learning outcomes alignment
- **KPI 3.2** - Content load balance
- **KPI 3.3** - Content interactivity
- **KPI 3.7, 3.8** - Assessment design

→ Sử dụng cho: Course review, Peer review, Quality assurance

### KPIs Quá trình (Process Quality) - During course
- **KPI 3.4** - Community of Inquiry
- **KPI 3.5** - Multi-directional interaction
- **KPI 3.6** - Timely feedback
- **KPI 3.9** - Rubric usage

→ Sử dụng cho: Mid-course adjustments, Instructor coaching

### KPIs Kết quả (Outcome Quality) - Post-course
- **KPI 3.10** - Learning outcomes achievement
- **KPI 3.11** - Retention rate
- **KPI 3.12** - Student satisfaction

→ Sử dụng cho: Program assessment, Accreditation, Strategic decisions

### Dashboard Views
**Course Design Dashboard**:
- Pre-launch checklist: KPI 3.1, 3.2, 3.3, 3.7, 3.8 phải ≥ threshold
- Peer review scores
- Comparison với course template

**Course Delivery Dashboard** (realtime):
- Weekly: KPI 3.4, 3.5, 3.6
- Student engagement heatmap
- Alert: Low interaction, delayed feedback

**Course Evaluation Dashboard** (end-of-semester):
- KPI 3.10, 3.11, 3.12
- Trend analysis: Compare với previous offerings
- Action items for next iteration

---

## NGUỒN THAM KHẢO CHÍNH

1. **Laurillard, D. (2012)**. *Teaching as a Design Science: Building Pedagogical Patterns for Learning and Technology*. Routledge.
   - ISBN: 978-0415803878

2. **Boud, D., & Molloy, E. (2013)**. *Feedback in Higher and Professional Education*. Routledge.
   - ISBN: 978-0415696760

3. **OECD (2018)**. *The Future of Education and Skills: Education 2030*.
   - Link: https://www.oecd.org/education/2030-project/

4. **Quality Matters (QM) Higher Education Rubric** (2020). 6th Edition.
   - Link: https://www.qualitymatters.org/

5. **UNESCO (2017)**. *E-Learning Methodologies: A Guide for Designing and Developing E-Learning Courses*.
   - Link: https://www.fao.org/3/i2516e/i2516e.pdf

---

**Tiếp theo**: [4️⃣ Chỉ số Đánh giá Môi trường LMS & Học tập Số →](./04_Chi_So_Moi_Truong_LMS.md)

[← Quay lại README](./README.md)
