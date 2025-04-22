from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
import sqlite3
import pandas as pd
import time

SQLALCHEMY_DATABASE_URL = 'sqlite+pysqlite:///app/data/firms.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# conn = None

# while True:
#     try:
#         df = pd.read_csv('app/data/firms.csv', header=0)
#         # print(df.head(10))
#         conn = sqlite3.connect('app/data/firms.db', check_same_thread=False)
#         cursor = conn.cursor()
#         print('database connected...')
#         df.to_sql('firms', conn, if_exists='replace')
#         # sql = "SELECT * from firms;"
#         # df_read = pd.read_sql(sql, conn)
#         # print(df_read.head(10))
#         # df_read.to_csv('app/data/updated.csv')
#         break
#     except Exception as error:
#         print("Connection failed...")
#         print("Error: ", error)
#         time.sleep(2)
#     # finally:
#         # if conn:
#             # conn.close()

