#!/usr/bin/python3
import pymysql
from notetool.secret import read_secret


def create_database(database=None):
    # 打开数据库连接
    host = read_secret(cate1="database", cate2="mysql", cate3="host")
    user = read_secret(cate1="database", cate2="mysql", cate3="user")
    password = read_secret(cate1="database", cate2="mysql", cate3="password")
    database = database or read_secret(cate1="database", cate2="mysql", cate3="database")
    print(host, user, password, database)
    db = pymysql.connect(host=host, user=user, password=password)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    cursor.execute(f'CREATE DATABASE {database};')

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("show databases")

    data = cursor.fetchmany()

    print(f"Database {data}")

    # 关闭数据库连接
    db.close()


create_database(database='notecoin')
