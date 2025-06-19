# DSS Admin Tool Automation Test Suite

## Mô tả

Bộ test tự động sử dụng **Playwright** + **Pytest** (Python) kiểm thử trang đăng nhập của DSS Admin Tool theo mô hình Page Object Model (POM).

## Yêu cầu hệ thống
- Python 3.8+
- pip
- Git (nếu clone repo)

## Cài đặt & Setup môi trường

### 1. Clone repository (nếu cần)
```bash
git clone <repo-url>
cd MCPBrowser
```

### 2. Tạo virtual environment (khuyến nghị)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

Nếu chưa có file `requirements.txt`, cài trực tiếp:
```bash
pip install playwright pytest pytest-html
```

### 4. Cài đặt browser cho Playwright
```bash
playwright install
```

## Cấu trúc thư mục
```
MCPBrowser/
├── pages/                # Page Object Model classes
│   ├── login_page.py
│   └── dashboard_page.py
├── tests/                # Test scripts
│   └── test_accessibility.py
├── conftest.py           # Pytest fixtures (login, browser, ...)
├── requirements.txt      # Danh sách dependencies (nếu có)
└── README.md             # File hướng dẫn này
```

## Hướng dẫn chạy test

### 1. Chạy toàn bộ test
```bash
pytest
```

### 2. Chạy test với báo cáo HTML
```bash
pytest --html=report.html --self-contained-html
```

### 3. Chạy test ở chế độ headed (có giao diện)
```bash
pytest --headed --slowmo=500
```

### 4. Một số lệnh hữu ích
- **Chạy test cụ thể:**
  ```bash
  pytest tests/test_accessibility.py
  ```
- **Chạy test và lưu log:**
  ```bash
  pytest -v > result.log
  ```

## Lưu ý
- Đảm bảo mạng nội bộ truy cập được vào trang DSS Admin Tool (`http://10.255.245.202`).
- Nếu gặp lỗi về browser, hãy chạy lại `playwright install`.
- Có thể cần cập nhật selector nếu UI thay đổi.

## Liên hệ
Nếu gặp vấn đề, liên hệ QA/Dev phụ trách automation. 