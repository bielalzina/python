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
        # Comprovam que existeix ID
        resultat_comprovacio=self.existeixIdUsuari(id_usuari)
        if (resultat_comprovacio):
            sql = "SELECT id,username,email,nom,llinatges,telefon,diaalta FROM usuaris"
            sql = sql + " WHERE id="+str(id_usuari)
            
            self.cursor.execute(sql)
            ResQuery=self.cursor.fetchone()
            # Convertirm date object a string
            ResQuery['diaalta']=ResQuery['diaalta'].strftime("%d/%m/%Y")
            return ResQuery
        else:
            return('UNABLE TO PROCESS THE OPERATION (GET)')

    def existeixIdUsuari(self, id_usuari):
        sql="SELECT COUNT(id) FROM usuaris WHERE id="+str(id_usuari)
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchone()
        if(ResQuery['COUNT(id)']==1):
            return True
        else:
            return False


    def modificaUsuari(self,id_usuari,camps):
        # Comprovam que existeix ID
        resultat_comprovacio=self.existeixIdUsuari(id_usuari)
        if (resultat_comprovacio):
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
        else:
            return('UNABLE TO PROCESS THE OPERATION (PUT)')

    def eliminaUsuari(self, id_usuari):
        # Comprovam que existeix ID
        resultat_comprovacio=self.existeixIdUsuari(id_usuari)
        if (resultat_comprovacio):
            sql = "DELETE FROM usuaris WHERE id="+str(id_usuari)
            self.cursor.execute(sql)
            return('USER DELETED')
        else:
            return('UNABLE TO PROCESS THE OPERATION (DELETE)')

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
        
        # Convertim data a objecte datetime
        # Si la data introduïda no es correcta strptime llança una errada,
        # per la qual cosa farem servir try - except
        try:
            data_object=datetime.datetime.strptime(data,"%Y-%m-%d")
            # print(type(data_object))
            # print(data_object)

            # Obtenim extrems inferior i superior de la setmana
            extremsSetmana=self.tornaExtremsSetmana(data_object)
            
            # Executam consulta
            llistaReserves=self.tornaReserves(extremsSetmana[0],extremsSetmana[1])
            return llistaReserves
        except ValueError:
            return('UNABLE TO PROCESS THE OPERATION (GET)')
            

        
    
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
        
        # Si la data-hora introduïda no es correcta strptime llança una errada,
        # per la qual cosa farem servir try - except
        try:
            data_object=datetime.datetime.strptime(camps['data'],"%Y-%m-%d %H:%M:%S")
            #print(type(data_object))
            #print(data_object)
            
            # Comprovam validesa HORA RESERVA
            
            hora_reserva=datetime.datetime.time(data_object)
            hora_reserva=hora_reserva.replace(minute=00)
            hora_reserva=hora_reserva.replace(second=00)
            # print(hora_reserva)
            # print(type(hora_reserva))
            hora_minima=datetime.time(15)
            hora_maxima=datetime.time(20)
            #print(hora_minima)
            #print(hora_maxima)
            if (hora_reserva>=hora_minima and hora_reserva<=hora_maxima):
                
                # Modificam camp['data'] passant minuts i segons a 0
                data_object=data_object.replace(minute=00)
                data_object=data_object.replace(second=00)
                camps['data']=data_object.strftime("%Y-%m-%d %H:%M:%S")
                # print(camps['data'])
                
                # Obtenim data-hora actual
                                
                dataHoraActual=self.tornaDataHoraActual()
                # print(dataHoraActual)
                
                # Comprovam si idpista introduït és correcte
                resultatComprovacioIdPista=self.comprovaIdPista(camps['idpista'])
                    
                # Comprovam si idusuari introduït és correcte
                resultatComprovacioIdUsuari=self.existeixIdUsuari(id_usuari)
                
                # Comprovam disponibilitat de la reserva
                reservaDisponible=self.tornaReservaDisponible(camps['data'],camps['idpista'])
                
                if (data_object>=dataHoraActual and resultatComprovacioIdPista and resultatComprovacioIdUsuari and reservaDisponible):

                    sql="INSERT INTO reserves (data,idpista,idclient)"
                    sql = sql + " values ('"+camps['data']+"',"+str(camps['idpista'])+","
                    sql = sql + str(id_usuari)+")"
                    # print(sql)
                    self.cursor.execute(sql)

                    # Retornam llistat de reserves fetes per l'usuari
                    llistatReserves=self.tornaReservesUsuari(id_usuari)
                    return llistatReserves

                else:
                    return('UNABLE TO REGISTER THE OPERATION (POST)')

            else:
                    return('UNABLE TO REGISTER THE OPERATION (POST)')

        except ValueError:
            
            return('UNABLE TO REGISTER THE OPERATION (POST)')
        
        
    def comprovaIdPista(self, idpista):
        
        sql="SELECT COUNT(idpista) FROM pistes WHERE idpista="+str(idpista)
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchone()
        if(ResQuery['COUNT(idpista)']==1):
            return True
        else:
            return False

    def eliminaReservaUsuari(self, id_usuari, camps):
        # Consider que només es poden eliminar les reserves futures, 
        # per la qual cosa cal comprovar que la reserva que es vol eliminar
        # es posterior a la data-hora actual
        
        # Primer cal comprovar la validesa de la data-hora inserida
        data_object=self.comprovaValidesaDataHora(camps['data'])
        
        if (data_object==False):
            return('UNABLE TO REGISTER THE OPERATION (DELETE)')
        else:
            # Obtenim data-hora actual
            dataHoraActual=self.tornaDataHoraActual()
            
            # Comprovam si idpista introduït és correcte
            resultatComprovacioIdPista=self.comprovaIdPista(camps['idpista'])
                    
            # Comprovam si idusuari introduït és correcte
            resultatComprovacioIdUsuari=self.existeixIdUsuari(id_usuari)
            
            # Comprovam si existeix la reserva que es vol anular
            reservaExistent=self.tornaReservaExistent(camps['data'],
                                                      camps['idpista'],
                                                      id_usuari)
            
            if (data_object>=dataHoraActual and resultatComprovacioIdPista and resultatComprovacioIdUsuari and reservaExistent):

                sql = "DELETE FROM reserves WHERE data='"+camps['data']+"'"
                sql = sql + " AND idpista="+str(camps['idpista'])
                sql = sql + " AND idclient="+str(id_usuari)
                # print(sql)
                self.cursor.execute(sql)
                return('RESERVA ELIMINADA')
        
            else:
                return('UNABLE TO REGISTER THE OPERATION (DELETE)')

    def tornaReservaDisponible(self, dataHora, idpista):
        sql="SELECT data, idpista FROM reserves"
        sql=sql+" WHERE data='"+dataHora+"' "
        sql=sql+" AND idpista="+str(idpista)
        print(sql)
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchone()
        if(ResQuery==None):
            return True
        else:
            return False
    
    
    def comprovaValidesaDataHora(self, dataHora):
        # Si la data-hora introduïda no es correcta strptime llança una errada,
        # per la qual cosa farem servir try - except
        try:
            data_object=datetime.datetime.strptime(dataHora,"%Y-%m-%d %H:%M:%S")
            return data_object
            
        except ValueError:
            return False

    def tornaDataHoraActual(self):
        dataHoraActual= datetime.datetime.now()
        dataHoraActual=dataHoraActual+datetime.timedelta(hours=1)
        dataHoraActual=dataHoraActual.replace(minute=00)
        dataHoraActual=dataHoraActual.replace(second=00)
        dataHoraActual=dataHoraActual.replace(microsecond=00)
        return dataHoraActual
    
    def tornaReservaExistent(self, dataHora, idpista, idusuari):
        sql="SELECT data, idpista FROM reserves"
        sql=sql+" WHERE data='"+dataHora+"' "
        sql=sql+" AND idpista="+str(idpista)
        sql=sql+" AND idclient="+str(idusuari)
        print(sql)
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchone()
        
        if(ResQuery==None):
            return False
        else:
            return True