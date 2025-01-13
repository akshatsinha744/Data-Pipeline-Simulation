import psycopg2
import pandas as pd
import json
from sqlalchemy import create_engine

hostname = 'localhost'
database = 'Company_Set'
username = 'postgres'
pwd = '250857'
port_id = 5432
conn = None
cur = None

try:
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
    cur = conn.cursor()

    def etl_process(json_file,postgres_uri,table_name):
        with open(json_file,'r') as file:
            data = json.load(file)
        
        df = pd.json_normalize(data,record_path=['users'],meta=[],errors='ignore')

        engine = create_engine(postgres_uri)

        df.to_sql(table_name, engine, if_exists = 'replace', index = False)

        print(f"ETL process completed. Data loaded into '{table_name}' table")

    json_file_path = r"C:\Users\davpt\OneDrive\Desktop\Akshat\question3_sample_data.json"
    postgres_uri = 'postgresql://postgres:250857@localhost:5432/Company_Set'
    table_name = 'qq3_csv'

    etl_process(json_file_path,postgres_uri,table_name)


except Exception as error:
    print("Error:", error)

finally:

    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()

        