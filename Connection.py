import pymysql
import pandas as pd

class Connection:

    def __init__(self):
        try:
            self.connection=pymysql.connect("localhost","root","root","Instacart")
        except:
            print ("Connection Error!!!!")

    def select(self,table,column):

        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute("select "+ column +" from "+table)
            results = self.cursor.fetchall()
            return results
        except IOError as e:
            print  format(e.errno, e.strerror)


    def select_df(self,table):
        try:
            results = pd.read_sql("select * from "+table+" where 1 "  ,con=self.connection)
            return results
        except IOError as e:
            print  format(e.errno, e.strerror)        
