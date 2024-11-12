import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_database = os.getenv('DB_DATABASE')