import pymysql.cursors
import sqlalchemy as db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import configparser
import json

class gimnas(object):
    def conecta(self):
        # CONNEXIÓ A BBDD
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  db='gimnasUT5',
                                  charset='utf8mb4',
                                  autocommit=True,
                                  cursorclass=pymysql.cursors.DictCursor)
        self.cursor=self.db.cursor()
    
    def desconecta(self):
        self.db.close()
    
    def tornaUsuaris(self):
        sql="SELECT id,username,email,nom,llinatges,telefon,diaalta FROM usuaris"
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        
        # Convertirm date object a string
        for valor in ResQuery:
            valor['diaalta']=valor['diaalta'].strftime("%d/%m/%Y")
        
        return ResQuery
    
    def nouUsuari(self, camps):
        # Comprovam que el nom d'usuari NO estigui ocupat
        sql="SELECT username FROM usuaris WHERE username='"+camps['username']+"'"
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchone()
        #print(ResQuery)
        if (ResQuery==None):
            
            # Obtenim ID pel nou usuari
            sql="SELECT MAX(id)+1 nouID FROM usuaris"
            self.cursor.execute(sql)
            nouID=self.cursor.fetchone()
            
            # Generam HASH pel password
            camps['password']=generate_password_hash(camps['password'])
            
            # Afegim usuari
            sql="INSERT INTO usuaris (id"
            for a in camps:
                sql = sql + ","+a
            sql = sql + ") VALUES ("+str(nouID['nouID'])
            for a in camps:
                sql = sql + ",'"+camps[a]+"'"
            sql = sql + ")"
            self.cursor.execute(sql)
            
            # Retornam nou usuari 
            ResQuery=self.tornaUsuariPerID(nouID['nouID'])
            return ResQuery
        
        else:
            return('UNABLE TO REGISTER THE OPERATION')


    def tornaUsuariPerID(self, id_usuari):
        sql = "SELECT id,username,email,nom,llinatges,telefon,diaalta FROM usuaris"
        sql = sql + " WHERE id="+str(id_usuari)
        print(sql)
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchone()
        # Convertirm date object a string
        ResQuery['diaalta']=ResQuery['diaalta'].strftime("%d/%m/%Y")
        return ResQuery

    def modificaUsuari(self,id_usuari,camps):
        # Si es modifica password, generam HASH
        if camps['password']:
            camps['password']=generate_password_hash(camps['password'])
        
        # Inserim modificacions
        for canvi in camps:
            sql = "UPDATE usuaris SET "+canvi+"='"+camps[canvi]+"' "
            sql = sql +"WHERE id="+str(id_usuari)
            self.cursor.execute(sql)
        
        # Retornam dades de l'usuari modificat
        ResQuery=self.tornaUsuariPerID(id_usuari)
        return ResQuery

    def eliminaUsuari(self, id_usuari):
        sql = "DELETE FROM usuaris WHERE id="+str(id_usuari)
        self.cursor.execute(sql)

    def tornaReserves(self,dataInicial,dataFinal):
        sql="SELECT reserves.data,pistes.tipo,usuaris.username"
        sql=sql+" FROM reserves"
        sql=sql+" INNER JOIN pistes ON reserves.idpista=pistes.idpista"
        sql=sql+" INNER JOIN usuaris ON reserves.idclient=usuaris.id"
        sql=sql+" WHERE data BETWEEN '"+dataInicial+"' AND '"+dataFinal+"'"
        sql=sql+" ORDER BY reserves.data ASC;"
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        # Convertirm date object a string
        for valor in ResQuery:
            valor['data']=valor['data'].strftime("%d/%m/%Y, %H:%M:%S")
        return ResQuery
    
    
    def tornaReservesSetmana(self,data):
        # print('data:')
        # print(type(data))
        # print(data)

        # Convertim data a objecte datetime
        data_object=datetime.datetime.strptime(data,"%Y-%m-%d")
        # print(type(data_object))
        # print(data_object)

        # Obtenim extrems inferior i superior de la setmana
        extremsSetmana=self.tornaExtremsSetmana(data_object)
        
        # Executam consulta
        llistaReserves=self.tornaReserves(extremsSetmana[0],extremsSetmana[1])
        return llistaReserves

        
    
    def tornaReservesSetmanaActual(self):
        
        # Obtenim data avui
        avui=datetime.date.today()
        print(avui)

        # Obtenim extrems inferior i superior de la setmana
        extremsSetmana=self.tornaExtremsSetmana(avui)
        
        # Executam consulta
        llistaReserves=self.tornaReserves(extremsSetmana[0],extremsSetmana[1])
        return llistaReserves

    def tornaExtremsSetmana(self, data):
        diaDeLaSetmana=int(data.strftime("%w"))
        
        if diaDeLaSetmana==0: # Diumenge
            extremInferior=data-datetime.timedelta(days=6)
        else: # Dilluns, dimarts,.., dissabte
            extremInferior=data-datetime.timedelta(days=(diaDeLaSetmana-1))
        extremSuperior=extremInferior+datetime.timedelta(days=7)

        # Valors per fer consultar SQL
        extremInferiorSQL=extremInferior.strftime("%Y-%m-%d")
        extremSuperiorSQL=extremSuperior.strftime("%Y-%m-%d")

        # print('extremInferiorSQL:')
        # print(extremInferiorSQL)
        # print('extremSuperiorSQL:')
        # print(extremSuperiorSQL)

        return[extremInferiorSQL,extremSuperiorSQL]


    def tornaReservesUsuari(self,id_usuari):
        sql="SELECT reserves.data,pistes.tipo"
        sql=sql+" FROM reserves"
        sql=sql+" INNER JOIN pistes ON reserves.idpista=pistes.idpista"
        sql=sql+" WHERE idclient='"+str(id_usuari)+"'"
        sql=sql+" ORDER BY reserves.data ASC;"
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        # Convertirm date object a string
        for valor in ResQuery:
            valor['data']=valor['data'].strftime("%d/%m/%Y, %H:%M:%S")
        return ResQuery

    def novaReservaUsuari(self, id_usuari, camps):
        # print(id_usuari)
        # print(type(id_usuari))
        # print(camps['data'])
        # print(type(camps['data']))
        # print(camps['idpista'])
        # print(type(camps['idpista']))
        
        # Comprovam disponibilitat de la reserva
        sql="SELECT data, idpista FROM reserves"
        sql=sql+" WHERE data='"+camps['data']+"' "
        sql=sql+" AND idpista="+str(camps['idpista'])
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchone()
        #print(ResQuery)
        if (ResQuery==None):
            sql="INSERT INTO reserves (data,idpista,idclient)"
            sql = sql + " values ('"+camps['data']+"',"+str(camps['idpista'])+","
            sql = sql + str(id_usuari)+")"
            # print(sql)
            self.cursor.execute(sql)

            # Retornam llistat de reserves fetes per l'usuari
            llistatReserves=self.tornaReservesUsuari(id_usuari)
            return llistatReserves

        else:
            return('UNABLE TO REGISTER THE OPERATION')

    def eliminaReservaUsuari(self, id_usuari, camps):
        sql = "DELETE FROM reserves WHERE data='"+camps['data']+"'"
        sql = sql + " AND idpista="+str(camps['idpista'])
        sql = sql + " AND idclient="+str(id_usuari)
        # print(sql)
        self.cursor.execute(sql)
