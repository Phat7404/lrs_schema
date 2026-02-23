-- =============================================
-- SQL Server Schema for xAPI Data Analytics (Star Schema)
-- Generated based on Draw.io diagram
-- =============================================

USE [master];
GO

-- Create Database if it doesn't exist
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'xAPI_Analytics_DB')
BEGIN
    CREATE DATABASE [xAPI_Analytics_DB];
END
GO

USE [xAPI_Analytics_DB];
GO

-- =============================================
-- I. DIMENSION TABLES
-- =============================================

-- 1. dim_actor (Thông tin người dùng)
IF OBJECT_ID('dim_actor', 'U') IS NOT NULL DROP TABLE dim_actor;
CREATE TABLE dim_actor (
    actor_id NVARCHAR(255) NOT NULL,           -- xAPI.actor.account
    actor_name NVARCHAR(500),                  -- xAPI.actor.name
    CONSTRAINT PK_dim_actor PRIMARY KEY (actor_id)
);
GO

-- 2. dim_interation_type (Loại tương tác/Verb)
IF OBJECT_ID('dim_interation_type', 'U') IS NOT NULL DROP TABLE dim_interation_type;
CREATE TABLE dim_interation_type (
    interaction_id NVARCHAR(500) NOT NULL,     -- xAPI.verb.id
    interaction_name NVARCHAR(255),            -- xAPI.verb.display
    interaction_category NVARCHAR(255),        -- Tự phân loại
    CONSTRAINT PK_dim_interation_type PRIMARY KEY (interaction_id)
);
GO

-- 3. dim_time (Chiều thời gian)
IF OBJECT_ID('dim_time', 'U') IS NOT NULL DROP TABLE dim_time;
CREATE TABLE dim_time (
    time_id INT NOT NULL,                      -- Surrogate Key (YYYYMMDD) or ID
    [date] DATE,
    [week] INT,
    [month] INT,
    day_of_week NVARCHAR(50),
    time_slot NVARCHAR(50),                    -- Morning / Afternoon / Evening
    ingest_timestamp DATETIME2 DEFAULT GETDATE(),
    CONSTRAINT PK_dim_time PRIMARY KEY (time_id)
);
GO

-- 4. dim_context (Bối cảnh học tập - Moodle Context)
IF OBJECT_ID('dim_context', 'U') IS NOT NULL DROP TABLE dim_context;
CREATE TABLE dim_context (
    context_id NVARCHAR(255) NOT NULL,         -- xAPI.context
    course_id INT,                             -- Moodle Course ID
    section_id INT,                            -- Moodle Section ID
    learning_path_id INT,                      -- Moodle Learning Path ID
    is_interrupt BIT DEFAULT 0,                -- (Derived)
    CONSTRAINT PK_dim_context PRIMARY KEY (context_id)
);
GO

-- 5. dim_activity (Danh mục Hoạt động)
IF OBJECT_ID('dim_activity', 'U') IS NOT NULL DROP TABLE dim_activity;
CREATE TABLE dim_activity (
    activity_id NVARCHAR(500) NOT NULL,        -- xAPI.object.id
    activity_type NVARCHAR(255),               -- Moodle Activity Type
    content_type NVARCHAR(255),                -- Moodle Content Type
    interactivity_level INT,                   -- Tự định nghĩa
    CONSTRAINT PK_dim_activity PRIMARY KEY (activity_id)
);
GO

-- 6. dim_learning_outcome (Chuẩn đầu ra)
IF OBJECT_ID('dim_learning_outcome', 'U') IS NOT NULL DROP TABLE dim_learning_outcome;
CREATE TABLE dim_learning_outcome (
    outcome_id NVARCHAR(255) NOT NULL,         -- Moodle Outcome ID
    outcome_code NVARCHAR(100),                -- LO Code
    outcome_description NVARCHAR(MAX),         -- Syllabus description
    outcome_level NVARCHAR(100),               -- Bloom taxonomy level
    CONSTRAINT PK_dim_learning_outcome PRIMARY KEY (outcome_id)
);
GO

-- =============================================
-- II. FACT TABLES
-- =============================================

-- 1. fact_statement (Sự kiện xAPI chi tiết)
IF OBJECT_ID('fact_statement', 'U') IS NOT NULL DROP TABLE fact_statement;
CREATE TABLE fact_statement (
    event_id NVARCHAR(255) NOT NULL,           -- xAPI.id
    actor_id NVARCHAR(255) NOT NULL,           -- xAPI.actor
    interaction_id NVARCHAR(500) NOT NULL,     -- xAPI.verb.id
    context_id NVARCHAR(255) NOT NULL,         -- xAPI.context
    [timestamp] DATETIME2,                     -- xAPI.timestamp
    object_type NVARCHAR(100),                 -- xAPI.object.objectType
    object_id NVARCHAR(500),                   -- xAPI.object.id
    result_flag BIT,                           -- (Derived) Trạng thái thành công (1: Success, 0: Other)
    raw_duration_ms BIGINT,                    -- xAPI.result.duration
    time_id INT,
    ingest_timestamp DATETIME2 DEFAULT GETDATE(),
    CONSTRAINT PK_fact_statement PRIMARY KEY NONCLUSTERED (event_id),
    CONSTRAINT FK_fact_statement_actor FOREIGN KEY (actor_id) REFERENCES dim_actor(actor_id),
    CONSTRAINT FK_fact_statement_interaction FOREIGN KEY (interaction_id) REFERENCES dim_interation_type(interaction_id),
    CONSTRAINT FK_fact_statement_context FOREIGN KEY (context_id) REFERENCES dim_context(context_id),
    CONSTRAINT FK_fact_statement_time FOREIGN KEY (time_id) REFERENCES dim_time(time_id)
);
GO

-- 1.5 Tạo Clustered Columnstore Index cho fact_statement (Yêu cầu SQL Server 2014+)
-- Lưu ý: Primary Key PK_fact_statement sẽ tự động tạo Non-clustered Index nếu ta dùng Columnstore Clustered.
-- Tuy nhiên trong SQL Server, một bảng chỉ có 1 Clustered Index. 
-- Ta sẽ tạo Columnstore Index để tối ưu báo cáo.
CREATE CLUSTERED COLUMNSTORE INDEX CCI_fact_statement ON fact_statement;
GO

-- 2. fact_session (Phiên học tập)
IF OBJECT_ID('fact_session', 'U') IS NOT NULL DROP TABLE fact_session;
CREATE TABLE fact_session (
    session_id UNIQUEIDENTIFIER NOT NULL,      -- xAPI.context.registration
    actor_id NVARCHAR(255) NOT NULL,           -- xAPI.actor
    entry_point NVARCHAR(500),                 -- xAPI.object đầu session
    session_type NVARCHAR(100),                -- Tự định nghĩa
    start_time DATETIME2,                      -- min(timestamp)
    end_time DATETIME2,                        -- max(timestamp)
    session_duration INT,                      -- (Derived seconds)
    interrupt_count INT,                       -- (Derived)
    context_id NVARCHAR(255),
    avg_activity_gap DECIMAL(10,2),           -- (Derived)
    time_id INT,
    ingest_timestamp DATETIME2 DEFAULT GETDATE(),
    CONSTRAINT PK_fact_session PRIMARY KEY (session_id),
    CONSTRAINT FK_fact_session_actor FOREIGN KEY (actor_id) REFERENCES dim_actor(actor_id),
    CONSTRAINT FK_fact_session_context FOREIGN KEY (context_id) REFERENCES dim_context(context_id),
    CONSTRAINT FK_fact_session_time FOREIGN KEY (time_id) REFERENCES dim_time(time_id)
);
GO

-- 3. fact_quiz (Kết quả bài kiểm tra)
IF OBJECT_ID('fact_quiz', 'U') IS NOT NULL DROP TABLE fact_quiz;
CREATE TABLE fact_quiz (
    quiz_attempt_id NVARCHAR(255) NOT NULL,    -- ID lần thử (Moodle/xAPI context)
    time_id INT,
    attempt_no INT,                            -- Số lần thử (moodle)
    actor_id NVARCHAR(255) NOT NULL,
    start_time DATETIME2,                      -- (Derived)
    end_time DATETIME2,                        -- xAPI.timestamp
    total_score DECIMAL(10,2),                -- xAPI.result.score.raw
    max_score DECIMAL(10,2),                   -- Moodle max score
    pass_threshold DECIMAL(10,2),             -- Moodle threshold
    time_pressure_flag BIT,                    -- (Derived)
    isComplete BIT,                            -- xAPI.result.completion
    isSucceed BIT,                             -- xAPI.result.success
    raw_duration_ms BIGINT,                    -- xAPI.result.duration
    ingest_timestamp DATETIME2 DEFAULT GETDATE(),
    CONSTRAINT PK_fact_quiz PRIMARY KEY (quiz_attempt_id),
    CONSTRAINT FK_fact_quiz_actor FOREIGN KEY (actor_id) REFERENCES dim_actor(actor_id),
    CONSTRAINT FK_fact_quiz_time FOREIGN KEY (time_id) REFERENCES dim_time(time_id)
);
GO

-- 4. fact_question (Chi tiết câu hỏi trong Quiz)
IF OBJECT_ID('fact_question', 'U') IS NOT NULL DROP TABLE fact_question;
CREATE TABLE fact_question (
    question_id NVARCHAR(255) NOT NULL,        -- ID câu hỏi
    quiz_attempt_id NVARCHAR(255) NOT NULL,    -- FK to fact_quiz
    selected_answer NVARCHAR(MAX),             -- xAPI.response
    retry_count INT,                           -- (Derived)
    is_correct BIT,                            -- xAPI.result.success
    question_difficulty DECIMAL(5,2),          -- Tự định nghĩa
    ingest_timestamp DATETIME2 DEFAULT GETDATE(),
    CONSTRAINT PK_fact_question PRIMARY KEY (question_id, quiz_attempt_id),
    CONSTRAINT FK_fact_question_quiz FOREIGN KEY (quiz_attempt_id) REFERENCES fact_quiz(quiz_attempt_id)
);

-- 5. fact_activity (Thống kê hoạt động)
IF OBJECT_ID('fact_activity', 'U') IS NOT NULL DROP TABLE fact_activity;
CREATE TABLE fact_activity (
    activity_id NVARCHAR(500) NOT NULL,
    actor_id NVARCHAR(255) NOT NULL,
    activity_length INT,                       -- Moodle metadata (thời gian ước lượng)
    activity_type NVARCHAR(255),
    activity_difficulty DECIMAL(5,2),
    activity_order INT,                         -- (Moodle)
    is_mandatory BIT DEFAULT 1,                -- (Moodle)
    context_id NVARCHAR(255),
    completion_status NVARCHAR(100),           -- (Derived từ verb + result)
    time_spent BIGINT,                         -- sum(raw_duration)
    attempt_count INT,                         -- (Derived (chỉ quiz))
    time_id INT,
    ingest_timestamp DATETIME2 DEFAULT GETDATE(),
    CONSTRAINT PK_fact_activity PRIMARY KEY (activity_id, actor_id, time_id),
    CONSTRAINT FK_fact_activity_activity FOREIGN KEY (activity_id) REFERENCES dim_activity(activity_id),
    CONSTRAINT FK_fact_activity_actor FOREIGN KEY (actor_id) REFERENCES dim_actor(actor_id), 
    CONSTRAINT FK_fact_activity_context FOREIGN KEY (context_id) REFERENCES dim_context(context_id),
    CONSTRAINT FK_fact_activity_time FOREIGN KEY (time_id) REFERENCES dim_time(time_id)
);

-- 6. fact_progress (Tiến độ học tập)
IF OBJECT_ID('fact_progress', 'U') IS NOT NULL DROP TABLE fact_progress;
CREATE TABLE fact_progress (
    progress_id INT IDENTITY(1,1) NOT NULL,
    actor_id NVARCHAR(255) NOT NULL,
    outcome_id NVARCHAR(255),
    progress_percent DECIMAL(5,2),             -- (Derived)
    activity_difficulty DECIMAL(5,2),          -- (Derived)
    mastery_level NVARCHAR(100),               -- (Derived)
    last_activity_time DATETIME2,              -- (Derived)
    context_id NVARCHAR(255),
    attempt_count INT,                         -- (Derived)
    progress_velocity DECIMAL(10,2),           -- (Derived)
    ingest_timestamp DATETIME2 DEFAULT GETDATE(),
    CONSTRAINT PK_fact_progress PRIMARY KEY (progress_id),
    CONSTRAINT FK_fact_progress_actor FOREIGN KEY (actor_id) REFERENCES dim_actor(actor_id),
    CONSTRAINT FK_fact_progress_outcome FOREIGN KEY (outcome_id) REFERENCES dim_learning_outcome(outcome_id),
    CONSTRAINT FK_fact_progress_context FOREIGN KEY (context_id) REFERENCES dim_context(context_id)
);

-- =============================================
-- III. BRIDGE TABLES
-- =============================================

-- 1. bridge_ActivityHierachy (Phân cấp Hoạt động)
IF OBJECT_ID('bridge_ActivityHierachy', 'U') IS NOT NULL DROP TABLE bridge_ActivityHierachy;
CREATE TABLE bridge_ActivityHierachy (
    ancestor_activity_id NVARCHAR(500) NOT NULL,
    descendant_activity NVARCHAR(500) NOT NULL,    -- Đổi tên cho khớp với ảnh diagram
    is_direct_parent BIT DEFAULT 0,
    CONSTRAINT PK_bridge_ActivityHierachy PRIMARY KEY (ancestor_activity_id, descendant_activity),
    CONSTRAINT FK_bridge_ancestor_activity FOREIGN KEY (ancestor_activity_id) REFERENCES dim_activity(activity_id),
    CONSTRAINT FK_bridge_fact_activity FOREIGN KEY (descendant_activity) REFERENCES dim_activity(activity_id) 
);
GO

-- =============================================
-- TẠO INDEX ĐỂ TỐI ƯU TRUY VẤN
-- =============================================
CREATE INDEX IX_fact_statement_actor_time ON fact_statement(actor_id, time_id);
CREATE INDEX IX_fact_session_registration ON fact_session(session_id);
CREATE INDEX IX_fact_quiz_actor ON fact_quiz(actor_id);
GO

PRINT 'Da tao thanh cong Database va tat ca cac bang cho mo hinh Fact/Dimension xAPI!';
GO
