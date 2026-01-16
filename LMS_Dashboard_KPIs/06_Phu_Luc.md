# 📖 PHỤ LỤC: CÔNG THỨC CHI TIẾT & ỨNG DỤNG

[← Quay lại README](./README.md)

---

## MỤC LỤC PHỤ LỤC

- **A. Công thức Toán học Chi tiết**
- **B. Ví dụ Tính toán Thực tế**
- **C. SQL Queries Mẫu cho Moodle**
- **D. xAPI Statements Mapping**
- **E. Dashboard Wireframes**
- **F. Bảng Ngưỡng Đánh giá Tổng hợp**
- **G. Checklist Triển khai**

---

## A. CÔNG THỨC TOÁN HỌC CHI TIẾT

### A1. Statistical Measures

#### Trung bình có trọng số (Weighted Average)
```
Công thức:
x̄ = (Σ wi × xi) / Σ wi

Trong đó:
- xi: giá trị thứ i
- wi: trọng số của giá trị i
- Σ: tổng

Ứng dụng: KPI 2.9 (Cumulative GPA), KPI 3.1 (Alignment Score)
```

#### Độ lệch chuẩn (Standard Deviation)
```
Công thức:
σ = √[Σ(xi - x̄)² / N]

Trong đó:
- xi: giá trị thứ i
- x̄: trung bình
- N: số lượng quan sát

Ứng dụng: KPI 3.2 (Content Load Balance)
```

#### Hệ số biến thiên (Coefficient of Variation)
```
Công thức:
CV = (σ / x̄) × 100%

CV < 15%: Low variability (very consistent)
CV 15-30%: Moderate variability
CV > 30%: High variability

Ứng dụng: KPI 3.2 - Đánh giá sự đồng đều workload
```

### A2. Percentile & Distribution

#### Percentile Rank
```
Công thức:
PR = (B + 0.5E) / N × 100

Trong đó:
- B: số quan sát dưới giá trị X
- E: số quan sát bằng giá trị X
- N: tổng số quan sát

Ứng dụng: Xếp hạng sinh viên theo engagement scores
```

#### Z-score (Standardization)
```
Công thức:
z = (x - μ) / σ

Trong đó:
- x: giá trị cần chuẩn hóa
- μ: trung bình tổng thể
- σ: độ lệch chuẩn

Ứng dụng: So sánh KPIs khác thang đo
```

### A3. Trend Analysis

#### Linear Regression (Simple)
```
Công thức:
y = b₀ + b₁x

Trong đó:
- b₁ = Σ[(xi - x̄)(yi - ȳ)] / Σ(xi - x̄)²  (slope)
- b₀ = ȳ - b₁x̄  (intercept)

Ứng dụng: KPI 2.12 (Grade Improvement Trend)
```

#### Growth Rate
```
Công thức:
Growth Rate = [(Valuefinal - Valueinitial) / Valueinitial] × 100%

Ứng dụng: So sánh semester-to-semester improvement
```

---

## B. VÍ DỤ TÍNH TOÁN THỰC TẾ

### B1. Ví dụ KPI 2.13: Self-Regulated Learning Index

**Bối cảnh**: Sinh viên Nguyễn Văn A trong khóa học "Lập trình Python"

**Dữ liệu thu thập**:
1. **Planning behaviors** (30%):
   - Đã tạo study schedule: Có (1 point)
   - Đã đặt learning goals: Có (1 point)
   - Score: (1 + 1) / 2 × 30 = **30 points**

2. **Monitoring** (40%):
   - Số lần check progress dashboard: 15 lần/tháng
   - Benchmark: ≥ 10 lần = full points
   - Số lần review feedback: 8/10 assignments
   - Score: [(15/10 × 0.5) + (8/10 × 0.5)] × 40 = **36 points**

3. **Adjusting** (30%):
   - Redo quiz sau poor performance: 3/3 failed quizzes
   - Access extra resources: 5 supplementary videos watched
   - Score: [(3/3 × 0.7) + (5/10 × 0.3)] × 30 = **25.5 points**

**SRL Index = 30 + 36 + 25.5 = 91.5/100 → "Highly self-regulated"**

---

### B2. Ví dụ KPI 3.4: Community of Inquiry Index

**Bối cảnh**: Khóa học "Quản trị Kinh doanh", 45 sinh viên

**Dữ liệu survey CoI** (5-point Likert scale):

1. **Cognitive Presence** (33%):
   - Triggering event: 4.2
   - Exploration: 4.0
   - Integration: 3.8
   - Resolution: 3.5
   - Average: (4.2 + 4.0 + 3.8 + 3.5) / 4 = **3.875**
   - Score: 3.875 × 0.33 = **1.28**

2. **Social Presence** (33%):
   - Open communication: 4.3
   - Group cohesion: 4.1
   - Emotional expression: 3.9
   - Average: (4.3 + 4.1 + 3.9) / 3 = **4.10**
   - Score: 4.10 × 0.33 = **1.35**

3. **Teaching Presence** (34%):
   - Design & organization: 4.5
   - Facilitation: 4.2
   - Direct instruction: 4.0
   - Average: (4.5 + 4.2 + 4.0) / 3 = **4.23**
   - Score: 4.23 × 0.34 = **1.44**

**CoI Index = 1.28 + 1.35 + 1.44 = 4.07/5.0 → "Strong community"**

---

### B3. Ví dụ KPI 1.10: Feedback Quality Score

**Bối cảnh**: Đánh giá chất lượng feedback của GV Trần Thị B

**Sample assignment feedback**:
```
Assignment: Essay về "Tác động của AI đến giáo dục"
Student: Phạm Văn C
Grade: 7/10

Feedback text (200 words):
"Bài viết của bạn có cấu trúc rõ ràng và dẫn chứng khá tốt. 
Tuy nhiên, phần phân tích còn hời hợt. Cụ thể:
- Thiếu so sánh giữa các quan điểm khác nhau (chỉ trình bày 1 góc nhìn)
- Chưa có ví dụ cụ thể từ nghiên cứu gần đây
- Kết luận chưa gắn với các đề xuất thực tế

Gợi ý cải thiện:
1. Đọc thêm bài báo của [tác giả X] về [chủ đề Y]
2. Bổ sung counterarguments để tăng tính thuyết phục
3. Lần sau, outline trước khi viết để đảm bảo logic

Điểm mạnh: Văn phong học thuật, trích dẫn đúng format APA.
Điểm cần cải thiện: Depth of analysis, critical thinking.

Nếu cần hướng dẫn thêm, book office hours với thầy nhé!"
```

**Tính điểm**:
1. **Độ dài phản hồi** (30%):
   - Word count: 200 words
   - Benchmark: ≥ 100 words = full points
   - Score: 30/30

2. **Có rubric chi tiết** (30%):
   - Rubric used: Có (với criteria: Structure, Evidence, Analysis, Writing)
   - Clear explanation: Có
   - Score: 30/30

3. **Có gợi ý cải tiến** (40%):
   - Specific suggestions: 3 items
   - Actionable: Có (reading list, structure advice)
   - Encouraging tone: Có
   - Score: 40/40

**Feedback Quality Score = (30 + 30 + 40) / 100 × 5 = 5.0/5.0 → "Excellent"**

---

## C. SQL QUERIES MẪU CHO MOODLE

### C1. KPI 2.1: Login Frequency

```sql
-- Tần suất đăng nhập của sinh viên trong 4 tuần gần nhất
SELECT 
    u.id AS user_id,
    u.firstname,
    u.lastname,
    COUNT(DISTINCT DATE(FROM_UNIXTIME(l.timecreated))) AS login_days,
    COUNT(*) AS total_logins,
    COUNT(*) / 4.0 AS logins_per_week
FROM 
    mdl_user u
JOIN 
    mdl_logstore_standard_log l ON u.id = l.userid
WHERE 
    l.action = 'loggedin'
    AND l.timecreated >= UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 4 WEEK))
    AND u.deleted = 0
GROUP BY 
    u.id
ORDER BY 
    logins_per_week DESC;
```

### C2. KPI 2.3: Resource Completion Rate

```sql
-- Tỷ lệ hoàn thành tài liệu của sinh viên trong 1 khóa học
SELECT 
    u.id,
    u.firstname,
    u.lastname,
    c.fullname AS course_name,
    COUNT(DISTINCT cm.id) AS total_resources,
    COUNT(DISTINCT cmc.coursemoduleid) AS completed_resources,
    (COUNT(DISTINCT cmc.coursemoduleid) / COUNT(DISTINCT cm.id) * 100) AS completion_rate
FROM 
    mdl_user u
JOIN 
    mdl_user_enrolments ue ON u.id = ue.userid
JOIN 
    mdl_enrol e ON ue.enrolid = e.id
JOIN 
    mdl_course c ON e.courseid = c.id
JOIN 
    mdl_course_modules cm ON c.id = cm.course
LEFT JOIN 
    mdl_course_modules_completion cmc ON cm.id = cmc.coursemoduleid AND u.id = cmc.userid AND cmc.completionstate > 0
WHERE 
    c.id = 123  -- Replace with actual course ID
    AND cm.completion > 0  -- Only count modules with completion tracking
GROUP BY 
    u.id, c.id
ORDER BY 
    completion_rate DESC;
```

### C3. KPI 1.9: On-time Grading Rate

```sql
-- Tỷ lệ chấm bài đúng hạn của giảng viên
SELECT 
    t.userid AS teacher_id,
    CONCAT(u.firstname, ' ', u.lastname) AS teacher_name,
    COUNT(*) AS total_submissions,
    SUM(CASE 
        WHEN g.timemodified <= (s.timemodified + a.gradingduedate) 
        THEN 1 ELSE 0 
    END) AS graded_on_time,
    (SUM(CASE 
        WHEN g.timemodified <= (s.timemodified + a.gradingduedate) 
        THEN 1 ELSE 0 
    END) / COUNT(*) * 100) AS on_time_rate
FROM 
    mdl_assign a
JOIN 
    mdl_assign_submission s ON a.id = s.assignment
JOIN 
    mdl_assign_grades g ON s.userid = g.userid AND s.assignment = g.assignment
JOIN 
    mdl_context ctx ON a.id = ctx.instanceid AND ctx.contextlevel = 70
JOIN 
    mdl_role_assignments ra ON ctx.id = ra.contextid
JOIN 
    mdl_role r ON ra.roleid = r.id
JOIN 
    mdl_user u ON ra.userid = u.id
WHERE 
    r.shortname = 'editingteacher'
    AND g.timemodified IS NOT NULL
    AND a.gradingduedate > 0  -- Only assignments with grading deadline
GROUP BY 
    t.userid
ORDER BY 
    on_time_rate DESC;
```

### C4. KPI 3.11: Retention Rate

```sql
-- Tỷ lệ retention của khóa học
SELECT 
    c.id AS course_id,
    c.fullname AS course_name,
    COUNT(DISTINCT ue.userid) AS enrolled_students,
    COUNT(DISTINCT CASE 
        WHEN l.timecreated >= UNIX_TIMESTAMP(DATE_SUB(FROM_UNIXTIME(c.enddate), INTERVAL 2 WEEK))
        THEN ue.userid 
    END) AS active_at_end,
    (COUNT(DISTINCT CASE 
        WHEN l.timecreated >= UNIX_TIMESTAMP(DATE_SUB(FROM_UNIXTIME(c.enddate), INTERVAL 2 WEEK))
        THEN ue.userid 
    END) / COUNT(DISTINCT ue.userid) * 100) AS retention_rate
FROM 
    mdl_course c
JOIN 
    mdl_enrol e ON c.id = e.courseid
JOIN 
    mdl_user_enrolments ue ON e.id = ue.enrolid
LEFT JOIN 
    mdl_logstore_standard_log l ON ue.userid = l.userid AND l.courseid = c.id
WHERE 
    c.enddate > 0
    AND ue.status = 0  -- Active enrolment
GROUP BY 
    c.id
ORDER BY 
    retention_rate DESC;
```

---

## D. xAPI STATEMENTS MAPPING

### D1. Activity Types cho Learning Analytics

```json
{
  "xAPI_verb_mapping": {
    "engagement": [
      "logged-in",
      "accessed",
      "viewed",
      "attended"
    ],
    "knowledge_construction": [
      "attempted",
      "answered",
      "completed",
      "passed",
      "failed"
    ],
    "collaboration": [
      "commented",
      "shared",
      "posted",
      "replied"
    ],
    "self_regulation": [
      "reviewed",
      "reflected",
      "set-goal",
      "tracked-progress"
    ]
  }
}
```

### D2. Sample xAPI Statement cho KPI 2.3

```json
{
  "actor": {
    "account": {
      "name": "student123",
      "homePage": "https://lms.university.edu.vn"
    }
  },
  "verb": {
    "id": "http://adlnet.gov/expapi/verbs/completed",
    "display": {"en-US": "completed"}
  },
  "object": {
    "id": "https://lms.university.edu.vn/course/42/module/video/intro",
    "definition": {
      "name": {"en-US": "Introduction to Python Programming"},
      "type": "http://adlnet.gov/expapi/activities/video"
    }
  },
  "result": {
    "completion": true,
    "duration": "PT12M30S"
  },
  "timestamp": "2026-01-16T10:30:00Z"
}
```

**Sử dụng**: Query LRS để đếm số "completed" verbs per student per course → tính completion rate

---

## E. DASHBOARD WIREFRAMES (Mô tả)

### E1. Student-Facing Dashboard Layout

```
┌─────────────────────────────────────────────────────┐
│  MY LEARNING DASHBOARD                              │
├──────────────┬──────────────────────────────────────┤
│ PROGRESS     │  Course: Introduction to AI          │
│              │  ━━━━━━━━━━━━━━ 78%                  │
│ 78%          │                                       │
│ On-track ✓   │  KPIs:                               │
│              │  • Login frequency: 4.2/week  🟢     │
│              │  • Completion rate: 85%       🟢     │
│              │  • On-time submissions: 90%   🟢     │
│              │  • Current GPA: 8.2/10        🟡     │
├──────────────┼──────────────────────────────────────┤
│ NEXT STEPS   │  UPCOMING DEADLINES                  │
│              │  📝 Assignment 5: Due in 3 days      │
│ ⚠ Complete   │  📊 Quiz 3: Opens tomorrow          │
│   Module 7   │  💬 Discussion Post: Due Friday      │
│              │                                       │
│ 📚 Review    │  RECOMMENDATIONS                      │
│   Feedback   │  • Review Module 5 (low quiz score)  │
│              │  • Join study group (improve collab) │
└──────────────┴──────────────────────────────────────┘
```

### E2. Instructor Dashboard Layout

```
┌─────────────────────────────────────────────────────┐
│  COURSE: MACHINE LEARNING (CS401)    Spring 2026    │
├──────────────┬──────────────────────────────────────┤
│ OVERVIEW     │  CLASS PERFORMANCE                    │
│              │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│ 45 students  │  Engagement: 82%   ▲ +5%            │
│ 3 at-risk ⚠  │  Avg GPA: 7.5      ━ 0%             │
│              │  Completion: 88%   ▼ -2%            │
├──────────────┼──────────────────────────────────────┤
│ MY KPIs      │  AT-RISK STUDENTS                     │
│              │  🔴 Nguyễn A: No login 7 days        │
│ Login: 6/wk  │  🟡 Trần B: Completion 45%           │
│ Response:18h │  🟡 Lê C: 3 late submissions         │
│ Grading: 95% │                                       │
│              │  ACTION ITEMS                         │
│ Student      │  ✉ Send reminder to Nguyễn A         │
│ Rating:4.6/5 │  📞 Schedule check-in with Trần B    │
└──────────────┴──────────────────────────────────────┘
```

---

## F. BẢNG NGƯỠNG ĐÁNH GIÁ TỔNG HỢP

### F1. Tổng hợp Ngưỡng theo Nhóm

| Nhóm KPI | Xuất sắc | Tốt | Cần Cải thiện |
|----------|----------|-----|---------------|
| **Giảng viên - Hoạt động** | | | |
| Login frequency | ≥5 lần/tuần | 3-4 | <3 |
| Time online | ≥8 giờ/tuần | 5-7 | <5 |
| Response time | ≤24h | 24-48h | >48h |
| **Người học - Engagement** | | | |
| Login frequency | ≥4 lần/tuần | 2-3 | <2 |
| Time on task | 6-10 giờ/tuần | 4-6 | <4 |
| Completion rate | ≥80% | 50-79% | <50% |
| **Kết quả - Achievement** | | | |
| Cumulative GPA | ≥8.5/10 | 7.0-8.4 | <7.0 |
| Course completion | ≥85% | 70-84% | <70% |
| On-time submission | ≥90% | 75-89% | <75% |
| **Môi trường - System** | | | |
| Uptime | ≥99.5% | 99.0-99.4% | <99.0% |
| Page load time | ≤2s | 2-4s | >4s |
| UX score (SUS) | ≥80/100 | 68-79 | <68 |

### F2. Color-Coding cho Dashboard

```
🟢 Green (Excellent): Vượt ngưỡng xuất sắc
🟡 Yellow (Warning): Trong khoảng "Tốt" nhưng cần theo dõi
🔴 Red (Alert): Dưới ngưỡng, cần can thiệp ngay
⚪ Gray: Không có dữ liệu
```

---

## G. CHECKLIST TRIỂN KHAI

### G1. Phase 1: Data Collection (2-4 tuần)

- [ ] Kiểm tra database schema của LMS
- [ ] Xác định tables và fields cần thiết cho từng KPI
- [ ] Test SQL queries trên sample data
- [ ] Thiết lập ETL pipeline (Extract-Transform-Load)
- [ ] Validate data quality (missing values, outliers)

### G2. Phase 2: KPI Calculation Engine (4-6 tuần)

- [ ] Implement calculation scripts (Python/R)
- [ ] Tạo scheduled jobs (cron/Airflow) cho automated updates
- [ ] Build data warehouse/data mart
- [ ] Test accuracy với manual calculations
- [ ] Optimizeperformance (indexing, caching)

### G3. Phase 3: Dashboard Development (6-8 tuần)

- [ ] Choose visualization tool (PowerBI/Tableau/Custom)
- [ ] Design wireframes (student, instructor, admin views)
- [ ] Develop interactive charts
- [ ] Implement filters và drill-down features
- [ ] Add real-time alerts/notifications
- [ ] User testing và iterative refinement

### G4. Phase 4: Deployment & Training (2-3 tuần)

- [ ] Deploy to production environment
- [ ] Create user guides/documentation
- [ ] Conduct training workshops for:
  - [ ] Students
  - [ ] Faculty
  - [ ] Administrators
- [ ] Gather initial feedback
- [ ] Monitor system performance

### G5. Phase 5: Continuous Improvement (Ongoing)

- [ ] Monthly review of KPI thresholds
- [ ] Quarterly validation studies (correlate KPIs với outcomes)
- [ ] Semi-annual user satisfaction survey
- [ ] Yearly benchmark comparison với previous year
- [ ] Research integration: Publish findings, present at conferences

---

## H. CASE STUDY: ÁP DỤNG TẠI MỘT TRƯỜNG ĐẠI HỌC

### H1. Bối cảnh

**Trường**: Đại học Công nghệ ABC  
**Quy mô**: 5,000 sinh viên, 300 giảng viên  
**LMS**: Moodle 4.1  
**Thời gian triển khai**: Học kỳ I, năm học 2025-2026

### H2. KPIs Ưu tiên (Top 10)

1. **KPI 2.6**: Course Completion Rate → Mục tiêu: Tăng từ 75% lên 85%
2. **KPI 2.1**: Student Login Frequency → Early warning system
3. **KPI 1.9**: On-time Grading → Faculty accountability
4. **KPI 3.11**: Retention Rate → Institutional KPI
5. **KPI 2.9**: Cumulative GPA → Academic success measure
6. **KPI 1.13**: Student evaluation → Teaching quality
7. **KPI 3.4**: Community of Inquiry → Course quality
8. **KPI 4.7**: User Experience Score → System improvement
9. **KPI 2.13**: Self-regulated learning → Study skill development
10. **KPI 4.1**: System Uptime → IT performance

### H3. Kết quả sau 1 học kỳ

**Thành công**:
- Course completion: 75% → 82% (+7%)
- At-risk identification: 85% accuracy (validated với actual dropout)
- Faculty satisfaction với grading dashboard: 4.2/5.0
- System uptime: 99.7%

**Thách thức**:
- Data quality issues: 15% records thiếu timestamps
- Faculty resistance: 20% chưa sử dụng dashboard thường xuyên
- Student privacy concerns: Cần clarify data usage policy

**Bài học**:
- Start small: 10 KPIs trước, rồi mở rộng
- Change management critical: Training + incentives
- Continuous communication: Monthly reports về impact

---

## I. CÔNG CỤ HỖ TRỢ

### I1. Phần mềm Phân tích

- **Python Libraries**: pandas, numpy, scikit-learn, matplotlib
- **R Packages**: tidyverse, caret, ggplot2
- **SQL Tools**: MySQL Workbench, DBeaver, DataGrip
- **BI Tools**: PowerBI, Tableau, Looker, Metabase

### I2. LMS Analytics Plugins

- **Moodle**: 
  - Configurable Reports
  - Analytics API (built-in Moodle 3.4+)
  - Learning Analytics Enrichment
- **Canvas**: Canvas Data 2 (CD2)
- **Blackboard**: Blackboard Analytics for Learn

### I3. Learning Record Store (LRS)

- **Learning Locker** (open source)
- **Watershed LRS** (commercial)
- **Veracity Learning** (xAPI focus)

---

## J. TÀI NGUYÊN BỔ SUNG

### J1. Template Files

- **Excel Template**: KPI Tracking Spreadsheet
- **PowerPoint**: Dashboard Presentation Template
- **Word**: KPI Documentation Template

### J2. Code Repositories (GitHub)

- Example: `https://github.com/learning-analytics/moodle-kpi-dashboard`
- Example: `https://github.com/canvas-analytics/student-success-predictor`

### J3. Online Communities

- **EDUCAUSE Learning Analytics Constituent Group**: https://www.educause.edu/
- **Society for Learning Analytics Research (SoLAR)**: https://www.solaresearch.org/
- **r/EducationalDataScience** (Reddit): https://www.reddit.com/r/EducationalDataScience/

---

[← Quay lại README](./README.md)
