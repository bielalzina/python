import pymysql.cursors
import sqlalchemy as db
import configparser
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class vols(object):
    def conecta(self):
        # Conexion a la BBDD del servidor mySQL
        self.db = pymysql.connect(
            host="localhost",
            user="root",
            db="vols",
            charset="utf8mb4",
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor,
        )
        self.cursor = self.db.cursor()

    def desconecta(self):
        self.db.close()

    def cargaAeroports(self):
        sql = "SELECT * from airports"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        return ResQuery

    """ QUERY INICIAL
    def cargaArribades(self, aeroport, fecha_hora):
        fechasql = fecha_hora.replace("_", " ") + ":00"
        sql = "SELECT * from flights where arrival_airport='" + aeroport
        sql = (
            sql
            + "' AND arrival_time>='"
            + fechasql
            + "' order by arrival_time limit 10"
        )
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        return ResQuery
    """

    def cargaArribades(self, aeroport, fecha_hora):
        dataSql = fecha_hora + " 00:00:00"
        dataObj = datetime.datetime.strptime(dataSql, "%Y-%m-%d %H:%M:%S")
        dataObjDema = dataObj + datetime.timedelta(days=1)
        dataSqlDema = dataObjDema.strftime("%Y-%m-%d %H:%M:%S")
        print(dataSql)
        print(dataSqlDema)
        sql = "SELECT * FROM flights "
        sql = sql + "WHERE arrival_airport='" + aeroport + "' "
        sql = (
            sql
            + "AND (arrival_time>='"
            + dataSql
            + "' AND arrival_time<'"
            + dataSqlDema
            + "') "
        )
        sql = sql + "ORDER BY arrival_time LIMIT 10;"
        print(sql)
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        return ResQuery

    """ QUERY INICIAL
    def cargaSortides(self, aeroport, fecha_hora):
        fechasql = fecha_hora.replace("_", " ") + ":00"
        sql = "SELECT * from flights where departure_airport='" + aeroport
        sql = (
            sql
            + "' AND departure_time>='"
            + fechasql
            + "' order by departure_time limit 10"
        )
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        return ResQuery
    """

    def cargaSortides(self, aeroport, fecha_hora):
        # print(aeroport)
        # print(fecha_hora)
        dataSql = fecha_hora + " 00:00:00"
        dataObj = datetime.datetime.strptime(dataSql, "%Y-%m-%d %H:%M:%S")
        dataObjDema = dataObj + datetime.timedelta(days=1)
        dataSqlDema = dataObjDema.strftime("%Y-%m-%d %H:%M:%S")
        print(dataSql)
        print(dataSqlDema)
        sql = "SELECT * FROM flights "
        sql = sql + "WHERE departure_airport='" + aeroport + "' "
        sql = (
            sql
            + "AND (departure_time>='"
            + dataSql
            + "' AND departure_time<'"
            + dataSqlDema
            + "') "
        )
        sql = sql + "ORDER BY departure_time LIMIT 10;"
        print(sql)
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        return ResQuery

    def retrasaVol(self, id_vol):
        sql = "SELECT * FROM flights WHERE id_flight='" + id_vol + "';"
        self.cursor.execute(sql)
        valors = self.cursor.fetchone()
        sortida = valors["departure_time"]
        arribada = valors["arrival_time"]
        # print(type(sortida))
        # print(sortida)
        # print(type(arribada))
        # print(arribada)
        sortidaNova = sortida + datetime.timedelta(hours=1)
        arribadaNova = arribada + datetime.timedelta(hours=1)
        # print(type(sortidaNova))
        # print(sortidaNova)
        # print(type(arribadaNova))
        # print(arribadaNova)
        sortidaNovaSql = sortidaNova.strftime("%Y-%m-%d %H:%M:%S")
        arribadaNovaSql = arribadaNova.strftime("%Y-%m-%d %H:%M:%S")
        sql = (
            "UPDATE flights SET departure_time='"
            + sortidaNovaSql
            + "', arrival_time='"
            + arribadaNovaSql
            + "' WHERE id_flight='"
            + id_vol
            + "';"
        )
        # print(sql)
        self.cursor.execute(sql)
        return "FET"
