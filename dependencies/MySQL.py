import os
import pymysql
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class MySQL:
    def __init__(self, res_type: str):
        if res_type == "create":
            self.hostname = os.getenv("LINE_MYSQL_HOST")
            self.port = int(os.getenv("LINE_MYSQL_PORT"))
            self.username = os.getenv("LINE_MYSQL_USER")
            self.password = os.getenv("LINE_MYSQL_PASSWORD")
            self.database = os.getenv("LINE_MYSQL_DATABASE")

    def upload(self, sql_command: str):
        connection = pymysql.connect(
            host=self.hostname,
            port=self.port,
            user=self.username,
            password=self.password,
            db=self.database,
        )

        connection.autocommit(True)
        cursor = connection.cursor()
        

        try:
            cursor.execute(sql_command)
        except:
            raise Exception("uplaod failed")

        connection.commit()
        cursor.close()
        connection.close()

    def download(self, sql_command: str):
        connection = pymysql.connect(
            self.hostname,
            self.username,
            self.password,
            self.database,
        )
        try:
            cursor.execute(sql_command)
            data_tuple = cursor.fetchall()
            err_detail = 0
        except Exception:
            data_tuple = []

        cursor.close()
        connection.close()

        return data_tuple

