<<<<<<< HEAD
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "college_placement_db")
=======
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "college_placement_db")
>>>>>>> 24669ef91ad9a39de534320428a60ef7db8acb63
    )