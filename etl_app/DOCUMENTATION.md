# ETL Application Documentation (`etl_app`)

Tài liệu này mô tả luồng thực thi và quy tắc ánh xạ dữ liệu (mapping) từ xAPI Statements sang kho dữ liệu Star Schema (`xAPI_Analytics_DB`).

## 1. Luồng Thực thi (Execution Flow)

Ứng dụng ETL hoạt động theo cơ chế Batch Processing (Xử lý theo lô):

```mermaid
graph TD
    A[main.py] --> B[XAPIService]
    B -->|Fetch Statements| C[List[Dict]]
    C --> D[ETLManager]
    D --> E[DimensionProcessor]
    D --> F[FactProcessor]
    D --> G[BridgeProcessor]
    E -->|Save| H[(SQL Server)]
    F -->|Save| H
    G -->|Save| H
```

1.  **Khởi tạo**: `main.py` khởi tạo `DatabaseManager` để kết nối SQL Server và MySQL.
2.  **Lấy dữ liệu**: `XAPIService` gửi yêu cầu HTTP Basic Auth đến LRS. Hệ thống hỗ trợ **Phân trang (Pagination)**: tự động nhận diện link `more` để fetch toàn bộ dữ liệu cho đến khi đạt `limit`.
3.  **Điều phối (Orchestration)**: `ETLManager` thực hiện các bước:
    *   **Sắp xếp**: Toàn bộ statements được sắp xếp theo thời gian tăng dần (`timestamp ASC`) để đảm bảo logic tính toán phiên (Session) và trạng thái là chính xác.
    *   **Lặp**: Duyệt qua từng Statement để gọi các Processor:
    *   **DimensionProcessor**: Lưu thông tin vào các bảng Dim (Actor, Verb, Activity, Time...). Đảm bảo tính duy nhất.
    *   **FactProcessor**: Tính toán và lưu vào các bảng Fact. Xử lý các logic phức tạp như thời gian học (`duration`), kết quả thi (`quiz/question`).
    *   **BridgeProcessor**: Xây dựng quan hệ phân cấp (Closure Table) cho các hoạt động.
4.  **Hoàn tất**: Thực hiện `COMMIT` transaction để đảm bảo tính toàn vẹn dữ liệu và đóng kết nối.

---

## 2. Ánh xạ Chi tiết từng Trường (Field-level Mappings)

Tất cả các trường dữ liệu được trích xuất từ cấu trúc JSON của xAPI Statement hoặc được tính toán (Derived) trong quá trình xử lý.

### 2.1 DIMENSION TABLES (Bảng Chiều)

#### `dim_actor` (Thông tin người dùng)
| Trường SQL          | Nguồn gốc | Chi tiết ánh xạ      | Mô tả                                                          |
| :------------------ | :-------- | :------------------- | :------------------------------------------------------------- |
| **`actor_id`** (PK) | xAPI      | `actor.account.name` | Định danh duy nhất của người dùng (thường là Moodle Username). |
| `actor_name`        | xAPI      | `actor.name`         | Tên đầy đủ hiển thị của người dùng.                            |

#### `dim_interation_type` (Loại tương tác/Verb)
| Trường SQL                | Nguồn gốc | Chi tiết ánh xạ            | Mô tả                                                                                                                   |
| :------------------------ | :-------- | :------------------------- | :---------------------------------------------------------------------------------------------------------------------- |
| **`interaction_id`** (PK) | Derived   | `verb.id` (Last segment)   | Mã rút gọn từ URL hành động (vd: `completed`).                                                                          |
| `interaction_name`        | xAPI      | `verb.display['en']`       | Tên hành động thân thiện (vd: "Completed").                                                                             |
| `interaction_category`    | Derived   | Logic `DimensionProcessor` | Phân nhóm: `navigation` (start/viewed), `engagement` (receive), `assessment` (passed/failed), `completion` (completed). |

#### `dim_time` (Chiều thời gian)
| Trường SQL         | Nguồn gốc | Chi tiết ánh xạ             | Mô tả                                                                             |
| :----------------- | :-------- | :-------------------------- | :-------------------------------------------------------------------------------- |
| **`time_id`** (PK) | Derived   | `timestamp` (YYYYMMDDHH)    | Khóa đại diện cho giờ thực hiện hành động.                                        |
| `date`             | xAPI      | `timestamp` (Date)          | Ngày thực hiện (YYYY-MM-DD).                                                      |
| `week`             | Derived   | ISO Week Number             | Số thứ tự tuần trong năm.                                                         |
| `month`            | Derived   | ISO Month Number            | Số thứ tự tháng trong năm.                                                        |
| `day_of_week`      | Derived   | Day Name                    | Tên thứ trong tuần (Monday, Tuesday...).                                          |
| `time_slot`        | Derived   | `hour` mapping (Morning...) | `Morning` (5h-12h), `Afternoon` (12h-18h), `Evening` (18h-22h), `Night` (22h-5h). |

#### `dim_context` (Bối cảnh/Đăng ký)
| Trường SQL            | Nguồn gốc | Chi tiết ánh xạ           | Mô tả                                                                          |
| :-------------------- | :-------- | :------------------------ | :----------------------------------------------------------------------------- |
| **`context_id`** (PK) | Derived   | `Course ID`               | ID của khóa học trên Moodle (vd: "12"). Dùng làm bối cảnh chính thay cho UUID. |
| `course_id`           | Derived   | `extract_course_id` logic | Trích xuất Moodle Course ID từ URL hoặc metadata.                              |
| `section_id`          | xAPI      | `context.extensions`      | ID của chương/mục trong khóa học.                                              |
| `learning_path_id`    | xAPI      | `context.extensions`      | ID của lộ trình học tập tương ứng.                                             |

#### `dim_activity` (Danh mục Hoạt động)
| Trường SQL             | Nguồn gốc | Chi tiết ánh xạ          | Mô tả                                                        |
| :--------------------- | :-------- | :----------------------- | :----------------------------------------------------------- |
| **`activity_id`** (PK) | xAPI      | `object.id`              | URL định danh hoạt động (vd: `.../mod/quiz/view.php?id=10`). |
| `activity_type`        | xAPI      | `object.definition.type` | Loại hoạt động (vd: `.../activities/assessment`).            |
| `content_type`         | xAPI      | `object.definition.name` | Tên hoặc chuỗi mô tả nội dung hoạt động.                     |

#### `dim_learning_outcome` (Chuẩn đầu ra)
| Trường SQL            | Nguồn gốc     | Chi tiết ánh xạ                                            | Mô tả                                                                                                         |
| :-------------------- | :------------ | :--------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------ |
| **`outcome_id`** (PK) | xAPI + Moodle | `context.extensions` -> `mdl_competency.id` / `idnumber`   | ID của chuẩn đầu ra (lấy từ metadata xAPI để truy vấn Moodle).                                                |
| `outcome_code`        | Moodle        | `mdl_competency.idnumber` (hoặc `shortname`)               | Mã định danh chuẩn đầu ra (vd: LO1, LO2).                                                                     |
| `outcome_description` | Moodle        | `mdl_competency.description`                               | Mô tả chi tiết nội dung chuẩn đầu ra từ Moodle.                                                               |
| `outcome_level`       | Derived       | `mdl_competency.description` + `shortname` (Bloom mapping) | Phân loại Bloom (Tiếng Việt): `Nhớ` (Remember), `Hiểu` (Understand), `Vận dụng` (Apply)... dựa trên nội dung. |

---

### 2.2 FACT TABLES (Bảng Sự kiện)

#### `fact_statement` (Nhật ký Sự kiện chi tiết)
Lưu trữ toàn bộ lịch sử tương tác (Audit Trail) phục vụ truy vấn chi tiết.
| Trường SQL          | Nguồn gốc | Chi tiết ánh xạ               | Mô tả                                       |
| :------------------ | :-------- | :---------------------------- | :------------------------------------------ |
| **`event_id`** (PK) | xAPI      | `id` (Statement ID)           | ID duy nhất của mỗi statement.              |
| `actor_id` (FK)     | xAPI      | `actor.account.name`          | Liên kết người dùng.                        |
| `interaction_id`    | Derived   | `verb.id` (last segment)      | Mã định danh rút gọn của hành động.         |
| `context_id` (FK)   | Derived   | `Course ID`                   | ID khóa học (thay vì UUID).                 |
| `timestamp`         | xAPI      | `timestamp`                   | Thời gian thực phát sinh sự kiện (ISO8601). |
| `object_id`         | xAPI      | `object.id`                   | Target của hành động.                       |
| `result_flag`       | Derived   | `1` if result.success is True | Trạng thái thành công/đạt (0/1).            |
| `raw_duration_ms`   | xAPI      | `result.duration`             | Thời gian tương tác (ms).                   |
| `time_id` (FK)      | Derived   | `timestamp` (YYYYMMDDHH)      | Phân tích theo thời gian.                   |

#### `fact_session` (Phiên học tập)
Tổng hợp các hoạt động theo từng lần người dùng truy cập (Registration).
| Trường SQL            | Nguồn gốc | Chi tiết ánh xạ          | Mô tả                                                             |
| :-------------------- | :-------- | :----------------------- | :---------------------------------------------------------------- |
| **`session_id`** (PK) | xAPI      | `context.registration`   | ID duy nhất cho phiên (UUID).                                     |
| `start_time`          | Derived   | `min(timestamp)`         | Thời điểm bắt đầu phiên.                                          |
| `end_time`            | Derived   | `max(timestamp)`         | Thời điểm kết thúc hoặc hoạt động cuối cùng.                      |
| `session_duration`    | Derived   | `DATEDIFF(start, end)`   | Tổng thời gian phiên (tính bằng giây).                            |
| `entry_point`         | Derived   | Keyword extraction       | Tên ngắn của hoạt động đầu tiên (`quiz`, `course`, `page`, v.v.). |
| `session_type`        | Derived   | Constant                 | Mặc định là `learning`.                                           |
| `context_id` (FK)     | Derived   | `extract_course_id`      | Trích xuất Moodle Course ID làm bối cảnh phiên.                   |
| `time_id`             | Derived   | `timestamp` (YYYYMMDDHH) | Khóa thời gian (NămThángNgàyGiờ).                                 |

#### `fact_quiz` (Kết quả thi/kiểm tra)
| Trường SQL            | Nguồn gốc | Chi tiết ánh xạ            | Mô tả                                      |
| :-------------------- | :-------- | :------------------------- | :----------------------------------------- |
| **`quiz_attempt_id`** | xAPI      | `context.registration`     | Mã lần thử (Attempt ID).                   |
| `total_score`         | xAPI      | `result.score.raw`         | Điểm thô đạt được.                         |
| `isComplete`          | xAPI      | `result.completion`        | Trạng thái hoàn thành (0/1).               |
| `isSucceed`           | xAPI      | `result.success`           | Trạng thái đạt/trượt (0/1).                |
| `raw_duration_ms`     | xAPI      | `result.duration` (PT...S) | Thời gian làm bài quy đổi ra milliseconds. |
| `end_time`            | xAPI      | `timestamp` (Completed)    | Thời điểm nộp bài.                         |

#### `fact_question` (Chi tiết câu hỏi)
| Trường SQL        | Nguồn gốc | Chi tiết ánh xạ        | Mô tả                               |
| :---------------- | :-------- | :--------------------- | :---------------------------------- |
| **`question_id`** | xAPI      | `object.id`            | ID định danh câu hỏi.               |
| `quiz_attempt_id` | xAPI      | `context.registration` | Liên kết với bài thi (`fact_quiz`). |
| `selected_answer` | xAPI      | `result.response`      | Lựa chọn của người dùng.            |
| `is_correct`      | xAPI      | `result.success`       | Đúng (1) hoặc Sai (0).              |

#### `fact_activity` (Thống kê hành vi tổng hợp)
| Trường SQL            | Nguồn gốc | Chi tiết ánh xạ                 | Mô tả                                                       |
| :-------------------- | :-------- | :------------------------------ | :---------------------------------------------------------- |
| `activity_id`         | xAPI      | `object.id`                     | ID của hoạt động.                                           |
| `actor_id`            | xAPI      | `actor.account.name`            | ID người dùng.                                              |
| `activity_length`     | Moodle    | `mdl_quiz.timelimit` (Moodle)   | Thời lượng ước lượng của hoạt động.                         |
| `activity_type`       | xAPI      | `object.definition.type`        | Loại hoạt động (Quiz, Resource, v.v.).                      |
| `activity_difficulty` | Metadata  | Tự định nghĩa                   | Độ khó của hoạt động (Metadata).                            |
| `activity_order`      | Moodle    | `mdl_course_modules.section`    | Thứ tự hiển thị của hoạt động trong khóa học.               |
| `is_mandatory`        | Moodle    | `mdl_course_modules.completion` | Hoạt động bắt buộc (1) hay không (0).                       |
| `context_id`          | Derived   | `Course ID`                     | Liên kết khóa học làm bối cảnh.                             |
| `completion_status`   | Derived   | Logic `FactProcessor`           | Trạng thái: `In Progress`, `Completed`, `Passed`, `Failed`. |
| `time_spent`          | Derived   | `sum(result.duration)`          | Tổng thời gian tương tác (giây).                            |
| `attempt_count`       | Derived   | `COUNT(Statements)` (Quiz only) | Tổng số lần làm bài (áp dụng cho Quiz).                     |
| `time_id`             | Derived   | `timestamp` (YYYYMMDDHH)        | Khóa thời gian.                                             |

#### `fact_progress` (Tiến độ học tập)
| Trường SQL           | Nguồn gốc | Chi tiết ánh xạ            | Mô tả                                                  |
| :------------------- | :-------- | :------------------------- | :----------------------------------------------------- |
| `actor_id`           | xAPI      | `actor.account.name`       | ID người dùng.                                         |
| `outcome_id` (FK)    | xAPI      | `context.extensions`       | Liên kết mã chuẩn đầu ra (`dim_learning_outcome`).     |
| `progress_percent`   | Derived   | `result.completion` (100%) | Phần trăm tiến độ (thường gán 100 khi đạt completion). |
| `last_activity_time` | xAPI      | `timestamp`                | Thời điểm ghi nhận tiến độ cuối cùng.                  |

---

### 2.3 BRIDGE TABLES (Phân cấp)

#### `bridge_ActivityHierachy` (Closure Table)
*   **`ancestor_activity_id`**: ID của hoạt động cha (trích xuất từ `context.contextActivities.parent`).
*   **`descendant_activity`**: ID của hoạt động hiện tại (đối tượng chính của Statement).
*   **`is_direct_parent`**: `1` nếu là quan hệ trực hệ, `0` nếu là quan hệ tự tham chiếu (Self-reference).

---

## 3. Cách chạy Ứng dụng

Chạy từ thư mục gốc của dự án:

```powershell
python -m etl_app.main
```

Cấu hình được quản lý trong file `.env`.
