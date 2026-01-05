## 📄 Tài liệu mô tả mô hình dữ liệu phân tích xAPI & mục đích phân tích

Mô hình được xây dựng theo **Star Schema** với:

- **3 bảng Fact**: `fact_statement`, `fact_quiz`, `fact_question_answer`
- **5 bảng Chiều**: `dim_actor_account`, `dim_verb`, `dim_activity`, `activity_detail`, `dim_event_meta`
- **1 bảng Liên kết phân cấp**: `bridge_ActivityHierarchy`

Mục tiêu là chuẩn hóa dữ liệu xAPI/Moodle để phục vụ:

- Phân tích hành vi học tập theo nhiều cấp (learner, course, module, micro-content, question).
- Hỗ trợ các kỹ thuật Learning Analytics (descriptive, diagnostic, predictive, prescriptive).
- Làm nền cho dashboard, báo cáo tiến trình và engine gợi ý cá nhân hóa.

---

## I. ⭐️ Bảng Fact (Fact Tables)

Bảng Fact lưu **sự kiện/hành vi** và **chỉ số đo lường**, là nguồn chính cho Learning Analytics.

### 1. `fact_statement` – Sự kiện xAPI chung (Event Log)

**Mục đích phân tích**

- Là **bản ghi trung tâm** cho mọi event xAPI: xem nội dung, bắt đầu quiz, hoàn thành, review, v.v.
- Hỗ trợ các phân tích:
  - Dòng thời gian học tập của từng người học (learning path, time-on-task).
  - Tần suất/tần suất lặp lại hành vi theo **verb** (answered, completed, viewed,…).
  - Phân tích event theo course/module/micro-content thông qua `activity_id` và phân cấp activity.

**Cấu trúc bảng**

| Trường | Mô tả | Nguồn Dữ liệu & Logic Map | Loại Khóa |
|--------|-------|---------------------------|-----------|
| `statement_id` (scorm) | ID duy nhất của Statement (GUID). | Statement (LRS): id | PK |
| `actor_account_id` | ID người dùng Moodle. | Statement (LRS): actor.account.name | FK → dim_actor_account |
| `verb_id` | ID của hành động (URI). | Statement (LRS): verb.id | FK → dim_verb |
| `activity_id` | ID của đối tượng (Activity/Object) chính. | Statement (LRS): object.id | FK → dim_activity |
| `event_meta_id` | ID của metadata sự kiện Moodle. | Tính toán (ETL): Hash của event_name | FK → dim_event_meta |
| `moodle_module_id` | ID của module Moodle (CMID). | Tính toán (ETL): Trích xuất từ URL Activity (cmid=X hoặc id=Y). | Thuộc tính Fact |
| `registration_id` | ID phiên làm việc. | Statement (LRS): context.registration | Thuộc tính Fact |
| `event_timestamp` | Thời gian xảy ra sự kiện. | Statement (LRS): timestamp | Thuộc tính Fact |
| `stored_timestamp` | Thời gian LRS lưu trữ Statement. | Statement (LRS): stored | Thuộc tính Fact |
| `ingest_timestamp` | Thời gian ingest vào Data Warehouse. | Tính toán (ETL): GETDATE() khi insert vào DW | Thuộc tính Fact |

**Vai trò phân tích của các nhóm trường**

- **Khóa & liên kết** (`statement_id`, `actor_account_id`, `verb_id`, `activity_id`, `event_meta_id`):
  - Cho phép join đến các dimension để phân tích theo **người học, hành động, loại hoạt động, loại event Moodle**.
- **Ngữ cảnh hệ thống** (`moodle_module_id`, `registration_id`):
  - Phân tích phiên học (session), module cụ thể tạo ra event (liên kết Moodle DB nếu cần).
- **Thời gian** (`event_timestamp`, `stored_timestamp`, `ingest_timestamp`):
  - Phân tích dòng thời gian, độ trễ ingest, so sánh hành vi trước/sau can thiệp sư phạm.

---

### 2. `fact_quiz` – Chỉ số quiz/đánh giá (Quiz Attempt Level)

**Mục đích phân tích**

- Lưu thông tin ở **mức lần làm quiz (attempt)**, dùng để:
  - Tính **tỷ lệ hoàn thành**, **tỷ lệ đạt**, **điểm trung bình** theo quiz, module, course.
  - Phân tích **hành vi luyện tập**: số lần thử, thời gian làm, pattern review lại bài.
  - Làm input cho các mô hình **early warning** (phát hiện học viên có nguy cơ rớt).

**Cấu trúc bảng**

| Trường | Mô tả | Nguồn Dữ liệu & Logic Map | Loại Khóa |
|--------|-------|---------------------------|-----------|
| `statement_id` | ID Statement liên kết (thường là Statement completed). | Statement (LRS): id (của Statement completed/answered) | PK / FK → fact_statement |
| `duration` | Thời lượng làm bài. | Statement (LRS): result.duration | Chỉ số |
| `attempt_count` | Số lần thử quiz. | Tính toán (ETL): Đếm số Statement started cho cùng Actor/Activity/Quiz. Hoặc Moodle DB. | Chỉ số |
| `score_raw` | Điểm số đạt được (Raw hoặc Scaled). | Statement (LRS): result.score.raw/scaled | Chỉ số |
| `quiz_name` | Tên của Quiz. | LRS (ETL): Trích xuất từ contextActivities.parent[*].definition.name.en | Thuộc tính Fact |
| `is_completed` | Trạng thái hoàn thành (True/False). | Statement (LRS): result.completion | Chỉ số |
| `is_successful` (pass/fail) | Kết quả thành công/thất bại. | Statement (LRS): result.success | Chỉ số |
| `module_name` | Tên Module chứa Quiz. | LRS (ETL): Trích xuất từ contextActivities.parent[*].definition.name.en | Thuộc tính Fact |
| `is_reviewed` | Cờ đánh dấu Lần thử này đã được học viên xem lại. | Tính toán (ETL): TRUE nếu có Statement Received 'Review' với cùng attempt_activity_id | Chỉ số (Boolean) |
| `review_count` | Tổng số lần học viên xem lại bài này. | Tính toán (ETL): Đếm số Statement Received 'Review' | Chỉ số (Integer) |
| `last_review_timestamp` | Thời gian lần cuối cùng học viên xem lại bài. | Tính toán (ETL): Lấy timestamp mới nhất của Statement Received 'Review' | Thuộc tính Fact (Timestamp) |

**Vai trò phân tích của các nhóm trường**

- **Hiệu suất quiz** (`score_raw`, `is_completed`, `is_successful`):
  - Đo mức độ đạt yêu cầu, làm cơ sở cho đánh giá kết quả học tập và phân loại người học.
- **Hành vi luyện tập & nỗ lực** (`attempt_count`, `duration`):
  - Phân tích mức độ cố gắng (nhiều lần thử), chiến lược làm bài (thời gian dài/ngắn), phát hiện hành vi bất thường.
- **Hành vi ôn tập/review** (`is_reviewed`, `review_count`, `last_review_timestamp`):
  - Đo mức độ **tự điều chỉnh học tập** (self-regulated learning), hỗ trợ đề xuất thời điểm nhắc nhở ôn tập.
- **Ngữ cảnh quiz** (`quiz_name`, `module_name`):
  - Cho phép tổng hợp theo quiz/module/course, hiển thị thân thiện trên dashboard.

---

### 3. `fact_question_answer` – Phân tích cấp độ câu hỏi (Question Level)

**Mục đích phân tích**

- Ghi lại từng **lần trả lời 1 câu hỏi** của người học, là nguồn cho:
  - Phân tích **độ khó câu hỏi**, tỷ lệ đúng/sai theo câu, theo nhóm kỹ năng (micro-skill).
  - Xây dựng mô hình **Knowledge Tracing / Bayesian Skill Assessment** dựa trên chuỗi đúng/sai theo thời gian.
  - Phân tích pattern trả lời (response pattern) để hiểu lỗi phổ biến, hiểu nhầm khái niệm.

**Cấu trúc bảng**

| Trường | Mô tả | Nguồn Dữ liệu & Logic Map | Loại Khóa |
|--------|-------|---------------------------|-----------|
| `statement_id` (PK/FK) | ID của Statement answered. | Statement (LRS): id | PK / FK → fact_statement |
| `question_activity_id` (FK) | ID của câu hỏi (Object ID). | Statement (LRS): object.id | FK → dim_activity |
| `response_pattern` | Câu trả lời/phản hồi của học viên. | Statement (LRS): result.response | Thuộc tính Fact |
| `is_correct` | Kết quả đúng/sai cho câu hỏi đó. | Statement (LRS): result.success | Chỉ số (Boolean) |
| `correct_answer_pattern` | Mô hình câu trả lời đúng. | Statement (LRS): object.definition.correctResponsesPattern | Thuộc tính Fact |
| `score_raw` | Điểm số đạt được (nếu có). | Statement (LRS): result.score.raw | Chỉ số |
| `attempt_activity_id` (FK) | ID của lần thử Quiz chứa câu hỏi này. | Statement (LRS): Trích xuất từ contextActivities.parent (Attempt ID) | FK → dim_activity |

**Vai trò phân tích của các nhóm trường**

- **Liên kết & ngữ cảnh** (`question_activity_id`, `attempt_activity_id`):
  - Cho phép gắn câu hỏi vào **quiz/module/course** và vào **micro-skill** (thông qua mapping ở dimension).
- **Kết quả & độ khó** (`is_correct`, `score_raw`):
  - Tính độ khó câu hỏi (tỷ lệ đúng), phân loại câu hỏi tốt/xấu, đánh giá mastery theo kỹ năng.
- **Phân tích lỗi & hành vi** (`response_pattern`, `correct_answer_pattern`):
  - Phát hiện pattern sai thường gặp, thiết kế can thiệp hoặc nội dung bổ trợ phù hợp.

---

## II. 🌐 Bảng Chiều (Dimension Tables)

Bảng Chiều chứa thông tin mô tả tương đối ổn định, dùng để **lọc, nhóm, phân loại** dữ liệu Fact.

### 1. `dim_actor_account` – Học viên / Người dùng

**Mục đích phân tích**

- Lưu thông tin nhận diện người học để:
  - Tổng hợp chỉ số **theo learner** (tiến trình, kết quả, hành vi).
  - Kết nối với các hệ thống quản lý người học khác (LMS, SIS).

**Cấu trúc bảng**

| Trường | Mô tả | Nguồn Dữ liệu & Logic Map | Loại Khóa |
|--------|-------|---------------------------|-----------|
| `actor_account_id` (account name) | ID người dùng Moodle (dùng làm Khóa chính). | Statement (LRS): actor.account.name | PK |
| `actor_home_page` | URL cơ sở của LMS. | Statement (LRS): actor.account.homePage | Thuộc tính |
| `actor_name` | Tên hiển thị của học viên. | Statement (LRS): actor.name | Thuộc tính |

**Vai trò phân tích**

- Dùng làm **dimension People**, cho phép:
  - Lọc/slice số liệu theo từng người học hoặc nhóm người học.
  - Hiển thị tên thân thiện trên dashboard/báo cáo.

---

### 2. `dim_verb` – Hành động (xAPI Verb)

**Mục đích phân tích**

- Chuẩn hóa danh sách hành động (answered, completed, viewed, experienced, launched, reviewed, …) để:
  - Phân tích **loại hành vi học tập** (chủ động làm bài, chỉ xem lướt, xem lại, v.v.).
  - Xây dựng các chỉ số **engagement** theo verb.

**Cấu trúc bảng**

| Trường | Mô tả | Nguồn Dữ liệu & Logic Map | Loại Khóa |
|--------|-------|---------------------------|-----------|
| `verb_id` | URI định danh hành động (Verb ID). | Statement (LRS): verb.id | PK |
| `verb_display` | Tên hiển thị của Verb (ví dụ: 'answered'). | Statement (LRS): verb.display.en | Thuộc tính |

**Vai trò phân tích**

- Cho phép nhóm và so sánh:
  - Số lần **completed** vs **started** để tính completion rate.
  - Số lần **reviewed** để đo hành vi ôn tập.

---

### 3. `dim_activity` – Hoạt động / Đối tượng học tập

**Mục đích phân tích**

- Là **dimension trung tâm** mô tả mọi loại activity:
  - Course, module, quiz, question, resource, page, attempt, v.v.
- Kết hợp với `bridge_ActivityHierarchy` để phân tích dữ liệu theo **cấu trúc khóa học**.

**Cấu trúc bảng**

| Trường | Mô tả | Nguồn Dữ liệu & Logic Map | Loại Khóa |
|--------|-------|---------------------------|-----------|
| `activity_id` | ID duy nhất của hoạt động (URL/URI). | Statement (LRS): object.id (hoặc từ contextActivities.parent) | PK |
| `activity_url` | URL đầy đủ của hoạt động. | Statement (LRS): id | Thuộc tính |
| `is_category` | Cờ đánh dấu nếu là hoạt động nhóm/phân loại. | Statement (LRS): Dựa vào sự xuất hiện trong contextActivities.category | Thuộc tính |

**Vai trò phân tích**

- Cho phép:
  - Xem lại dữ liệu theo các **loại activity** (quiz vs resource vs question).
  - Kết nối sang Moodle (thông qua URL) để truy xuất thêm metadata nếu cần.

---

### 4. `activity_detail` – Chi tiết hoạt động (object definition)

**Mục đích phân tích**

- Bổ sung metadata chi tiết cho `dim_activity`, phục vụ:
  - Gắn hoạt động vào **course/module** (`moodle_course_id`, `moodle_module_id`).
  - Phân tích theo **loại activity** (assessment, attempt, resource…).
  - Gán hoạt động/câu hỏi với **micro-skill** (dựa trên type, tên, quy tắc mapping).

**Cấu trúc bảng**

| Trường | Mô tả | Nguồn Dữ liệu & Logic Map | Loại Khóa |
|--------|-------|---------------------------|-----------|
| `activity_id` | ID Activity, liên kết với dim_activity. | Statement (LRS): object.id | PK / FK → dim_activity |
| `activity_name` | Tên hoạt động/bài học. | Statement (LRS): object.definition.name.en | Thuộc tính |
| `activity_type_uri` | Loại hoạt động (ví dụ: assessment, attempt). | Statement (LRS): object.definition.type | Thuộc tính |
| `object_type` | Loại đối tượng xAPI (ví dụ: Activity). | Statement (LRS): object.objectType | Thuộc tính |
| `moodle_module_id` | ID Module Moodle (CMID). | Tính toán (ETL): Trích xuất từ URL trong activity_id. | Thuộc tính |
| `moodle_course_id` | ID Khóa học Moodle. | Tính toán (ETL): Trích xuất từ URL trong contextActivities.parent (ví dụ: course/view.php?id=X). | Thuộc tính |

**Vai trò phân tích**

- Cho phép:
  - Tổng hợp theo **tên hoạt động** và **course/module**.
  - Xây dựng các mapping **activity → skill**, **activity → loại nội dung** cho các mô hình khuyến nghị.

---

### 5. `dim_event_meta` – Metadata sự kiện Moodle

**Mục đích phân tích**

- Chuẩn hóa metadata event từ Moodle (event_name, module_name, action) để:
  - Nhận diện nguồn gốc event (mod_quiz, mod_forum, core_course, …).
  - Phân tích loại sự kiện ở **cấp Moodle** (viewed, submitted, attempted, created…).

**Cấu trúc bảng**

| Trường | Mô tả | Nguồn Dữ liệu & Logic Map | Loại Khóa |
|--------|-------|---------------------------|-----------|
| `event_meta_id` (hash(event_name)) | ID duy nhất (Hash của tên sự kiện). | Tính toán (ETL): Hash của context.extensions['.../info'].event_name | PK |
| `moodle_event_action` | Tên sự kiện Moodle rút gọn. | Tính toán (ETL): Phân tích từ event_name (phần cuối chuỗi). | Thuộc tính |
| `moodle_module_name` | Module Moodle sinh ra sự kiện. | Tính toán (ETL): Phân tích từ event_name (phần đầu chuỗi, ví dụ: mod_quiz). | Thuộc tính |

**Vai trò phân tích**

- Cho phép:
  - Lọc/slice dữ liệu theo **loại sự kiện Moodle**.
  - So sánh hành vi giữa các module khác nhau (quiz vs forum vs assignment).

---

## III. 🔗 Bảng liên kết `bridge_ActivityHierarchy` – Phân cấp hoạt động (Closure Table)

**Mục tiêu chính:** Cho phép truy vấn các mối quan hệ phân cấp ở bất kỳ cấp độ nào (ví dụ: Course → Quiz → Question) chỉ bằng **một lần JOIN**, thay vì phải JOIN nhiều lần qua các cấp trung gian.

### 1. Cấu trúc bảng (Thiết kế Closure Table – Path-based)

Thiết kế này lưu trữ tất cả các con đường từ mọi nút (node) đến mọi nút con (descendant).

| Trường | Mô tả | Nguồn Dữ liệu & Logic Map | Loại Khóa | Loại Dữ liệu |
|--------|-------|---------------------------|-----------|--------------|
| `ancestor_activity_id` | ID của hoạt động cấp cao hơn (Cha, Ông, v.v.). | Statement (LRS): ID từ mảng parent | PK / FK → dim_activity | String (URI) hoặc Integer (Surrogate Key) |
| `descendant_activity_id` | ID của hoạt động cấp thấp hơn (Con). | Statement (LRS): object.id | PK / FK → dim_activity | String (URI) hoặc Integer (Surrogate Key) |
| `path_length` | Khoảng cách/số cấp độ giữa ancestor và descendant (0 = chính nó, 1 = cha trực tiếp). | Tính toán (ETL) | Thuộc tính | Integer |
| `is_direct_parent` | TRUE nếu path_length = 1 (mối quan hệ Cha-Con trực tiếp). | Tính toán (ETL) | Thuộc tính | Boolean |

**Vai trò phân tích**

- Hỗ trợ các truy vấn kiểu:
  - Tất cả statement/quiz/câu hỏi thuộc **một khóa học hoặc module**.
  - Tổng hợp chỉ số từ level **câu hỏi → quiz → module → course** một cách linh hoạt.
- Là nền tảng để phân tích cấu trúc course, so sánh **hiệu quả của từng phần trong khóa học**.

### 2. 💡 Logic ETL để tạo bảng Closure Table

- **Bước 1: Ghi bản ghi tự tham chiếu**
  - Ghi `(Activity ID, Activity ID, 0)` cho mọi hoạt động (chiều dài = 0).
- **Bước 2: Ghi bản ghi quan hệ trực tiếp**
  - Lặp qua mảng `parent` trong Statement xAPI.
  - Ghi `(Parent ID, Child ID, 1)` và `is_direct_parent = TRUE`.
- **Bước 3: Ghi bản ghi quan hệ gián tiếp (closure logic)**
  - Nếu A là cha của B, B là cha của C → A cũng là cha của C (`path_length = 2`), và tương tự cho các cấp cao hơn.
- **Bước 4: Logic ETL Category (root)**
  - Luôn thêm Activity ID của LMS Category (ví dụ: `http://localhost/moodle`) làm root ancestor cho mọi activity, giúp truy vấn tổng thể toàn hệ thống.

### 3. Ưu điểm của thiết kế Closure Table

| Tính năng | Mô hình cha–con đơn cấp | Mô hình Closure Table |
|-----------|-------------------------|------------------------|
| **Truy vấn phân cấp** | Cần truy vấn đệ quy hoặc nhiều JOIN. | Chỉ cần một JOIN để tìm tất cả con cháu. |
| **Tìm hoạt động con** | Phức tạp (JOIN qua nhiều cấp). | Đơn giản: `WHERE ancestor_activity_id = [Course ID]`. |
| **Tốc độ đọc/phân tích** | Chậm hơn với dữ liệu lớn. | Tối ưu cho đọc/OLAP. |
| **Kích thước bảng** | Nhỏ hơn. | Lớn hơn (lưu mọi đường đi). |

### 4. Ví dụ truy vấn phân tích

**Mục tiêu:** Lấy tất cả các `fact_statement` thuộc một khóa học có ID=2.

```sql
SELECT
    fs.* -- Statement ID, Verb ID, Actor ID, Activity ID, ...
FROM
    fact_statement fs
INNER JOIN
    bridge_ActivityHierarchy bridge
    ON fs.activity_id = bridge.descendant_activity_id
WHERE
    bridge.ancestor_activity_id = 'http://localhost/moodle/course/view.php?id=2'
    AND bridge.path_length > 0;
```

---

## IV. Gợi ý truy vấn cho Dashboard (Monitor & Analytics)

Dưới đây là các truy vấn SQL mẫu để xây dựng dashboard giám sát và phân tích kết quả từ góc độ Giáo viên, Học sinh và Quản trị viên.

### 1. Cho Giáo viên (Teacher Perspective)

- **Top 5 câu hỏi khó nhất trong khóa học:** Tìm các câu hỏi có tỷ lệ trả lời đúng thấp nhất để giáo viên có kế hoạch giải đáp hoặc điều chỉnh nội dung.

```sql
SELECT TOP 5
    ad.activity_name,
    COUNT(fqa.statement_id) as total_attempts,
    SUM(CAST(fqa.is_correct AS INT)) * 100.0 / COUNT(fqa.statement_id) as success_rate
FROM fact_question_answer fqa
JOIN activity_detail ad ON fqa.question_activity_id = ad.activity_id
JOIN bridge_ActivityHierarchy bridge ON fqa.question_activity_id = bridge.descendant_activity_id
WHERE bridge.ancestor_activity_id = 'http://171.246.224.10:81/moodle/course/view.php?id=7' -- Thay ID khóa học
GROUP BY ad.activity_name
ORDER BY success_rate ASC;
```

- **Xếp hạng mức độ tương tác của học sinh:** Xác định những học sinh tích cực nhất hoặc ít tương tác nhất.

```sql
SELECT 
    da.actor_name,
    COUNT(DISTINCT CAST(fs.event_timestamp AS DATE)) as active_days,
    COUNT(fs.statement_id) as total_interactions
FROM fact_statement fs
JOIN dim_actor_account da ON fs.actor_account_id = da.actor_account_id
GROUP BY da.actor_name
ORDER BY active_days DESC, total_interactions DESC;
```

### 2. Cho Học sinh (Student Perspective)

- **Tiến độ hoàn thành khóa học (%):** Tính toán xem học sinh đã hoàn thành bao nhiêu phần trăm các hoạt động trong một khóa học cụ thể.

```sql
WITH CourseActivities AS (
    -- Lấy tổng số hoạt động trong khóa học (loại trừ chính khóa học)
    SELECT COUNT(DISTINCT descendant_activity_id) as total_count
    FROM bridge_ActivityHierarchy
    WHERE ancestor_activity_id = 'http://171.246.224.10:81/moodle/course/view.php?id=7'
      AND path_length > 0
),
CompletedActivities AS (
    -- Lấy số hoạt động học sinh đã hoàn thành
    SELECT COUNT(DISTINCT fs.activity_id) as completed_count
    FROM fact_statement fs
    JOIN dim_verb dv ON fs.verb_id = dv.verb_id
    JOIN bridge_ActivityHierarchy bridge ON fs.activity_id = bridge.descendant_activity_id
    WHERE fs.actor_account_id = '3'
      AND bridge.ancestor_activity_id = 'http://171.246.224.10:81/moodle/course/view.php?id=7'
      AND dv.verb_display IN ('completed', 'passed')
)
SELECT 
    completed_count, 
    total_count,
    CAST(completed_count AS FLOAT) * 100 / total_count as completion_percentage
FROM CompletedActivities, CourseActivities;
```

- **Xu hướng điểm số qua các bài đánh giá:** Theo dõi sự tiến bộ của bản thân theo thời gian.

```sql
SELECT 
    fq.quiz_name,
    fs.event_timestamp,
    fq.score_raw,
    fq.is_successful
FROM fact_quiz fq
JOIN fact_statement fs ON fq.statement_id = fs.statement_id
WHERE fs.actor_account_id = '3'
ORDER BY fs.event_timestamp ASC;
```

- **Phân tích nỗ lực (Sơ đồ nỗ lực vs Kết quả):** Xem mối quan hệ giữa số lần thử và điểm số đạt được để điều chỉnh cách học.

```sql
SELECT 
    fq.quiz_name,
    fq.attempt_count,
    fq.score_raw,
    fq.duration / 60.0 as duration_minutes
FROM fact_quiz fq
JOIN fact_statement fs ON fq.statement_id = fs.statement_id
WHERE fs.actor_account_id = '3'
ORDER BY fq.attempt_count DESC;
```

- **Gợi ý nội dung cần ôn tập:** Danh sách các bài quiz có điểm thấp hoặc trạng thái "failed" cần được học sinh ưu tiên xem lại.

```sql
SELECT 
    fq.quiz_name,
    fq.score_raw,
    fq.last_review_timestamp,
    CASE 
        WHEN fq.is_reviewed = 0 THEN N'Chưa ôn tập'
        ELSE N'Đã ôn tập ' + CAST(fq.review_count AS NVARCHAR) + N' lần'
    END as review_status
FROM fact_quiz fq
JOIN fact_statement fs ON fq.statement_id = fs.statement_id
WHERE fs.actor_account_id = '3'
  AND (fq.is_successful = 0 OR fq.score_raw < 50)
ORDER BY fq.score_raw ASC;
```

- **Thống kê thời gian học tập tập trung:** Tổng thời gian thực tế dành cho các hoạt động chính trong khóa học.

```sql
SELECT 
    ad.activity_name,
    ISNULL(SUM(fq.duration), 0) / 60 as total_minutes_spent
FROM fact_quiz fq
JOIN fact_statement fs ON fq.statement_id = fs.statement_id
JOIN activity_detail ad ON fs.activity_id = ad.activity_id
WHERE fs.actor_account_id = '3'
GROUP BY ad.activity_name
HAVING SUM(fq.duration) > 0; -- Chỉ lấy những hoạt động thực sự có tốn thời gian
```

### 3. Giám sát hệ thống (System Monitoring)

- **Số lượng sự kiện thu thập theo thời gian (7 ngày gần nhất):** Kiểm tra xem dữ liệu có được đẩy vào đều đặn không.

```sql
SELECT 
    CAST(event_timestamp AS DATE) as activity_date,
    COUNT(*) as total_events
FROM fact_statement
WHERE event_timestamp >= DATEADD(day, -7, GETDATE())
GROUP BY CAST(event_timestamp AS DATE)
ORDER BY activity_date;
```

- **Thống kê các module Moodle đang sinh ra nhiều sự kiện nhất:**

```sql
SELECT 
    dem.moodle_module_name,
    dem.moodle_event_action,
    COUNT(*) as event_count
FROM fact_statement fs
JOIN dim_event_meta dem ON fs.event_meta_id = dem.event_meta_id
GROUP BY dem.moodle_module_name, dem.moodle_event_action
ORDER BY event_count DESC;
```

---

## V. Tóm tắt vai trò mô hình dữ liệu với Learning Analytics

- **Fact tables** cung cấp dữ liệu chi tiết ở 3 mức: **event**, **quiz attempt**, **question answer**, phù hợp cho cả báo cáo mô tả lẫn mô hình dự đoán.
- **Dimension tables** chuẩn hóa người học, hành vi (verb), hoạt động, metadata sự kiện, tạo nền cho việc slice/dice dữ liệu theo nhiều chiều phân tích.
- **Bridge table** cho phép “trải phẳng” cấu trúc phân cấp course/module/micro-content, giúp truy vấn và tổng hợp ở mọi cấp độ.
- Trên nền mô hình này có thể xây dựng:
  - Dashboard tiến trình & chất lượng học tập.
  - Phân tích kỹ năng (micro-skill) dựa trên dữ liệu `fact_question_answer`.
  - Mô hình cảnh báo sớm và engine gợi ý nội dung/hoạt động học tập cá nhân hóa.
