import sys 
import psycopg
from datetime import datetime
import argparse
from dotenv import load_dotenv
import os

load_dotenv()
def get_conn():
    return psycopg.connect(host=os.getenv("HOST"), dbname=os.getenv("DBNAME"), user=os.getenv("APP_USER"), password=os.getenv("PASSWORD"))

def execute_query(q, returnornot):
    try:
        with get_conn() as con: 
            with con.cursor() as cursor:
                cursor.execute(q)
                if returnornot:
                   return cursor.fetchall()
                
    except Exception as e:
        print(e)


def generate_table():
    query = """ 
    CREATE TABLE IF NOT EXISTS operations (
    id SERIAL PRIMARY KEY,
    action_type TEXT,
    executed_at TIMESTAMP,
    status TEXT,
    exit_code INT,
    duration_seconds FLOAT
    );"""
    try:
        with get_conn() as con: 
            with con.cursor() as cursor:
                cursor.execute(query)
    except Exception as e:
        print(e)

def insert_operation_data():
    current_datetime = datetime.now()
    action_type = sys.argv[1]
    operation_status = sys.argv[2]
    duration = sys.argv[3]
    query = f"""insert into operations (action_type, executed_at, status, exit_code, duration_seconds) VALUES 
    ('{action_type}', '{current_datetime}', '{operation_status}', 0, '{duration}');
    """
    execute_query(query, False)


def query_all_lines():
    query = f"SELECT * FROM operations;"
    rows = execute_query(query, True)
    for row in rows:
        print(row)


generate_table()
insert_operation_data()
query_all_lines()







