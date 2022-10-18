import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from config import host, user, password


def df_to_sql(df, db_name: str):
    try:
        conn_string = f'postgresql://{user}:{password}@{host}:5432'

        db = create_engine(conn_string)
        conn = db.connect()


        df.to_sql(db_name, con=conn, if_exists='replace',
                index=False)
        conn = psycopg2.connect(conn_string
                                )
        conn.autocommit = True
        cursor = conn.cursor()

        sql1 = f'''select * from {db_name};'''
        cursor.execute(sql1)
        conn.commit()

    except Exception as ex:
        print()
        print(f'ERROR {ex}')
        print()

    finally:
        if conn:
            cursor.close()
            conn.close()
            print('[INFO] PostgreSQL connection closed')
