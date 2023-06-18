import pymysql.cursors
import sqlalchemy as db
import configparser
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class vols(object):
    def conecta(self):
        # Conexion a la BBDD del servidor mySQL
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  db='vols',
                                  charset='utf8mb4',
                                  autocommit=True,
                                  cursorclass=pymysql.cursors.DictCursor)
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
        fechasql = fecha_hora.replace("_", " ")+":00"
        sql = "SELECT * from flights where arrival_airport='"+aeroport
        sql = sql+"' AND arrival_time>='"+fechasql+"' order by arrival_time limit 10"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        return ResQuery
    """

    def cargaArribades(self, aeroport, fecha_hora):
        dataSql = fecha_hora+" 00:00:00"
        dataObj = datetime.datetime.strptime(dataSql, '%Y-%m-%d %H:%M:%S')
        dataObjDema = dataObj+datetime.timedelta(days=1)
        dataSqlDema = dataObjDema.strftime("%Y-%m-%d %H:%M:%S")
        sql = "SELECT * FROM flights "
        sql = sql + "WHERE arrival_airport='"+aeroport+"' "
        sql = sql + "AND (arrival_time>='"+dataSql + \
            "' AND arrival_time<'"+dataSqlDema+"') "
        sql = sql + "ORDER BY arrival_time LIMIT 10"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        return ResQuery

    """ QUERY INICIAL
    def cargaSortides(self, aeroport, fecha_hora):
        fechasql = fecha_hora.replace("_", " ")+":00"
        sql = "SELECT * from flights where departure_airport='"+aeroport
        sql = sql+"' AND departure_time>='"+fechasql+"' order by departure_time limit 10"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        return ResQuery
    """

    def cargaSortides(self, aeroport, fecha_hora):
        dataSql = fecha_hora+" 00:00:00"
        # print(dataSql)
        # print(type(dataSql))
        dataObj = datetime.datetime.strptime(dataSql, '%Y-%m-%d %H:%M:%S')
        # print(dataObj)
        dataObjDema = dataObj+datetime.timedelta(days=1)
        # print(dataObjDema)
        dataSqlDema = dataObjDema.strftime("%Y-%m-%d %H:%M:%S")
        # print(dataSqlDema)
        # print(type(dataSqlDema))
        sql = "SELECT * FROM flights "
        sql = sql + "WHERE departure_airport='"+aeroport+"' "
        sql = sql + "AND (departure_time>='"+dataSql + \
            "' AND departure_time<'"+dataSqlDema+"') "
        sql = sql + "ORDER BY departure_time LIMIT 10"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchall()
        return ResQuery

    def tornaDadesVolRetras(self, id_vol):
        sql = "SELECT * FROM flights "
        sql = sql + "WHERE id_flight='"+id_vol+"';"
        self.cursor.execute(sql)
        ResQuery = self.cursor.fetchone()
        # print(ResQuery)
        return ResQuery

    def afegeixRetras(self, id_vol):
        dadesVol = vols.tornaDadesVolRetras(self, id_vol)
        print(dadesVol)
        horaSortida = dadesVol['departure_time']
        horaArribada = dadesVol['arrival_time']
        # print(type(horaSortida))
        # print(horaSortida)
        # print(horaArribada)
        horaSortida = horaSortida+datetime.timedelta(hours=1)
        horaArribada = horaArribada+datetime.timedelta(hours=1)
        # print(horaSortida)
        # print(horaArribada)
        horaSortidaSql = horaSortida.strftime("%Y-%m-%d %H:%M:%S")
        horaArribadaSql = horaArribada.strftime("%Y-%m-%d %H:%M:%S")
        # print(type(horaSortidaSql))
        # print(horaSortidaSql)
        # print(type(horaArribadaSql))
        # print(horaArribadaSql)
        sql = "UPDATE flights "
        sql = sql + "SET departure_time ='"+horaSortidaSql+"', "
        sql = sql + "arrival_time ='"+horaArribadaSql+"' "
        sql = sql + "WHERE id_flight='"+id_vol+"';"
        self.cursor.execute(sql)
        return "FET"
