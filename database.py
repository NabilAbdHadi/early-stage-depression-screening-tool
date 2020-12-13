import glob, os, re
from typing import Pattern
import mysql.connector
class FYP_MySQL:
    """
    setup and login database
    """
    def __init__(self, host="localhost", user="root", password="rootnabil", db="fyp_database"):
        self.host = host
        self.user = user
        self.password = password
        self.db = db


    #my_cursor.execute("CREATE DATABASE FYP_database")
    #my_cursor.execute("SHOW DATABASES")
    #my_cursor.execute("CREATE TABLE um_confession(ID VARCHAR(255) PRIMARY KEY, text LONGTEXT)")
    #my_cursor.execute("SHOW TABLES")


    def __connect__(self):
        self.mydb = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.password,
            database = self.db,
            )

        self.my_cursor = self.mydb.cursor()
    
    def __disconnect__(self):
        self.mydb.commit()
        self.mydb.close()

    def execute(self, sql):
        self.__connect__()
        self.my_cursor.execute(sql)
        self.__disconnect__()

    def fetchALL(self,table, attribute="*"):
        self.__connect__()
        self.my_cursor.execute("SELECT "+ attribute + " FROM "+ table)
        result = self.my_cursor.fetchall()
        self.__disconnect__()
        return result

    def insert(self, table, record):
        self.__connect__()
        sql_insert = "INSERT IGNORE INTO "+ table +" (ID, text) VALUES (%s, %s)"
        self.my_cursor.execute(sql_insert, record)
        self.__disconnect__()

    def delete(self, table, record):
        self.__connect__()
        sql_delete = "DELETE FROM "+ table +" WHERE ID = %s"
        self.my_cursor.execute(sql_delete, record)
        self.__disconnect__()

    def update(self, table, record):
        self.__connect__()
        sql_update = "UPDATE "+ table +" WHERE ID =%s SET text=%s"
        self.my_cursor.execute(sql_update, record)
        self.__disconnect__()


def main():

    
    db = FYP_MySQL()
    folder = 'um confession'
    table = folder.replace(" ","_").lower()

    """ create the database and table """
    #db.execute("CREATE DATABASE FYP_database")
    #db.execute("SHOW DATABASES")
    #db.execute("CREATE TABLE um_confession(ID VARCHAR(255) PRIMARY KEY, text LONGTEXT)")
    #db.execute("SHOW TABLES")

    """ commands for insert, update, and delete record """
    #db.execute("CREATE TABLE "+table+"(ID VARCHAR(255) PRIMARY KEY, text LONGTEXT)")

    """test mysql"""
    #record1 = ("M00001", "rabbit cat chicken")
    #my_cursor.execute(sql_delete,("ayam ikan lembu",))


    """
    extract all text file and save into database
    """
    #pattern = re.compile(r'[a-zA-Z0-9\,\.\(\)\s\?\!]+')

    for filename in os.listdir("E:/StudyAtUM/Sem 9/FYP 2/"+folder):
        content = open(os.path.join('E:/StudyAtUM/Sem 9/FYP 2/'+folder, filename), 'r', encoding='utf-8')
        filename = filename.split(".")
        id = filename[0]
        text = content.read()
        record = (id, text)
    
        db.insert(table, record)
    

    
if __name__ == '__main__':
    main()
    

