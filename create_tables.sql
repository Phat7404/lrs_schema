-- =============================================
-- Script tạo bảng cho Mô hình Dữ liệu Phân tích xAPI
-- Star Schema: 3 Bảng Fact, 5 Bảng Chiều, 1 Bảng Liên kết
-- SQL Server
-- =============================================

USE [master];
GO

-- Tạo Database (nếu chưa có)
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'moodle_datawarehouse')
BEGIN
    CREATE DATABASE [moodle_datawarehouse];
END
GO

USE [moodle_datawarehouse];
GO

-- =============================================
-- II. BẢNG CHIỀU (Dimension Tables)
-- =============================================

-- 1. dim_actor_account (Học viên)
IF OBJECT_ID('dim_actor_account', 'U') IS NOT NULL
    DROP TABLE dim_actor_account;
GO

CREATE TABLE dim_actor_account (
    actor_account_id NVARCHAR(255) NOT NULL,  -- ID người dùng Moodle (account name)
    actor_home_page NVARCHAR(500),            -- URL cơ sở của LMS
    actor_name NVARCHAR(255),                 -- Tên hiển thị của học viên
    CONSTRAINT PK_dim_actor_account PRIMARY KEY (actor_account_id)
);
GO

-- 2. dim_verb (Hành động)
IF OBJECT_ID('dim_verb', 'U') IS NOT NULL
    DROP TABLE dim_verb;
GO

CREATE TABLE dim_verb (
    verb_id NVARCHAR(500) NOT NULL,           -- URI định danh hành động (Verb ID)
    verb_display NVARCHAR(255),               -- Tên hiển thị của Verb (ví dụ: 'answered')
    CONSTRAINT PK_dim_verb PRIMARY KEY (verb_id)
);
GO

-- 3. dim_activity (Hoạt động/Đối tượng)
IF OBJECT_ID('dim_activity', 'U') IS NOT NULL
    DROP TABLE dim_activity;
GO

CREATE TABLE dim_activity (
    activity_id NVARCHAR(500) NOT NULL,       -- ID duy nhất của hoạt động (URL/URI)
    activity_url NVARCHAR(1000),              -- URL đầy đủ của hoạt động
    is_category BIT DEFAULT 0,                -- Cờ đánh dấu nếu là hoạt động nhóm/phân loại
    CONSTRAINT PK_dim_activity PRIMARY KEY (activity_id)
);
GO

-- 4. activity_detail (Chi tiết Hoạt động)
IF OBJECT_ID('activity_detail', 'U') IS NOT NULL
    DROP TABLE activity_detail;
GO

CREATE TABLE activity_detail (
    activity_id NVARCHAR(500) NOT NULL,       -- ID Activity, liên kết với dim_activity
    activity_name NVARCHAR(500),              -- Tên hoạt động/bài học
    activity_type_uri NVARCHAR(500),          -- Loại hoạt động (ví dụ: assessment, attempt)
    object_type NVARCHAR(100),                 -- Loại đối tượng xAPI (ví dụ: Activity)
    moodle_module_id INT,                      -- ID Module Moodle (CMID)
    moodle_course_id INT,                      -- ID Khóa học Moodle
    CONSTRAINT PK_activity_detail PRIMARY KEY (activity_id),
    CONSTRAINT FK_activity_detail_dim_activity FOREIGN KEY (activity_id) 
        REFERENCES dim_activity(activity_id)
);
GO

-- 5. dim_event_meta (Metadata Sự kiện Moodle)
IF OBJECT_ID('dim_event_meta', 'U') IS NOT NULL
    DROP TABLE dim_event_meta;
GO

CREATE TABLE dim_event_meta (
    event_meta_id NVARCHAR(255) NOT NULL,     -- ID duy nhất (Hash của tên sự kiện)
    moodle_event_action NVARCHAR(255),        -- Tên sự kiện Moodle rút gọn
    moodle_module_name NVARCHAR(255),         -- Module Moodle sinh ra sự kiện
    CONSTRAINT PK_dim_event_meta PRIMARY KEY (event_meta_id)
);
GO

-- =============================================
-- I. BẢNG FACT (Fact Tables)
-- =============================================

-- 1. fact_statement (Sự kiện xAPI Chung)
IF OBJECT_ID('fact_statement', 'U') IS NOT NULL
    DROP TABLE fact_statement;
GO

CREATE TABLE fact_statement (
    statement_id UNIQUEIDENTIFIER NOT NULL,   -- ID duy nhất của Statement (GUID)
    actor_account_id NVARCHAR(255) NOT NULL,  -- ID người dùng Moodle
    verb_id NVARCHAR(500) NOT NULL,           -- ID của hành động (URI)
    activity_id NVARCHAR(500) NOT NULL,       -- ID của đối tượng (Activity/Object) chính
    event_meta_id NVARCHAR(255),              -- ID của metadata sự kiện Moodle
    moodle_module_id INT,                     -- ID của module Moodle (CMID)
    registration_id UNIQUEIDENTIFIER,         -- ID phiên làm việc
    event_timestamp DATETIME2,                -- Thời gian xảy ra sự kiện
    stored_timestamp DATETIME2,               -- Thời gian LRS lưu trữ Statement
    ingest_timestamp DATETIME2 DEFAULT GETDATE(), -- Thời gian ingest vào Data Warehouse
    CONSTRAINT PK_fact_statement PRIMARY KEY (statement_id),
    CONSTRAINT FK_fact_statement_actor FOREIGN KEY (actor_account_id) 
        REFERENCES dim_actor_account(actor_account_id),
    CONSTRAINT FK_fact_statement_verb FOREIGN KEY (verb_id) 
        REFERENCES dim_verb(verb_id),
    CONSTRAINT FK_fact_statement_activity FOREIGN KEY (activity_id) 
        REFERENCES dim_activity(activity_id),
    CONSTRAINT FK_fact_statement_event_meta FOREIGN KEY (event_meta_id) 
        REFERENCES dim_event_meta(event_meta_id)
);
GO

-- 2. fact_quiz (Chỉ số Quiz/Đánh giá)
IF OBJECT_ID('fact_quiz', 'U') IS NOT NULL
    DROP TABLE fact_quiz;
GO

CREATE TABLE fact_quiz (
    statement_id UNIQUEIDENTIFIER NOT NULL,   -- ID Statement liên kết
    duration INT,                             -- Thời lượng làm bài (giây)
    attempt_count INT,                        -- Số lần thử quiz
    score_raw DECIMAL(10,2),                  -- Điểm số đạt được (Raw hoặc Scaled)
    quiz_name NVARCHAR(500),                  -- Tên của Quiz
    is_completed BIT,                         -- Trạng thái hoàn thành (True/False)
    is_successful BIT,                        -- Kết quả thành công/thất bại (pass/fail)
    module_name NVARCHAR(500),                -- Tên Module chứa Quiz
    is_reviewed BIT DEFAULT 0,                -- Cờ đánh dấu Lần thử này đã được học viên xem lại
    review_count INT DEFAULT 0,               -- Tổng số lần học viên xem lại bài này
    last_review_timestamp DATETIME2,          -- Thời gian lần cuối cùng học viên xem lại bài
    CONSTRAINT PK_fact_quiz PRIMARY KEY (statement_id),
    CONSTRAINT FK_fact_quiz_statement FOREIGN KEY (statement_id) 
        REFERENCES fact_statement(statement_id)
);
GO

-- 3. fact_question_answer (Phân tích cấp độ Câu hỏi)
IF OBJECT_ID('fact_question_answer', 'U') IS NOT NULL
    DROP TABLE fact_question_answer;
GO

CREATE TABLE fact_question_answer (
    statement_id UNIQUEIDENTIFIER NOT NULL,   -- ID của Statement answered
    question_activity_id NVARCHAR(500) NOT NULL, -- ID của câu hỏi (Object ID)
    response_pattern NVARCHAR(MAX),           -- Câu trả lời/phản hồi của học viên
    is_correct BIT,                           -- Kết quả đúng/sai cho câu hỏi đó
    correct_answer_pattern NVARCHAR(MAX),      -- Mô hình câu trả lời đúng
    score_raw DECIMAL(10,2),                  -- Điểm số đạt được (nếu có)
    attempt_activity_id NVARCHAR(500),        -- ID của lần thử Quiz chứa câu hỏi này
    CONSTRAINT PK_fact_question_answer PRIMARY KEY (statement_id),
    CONSTRAINT FK_fact_question_answer_statement FOREIGN KEY (statement_id) 
        REFERENCES fact_statement(statement_id),
    CONSTRAINT FK_fact_question_answer_question FOREIGN KEY (question_activity_id) 
        REFERENCES dim_activity(activity_id),
    CONSTRAINT FK_fact_question_answer_attempt FOREIGN KEY (attempt_activity_id) 
        REFERENCES dim_activity(activity_id)
);
GO

-- =============================================
-- III. BẢNG LIÊN KẾT (Bridge Table)
-- =============================================

-- bridge_ActivityHierarchy (Phân cấp Hoạt động - Closure Table)
IF OBJECT_ID('bridge_ActivityHierarchy', 'U') IS NOT NULL
    DROP TABLE bridge_ActivityHierarchy;
GO

CREATE TABLE bridge_ActivityHierarchy (
    ancestor_activity_id NVARCHAR(500) NOT NULL,   -- ID của hoạt động cấp cao hơn (Cha, Ông, v.v.)
    descendant_activity_id NVARCHAR(500) NOT NULL, -- ID của hoạt động cấp thấp hơn (Con)
    path_length INT NOT NULL,                      -- Khoảng cách/số cấp độ giữa ancestor và descendant
    is_direct_parent BIT DEFAULT 0,                -- TRUE nếu path_length = 1 (mối quan hệ Cha-Con trực tiếp)
    CONSTRAINT PK_bridge_ActivityHierarchy PRIMARY KEY (ancestor_activity_id, descendant_activity_id),
    CONSTRAINT FK_bridge_ancestor FOREIGN KEY (ancestor_activity_id) 
        REFERENCES dim_activity(activity_id),
    CONSTRAINT FK_bridge_descendant FOREIGN KEY (descendant_activity_id) 
        REFERENCES dim_activity(activity_id),
    CONSTRAINT CHK_path_length CHECK (path_length >= 0)
);
GO

/*
Logic ETL cho bridge_ActivityHierarchy (Closure Table):

Bước 1: Ghi bản ghi Tự tham chiếu
- Ghi bản ghi (Activity ID, Activity ID, 0) cho mọi hoạt động (chiều dài = 0).

Bước 2: Ghi bản ghi Quan hệ Trực tiếp
- Lặp qua mảng parent trong Statement xAPI.
- Ghi (Parent ID, Child ID, 1) và is_direct_parent = TRUE.

Bước 3: Ghi bản ghi Quan hệ Gián tiếp (Closure Logic)
- Sau khi có các quan hệ trực tiếp, sử dụng SQL/ETL để tạo các quan hệ gián tiếp:
  - Nếu A là Cha của B, và B là Cha của C, thì A cũng là Cha của C (chiều dài = 2).
  - Lặp lại logic này cho tất cả các cấp độ phân cấp.

Bước 4: Logic ETL Category (MỚI)
- Luôn thêm Activity ID của LMS Category (http://localhost/moodle) vào mảng Ancestor 
  (với path_length cao nhất) cho mọi Statement được xử lý.
- Đảm bảo tất cả Activity đều có Root Node là LMS/Category, giúp truy vấn tổng thể theo hệ thống.
*/

-- =============================================
-- TẠO INDEX ĐỂ TỐI ƯU HIỆU SUẤT
-- =============================================

-- Index cho fact_statement
CREATE NONCLUSTERED INDEX IX_fact_statement_actor ON fact_statement(actor_account_id);
CREATE NONCLUSTERED INDEX IX_fact_statement_verb ON fact_statement(verb_id);
CREATE NONCLUSTERED INDEX IX_fact_statement_activity ON fact_statement(activity_id);
CREATE NONCLUSTERED INDEX IX_fact_statement_timestamp ON fact_statement(event_timestamp);
CREATE NONCLUSTERED INDEX IX_fact_statement_ingest_timestamp ON fact_statement(ingest_timestamp);

-- Index cho fact_quiz
CREATE NONCLUSTERED INDEX IX_fact_quiz_completed ON fact_quiz(is_completed);
CREATE NONCLUSTERED INDEX IX_fact_quiz_successful ON fact_quiz(is_successful);
CREATE NONCLUSTERED INDEX IX_fact_quiz_reviewed ON fact_quiz(is_reviewed);
CREATE NONCLUSTERED INDEX IX_fact_quiz_review_timestamp ON fact_quiz(last_review_timestamp);

-- Index cho fact_question_answer
CREATE NONCLUSTERED INDEX IX_fact_question_answer_question ON fact_question_answer(question_activity_id);
CREATE NONCLUSTERED INDEX IX_fact_question_answer_attempt ON fact_question_answer(attempt_activity_id);
CREATE NONCLUSTERED INDEX IX_fact_question_answer_correct ON fact_question_answer(is_correct);

-- Index cho bridge_ActivityHierarchy (quan trọng cho truy vấn phân cấp)
CREATE NONCLUSTERED INDEX IX_bridge_ancestor ON bridge_ActivityHierarchy(ancestor_activity_id);
CREATE NONCLUSTERED INDEX IX_bridge_descendant ON bridge_ActivityHierarchy(descendant_activity_id);
CREATE NONCLUSTERED INDEX IX_bridge_path_length ON bridge_ActivityHierarchy(path_length);
CREATE NONCLUSTERED INDEX IX_bridge_direct_parent ON bridge_ActivityHierarchy(is_direct_parent);

-- Index cho activity_detail
CREATE NONCLUSTERED INDEX IX_activity_detail_course ON activity_detail(moodle_course_id);
CREATE NONCLUSTERED INDEX IX_activity_detail_module ON activity_detail(moodle_module_id);

GO

PRINT 'Da tao thanh cong tat ca cac bang cho mo hinh du lieu xAPI Analytics!';
GO

