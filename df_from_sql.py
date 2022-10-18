import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from config import host, user, password


def df_from_sql(db_name: str):
    try:

        conn_string = f'postgresql://{user}:{password}@{host}:5432'

        db = create_engine(conn_string)
        conn = db.connect()


        df = pd.read_sql_query(f'select * from {db_name}',con=conn)
        conn = psycopg2.connect(conn_string
                                )
        conn.autocommit = True
    except Exception as ex:
        print()
        print(f'ERROR {ex}')
        print()

    finally:
        if conn:
            conn.close()
            print('[INFO] PostgreSQL connection closed')
    return df
