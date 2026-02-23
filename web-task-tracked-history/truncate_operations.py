import sys 
import psycopg
from datetime import datetime
import argparse
from dotenv import load_dotenv
import os

load_dotenv()
def get_conn():
    return psycopg.connect(host=os.getenv("HOST"), dbname=os.getenv("DBNAME"), user=os.getenv("APP_USER"), password=os.getenv("PASSWORD"))

def truncate_operations():
    query = "TRUNCATE TABLE operations RESTART IDENTITY;"
    try:
        with get_conn() as con:
            with con.cursor() as cursor:
                cursor.execute(query)
                con.commit()
        print("operations table truncated.")
    except Exception as e:
        print("Error:", e)


truncate_operations()