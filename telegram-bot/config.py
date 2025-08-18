import os
from dotenv import load_dotenv

# بارگذاری متغیرها از فایل .env
load_dotenv()

PROXY_URL = os.getenv("PROXY_URL")
