import json
import mysql.connector
import pandas as pd

class FYP_MySQL:
    """
    setup and login database
    """
    def __init__(self, host="localhost", user="root", password="rootnabil", db="fyp_database"):
        self.host = host
        self.user = user
        self.password = password
        self.db = db


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

    def execute(self, sql, record):
        self.__connect__()
        self.my_cursor.execute(sql, record)
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
    with open('Data Training.json', encoding='utf8', mode='r') as json_file:
        data = json.load(json_file)

    for i in data:
        sql = "INSERT IGNORE INTO data_training (`id`, `raw text`, `token text`, `category`) VALUES (%s,%s,%s,%s)"
        temp = ";".join(data[i]['token text'])
        record = (i, data[i]['raw text'].lower(),temp,data[i]['category'],)
        db.execute(sql,record)
    
def symptomModel():
    db = FYP_MySQL()
    data = pd.read_csv('symptom.csv')

    for record in data.values:
        print(tuple(record))
        

def test(): 
    db = FYP_MySQL()       
    for i in db.fetchALL('data_training'):
        raw = i[1]
        token = i[2].split(';')
        label = i[3]
        print('raw text :',raw,"token text :",token,"label :",label)


    
if __name__ == '__main__':
    symptomModel()
    

