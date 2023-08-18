'''
    pip3 install Faker
    pip3 install sqlalchemy
'''
from faker import Faker

fake = Faker('ko_KR')
Faker.seed(1)

import random
import datetime
import pandas as pd
import pymysql

from sqlalchemy import create_engine
import sqlalchemy as db


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--repeat_count', type=int, default=1000)
parser.add_argument('--mode', type=str, default='user')
args = parser.parse_args()

repeat_count = args.repeat_count

user_name = 'root'
password = 'admin123!'
host = '127.0.0.1'
port = 3306
db_name = 'sora_db'


if args.mode == 'user':
    email = [fake.unique.free_email() for _ in range(repeat_count)]
    user_pw = [fake.password() for _ in range(repeat_count)]
    phone = []
    while True:
        new_num = '010'+str(random.randint(1, 9999)).zfill(4)+str(random.randint(1, 9999)).zfill(4)
        if new_num not in phone:
            phone.append(new_num)
        if len(phone) == repeat_count:
            break

    gender = [random.choice(['남', '여']) for _ in range(repeat_count)]
    university = [random.choice(['홍익대학교', '중앙대학교', '한양대학교']) for _ in range(repeat_count)]
    student_id = [str(random.randint(1, 9999)).zfill(4) for _ in range(repeat_count)]
    department = [random.choice(['경영학과', '전자공학과', '생명공학과']) for _ in range(repeat_count)]
    description = [fake.text() for _ in range(repeat_count)]

    df = pd.DataFrame()
    df['email'] = email
    df['user_pw'] = user_pw
    df['phone_number'] = phone
    df['gender'] = gender
    df['university'] = university
    df['student_id'] = student_id
    df['department'] = department
    df['description'] = description
    df['create_at'] = [datetime.datetime.now() for _ in range(repeat_count)]
    df['update_at'] = [datetime.datetime.now() for _ in range(repeat_count)]
    df['auth'] = [random.choice([0,1]) for _ in range(repeat_count)]

pymysql.install_as_MySQLdb()

engine = create_engine(f"mysql+pymysql://{user_name}:{password}@{host}:{port}/{db_name}?charset=utf8mb4")

with engine.connect() as conn:
    df.to_sql(name='user', con=conn, if_exists='append', index=False)
    conn.close()