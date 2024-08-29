import os
import time  # Import time module for waiting
import psycopg2
import glob
from sql_queries import *
import pandas as pd


def process_data(conn, cur, filepath, func):
    """
    Driver function to load data from csv files into Postgres database
    :param conn: The current connection to Postgres
    :param cur: The current cursor
    :param func: The function to call
    :return:
    """
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.csv'))
        for file in files:
            all_files.append(file)

    # print all found files
    print(f"There are {len(all_files)} files in the path {filepath}")

    # start to insert all data in filepath into Postgres
    for i, file in enumerate(all_files):
        func(cur, file)
        conn.commit()
        print(f"{i + 1}/{len(all_files)} files processed")


def process_account(cur, filepath):
    df = pd.read_csv(filepath, encoding="utf-8")
    for i, row in df.iterrows():
        for j in range(len(row)):
            if pd.isna(row[j]):
                row[j] = None
        cur.execute(account_insert, list(row))

    print(f"Records inserted for file {filepath}")


def main():
    conn = psycopg2.connect("host=10.86.153.53 dbname=assignment user=postgres password=190902 port=5433")
    cur = conn.cursor()

    process_data(conn=conn, cur=cur, filepath=".", func=process_account)


if __name__ == "__main__":
    main()
