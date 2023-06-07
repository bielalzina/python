import pymysql.cursors
import random
import joblib
import json
import sqlalchemy as db
from dateutil.parser import parse
import datetime


class gimnas (object):

    def carregaUsuaris():
        # CONNEXIO A BBDD
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='gimnas2',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        sql = "SELECT * from clients"
        cursor.execute(sql)
        ResQuery = cursor.fetchall()
        db.close()
        print(ResQuery)
        return ResQuery

    def carregaReserves(dia):
        # CONNEXIO A BBDD
        db = pymysql.connect(host='localhost',
                             user='root',
                             db='gimnas2',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()

        db.close()
        print(ResQuery)
        return ResQuery
