import os
from dotenv import load_dotenv
load_dotenv()

class Config():
    SECRET_KEY = os.getenv('SECRET_KEY')
    TEMPLATES_AUTO_RELOAD = True
    SQLITECLOUD_URL = os.getenv('SQLITECLOUD_URL')