import psycopg

def get_conn():
    return psycopg.connect(host="localhost", dbname="ops_db", user="ops_user", password="1234")

def execute_query(q,returns_rows=False):
    with get_conn() as con:
        with con.cursor() as cur:
            cur.execute(q)
            rows = []

            if returns_rows:
                rows= cur.fetchall()
            return rows        


def create_table():
        try:
            query = "CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT, email TEXT)"
            execute_query(query)
        except Exception as e:
            print(e)

def insert_data(name, email):
    try:
        query = f"INSERT INTO users (name , email) VALUES ('{name}' , '{email}')"
        execute_query(query)
    except Exception as e:
        print(e)

def query_by_name(name):
    query = f"SELECT * from users WHERE name='{name}'"
    result = execute_query(query,returns_rows=True)
    print(result)

def delete_by_id(id):
    try:
        query = f"delete from users where id={id}"
        result = execute_query(query)
    except Exception as e:
        print(e)



# insert_data("Check1", "Check1@gmail.com")
# insert_data("Moshe", "moshe@gmail.com")
# insert_data("Alex", "alex@gmail.com")

# create_table()
delete_by_id(3)
