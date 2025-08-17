# راهنمای اجرای ربات تلگرام

## مراحل اجرا

1. ایجاد محیط مجازی و فعال‌سازی آن:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. نصب وابستگی‌ها:
   ```bash
   pip install -r requirements.txt
   ```

3. کپی فایل `.env.example` به `.env` و مقداردهی متغیرها:
   - `BOT_TOKEN`: توکن ربات تلگرام
   - `BACKEND_URL`: آدرس سرور بک‌اند
   - `ADMIN_CHAT_ID`: آیدی چت ادمین

4. (اختیاری) تنظیم پروکسی‌ها برای استفاده از Every Proxy:
   ```bash
   export HTTP_PROXY=http://192.168.43.1:8080
   export HTTPS_PROXY=http://192.168.43.1:8080
   ```

5. اجرای ربات:
   ```bash
   python main.py
   ```

6. ارسال دستور `/start` در تلگرام و بررسی نمایش منوی اصلی.
