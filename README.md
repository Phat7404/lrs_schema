# xAPI Data Warehouse ETL Service

Service FastAPI để fetch dữ liệu từ xAPI LRS và load vào Data Warehouse (SQL Server) với dữ liệu bổ sung từ Moodle (MySQL).

## Cấu trúc Project

```
fact_schema_lrs/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Cấu hình database và API
│   ├── models/
│   │   ├── __init__.py
│   │   └── xapi_models.py         # Pydantic models cho xAPI statements
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py          # DatabaseManager class
│   ├── services/
│   │   ├── __init__.py
│   │   ├── xapi_service.py        # XAPIService class
│   │   └── moodle_service.py      # MoodleService class
│   └── etl/
│       ├── __init__.py
│       ├── processor.py           # ETLProcessor class chính
│       ├── dimension_processor.py # DimensionProcessor class
│       ├── fact_processor.py      # FactProcessor class
│       ├── bridge_processor.py     # BridgeProcessor class
│       └── utils.py               # DataExtractor utility class
├── requirements.txt               # Python dependencies
├── create_tables.sql              # Script tạo bảng SQL Server
├── doc.md                         # Tài liệu mô tả schema
└── README.md                      # File này
```

## Cài đặt

1. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

2. **Cấu hình database:**
   - Tạo file `.env` trong thư mục gốc và điền thông tin kết nối database:
     ```
     SQLSERVER_HOST=localhost
     SQLSERVER_PORT=1433
     SQLSERVER_DATABASE=moodle_datawarehouse
     SQLSERVER_USER=sa
     SQLSERVER_PASSWORD=your_password
     
     MYSQL_HOST=localhost
     MYSQL_PORT=3306
     MYSQL_DATABASE=moodle
     MYSQL_USER=root
     MYSQL_PASSWORD=your_password
     ```
   - Hoặc chỉnh sửa trực tiếp trong `app/config.py`
   - **Lưu ý:** Service sẽ kết nối database khi cần (lazy connection), không bắt buộc phải có database ngay khi khởi động

3. **Tạo database và tables:**
   - Chạy script `create_tables.sql` trên SQL Server để tạo database và các bảng

## Sử dụng

### Chạy service:

Cách 1: Sử dụng file run.py (khuyến nghị)
```bash
python run.py
```

Cách 2: Sử dụng uvicorn trực tiếp
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Cách 3: Chạy module
```bash
python -m app.main
```

### API Endpoints

1. **GET /** - Thông tin service
2. **GET /health** - Kiểm tra kết nối database
3. **POST /fetch-and-load** - Fetch tất cả statements từ xAPI LRS và load vào data warehouse
4. **POST /fetch-and-load-batch?limit=100&offset=0** - Fetch statements với pagination

### Ví dụ sử dụng:

```bash
# Health check
curl http://localhost:8000/health

# Fetch và load dữ liệu
curl -X POST http://localhost:8000/fetch-and-load

# Fetch với pagination
curl -X POST "http://localhost:8000/fetch-and-load-batch?limit=50&offset=0"
```

## Kiến trúc

Service này được tổ chức theo mô hình class-based với các thành phần:

### Services Layer:
- **XAPIService**: Xử lý việc fetch statements từ xAPI LRS
- **MoodleService**: Lấy dữ liệu bổ sung từ Moodle MySQL database

### ETL Layer:
- **ETLProcessor**: Class chính điều phối toàn bộ quá trình ETL
- **DimensionProcessor**: Xử lý các bảng dimension (dim_actor_account, dim_verb, dim_activity, activity_detail, dim_event_meta)
- **FactProcessor**: Xử lý các bảng fact (fact_statement, fact_quiz, fact_question_answer)
- **BridgeProcessor**: Xử lý bridge table (bridge_ActivityHierarchy với closure table logic)
- **DataExtractor**: Utility class để extract và parse dữ liệu từ statements

### Database Layer:
- **DatabaseManager**: Quản lý kết nối SQL Server và MySQL

### Quy trình ETL:

1. **Fetch dữ liệu:** XAPIService lấy statements từ xAPI LRS API với Basic Authentication
2. **ETL Processing:** 
   - DimensionProcessor xử lý các bảng dimension trước
   - FactProcessor xử lý các bảng fact
   - BridgeProcessor tạo closure table cho activity hierarchy
   - DataExtractor hỗ trợ extract và parse dữ liệu
3. **Load vào Data Warehouse:** Insert dữ liệu vào SQL Server với transaction management

## Các bảng được tạo:

### Dimension Tables:
- `dim_actor_account` - Thông tin học viên
- `dim_verb` - Các hành động xAPI
- `dim_activity` - Các hoạt động
- `activity_detail` - Chi tiết hoạt động
- `dim_event_meta` - Metadata sự kiện Moodle

### Fact Tables:
- `fact_statement` - Sự kiện xAPI chung
- `fact_quiz` - Chỉ số Quiz/Đánh giá
- `fact_question_answer` - Phân tích cấp độ câu hỏi

### Bridge Table:
- `bridge_ActivityHierarchy` - Phân cấp hoạt động (Closure Table)

## Lưu ý

- Service tự động xử lý duplicate statements (sử dụng IF NOT EXISTS)
- Tất cả các transactions được commit sau khi xử lý xong tất cả statements
- Service tự động reconnect nếu connection bị mất
- Xem file `doc.md` để hiểu chi tiết về schema và logic mapping

