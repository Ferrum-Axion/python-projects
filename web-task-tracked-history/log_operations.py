import sys 
import psycopg
from datetime import datetime
import argparse

def get_conn():
    # move values to .env file 
    return psycopg.connect(host="localhost", dbname="ops_db", user="ops_user", password="1234")

def execute_query(q, include_rows= False):
    try:
        with get_conn() as con: 
            with con.cursor() as cursor:
                cursor.execute(q)
                if include_rows == True:
                    return cursor.fetchall()
    except Exception as e:
        print(e)


def generate_table():
    query = """ CREATE TABLE IF NOT EXISTS operations  (
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
    print(sys.argv[1])
    operation_status = sys.argv[2]
    duration = sys.argv[3]
    print(action_type,operation_status,duration)
    query = f"""insert into operations (action_type, executed_at, status, duration_seconds) VALUES 
    ('{action_type}', '{current_datetime}', '{operation_status}', '{duration}');
    """
    return execute_query(query)

print(__name__)

if __name__ == "__main__":
    generate_table()
    insert_operation_data()






