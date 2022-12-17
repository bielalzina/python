import pymysql.cursors

class gimnas(object):

    def carregaClients():
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        
        cursor=db.cursor()
        sql="SELECT * FROM clients"
        cursor.execute(sql)
        ResQuery=cursor.fetchall()
        db.close()
        return ResQuery

    def carregaPistes():
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        
        cursor=db.cursor()
        sql="SELECT * FROM pistes"
        cursor.execute(sql)
        ResQuery=cursor.fetchall()
        db.close()
        return ResQuery
    
    def carregaReserves():
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        
        cursor=db.cursor()
        sql="SELECT * FROM reserves"
        cursor.execute(sql)
        ResQuery=cursor.fetchall()
        db.close()
        return ResQuery
    
    def afegeixReserva(dataReserva,idPistaReserva,idClientReserva):
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)

        cursor=db.cursor()
        sql="INSERT INTO reserves (data,idpista,idclient)"
        sql=sql+" VALUES ('"+dataReserva+"',"+str(idPistaReserva)+","+str(idClientReserva)+");"
        cursor.execute(sql)
        db.close

    def carregaReservesSetmana(diaInici,diaFinal):
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        
        cursor=db.cursor()
        sql="SELECT reserves.data,reserves.idpista,reserves.idclient,pistes.tipo,"
        sql=sql+"clients.nom,clients.llinatges FROM reserves"
        sql=sql+" INNER JOIN pistes ON reserves.idpista=pistes.idpista"
        sql=sql+" INNER JOIN clients ON reserves.idclient=clients.idclient"
        sql=sql+" WHERE data BETWEEN '"+diaInici+"' AND '"+diaFinal+"'"
        sql=sql+" ORDER BY reserves.data ASC;"
        #print(sql)
        cursor.execute(sql)
        ResQuery=cursor.fetchall()
        db.close()
        return ResQuery

    
    def carregaClients():
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        
        cursor=db.cursor()
        sql="SELECT * FROM clients"
        cursor.execute(sql)
        ResQuery=cursor.fetchall()
        db.close()
        return ResQuery


    def eliminaClient(idclient):
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        
        cursor=db.cursor()
        sql="DELETE FROM clients WHERE idclient="+str(idclient)+";"
        cursor.execute(sql)
        db.close()
        
    def tornaMaximIdclient():
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        
        cursor=db.cursor()
        sql="SELECT MAX(idclient) maxId FROM clients;"
        cursor.execute(sql)
        Id=cursor.fetchone()
        db.close()
        return Id

    def afegeixClient(idclient,nom,llinatges,telefon):
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        
        cursor=db.cursor()
        sql="INSERT INTO clients (idclient,nom,llinatges,telefon)"
        sql=sql+" VALUES ("+str(idclient)+",'"+nom+"','"+llinatges+"','"+telefon+"');"
        cursor.execute(sql)
        db.close()

    def modificaClient(idclient,nom,llinatges,telefon):
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)

        cursor=db.cursor()
        sql="UPDATE clients SET nom='"+nom+"',llinatges='"+llinatges+"',"
        sql=sql+"telefon='"+telefon+"' WHERE idclient="+str(idclient)+";"
        cursor.execute(sql)
        db.close

