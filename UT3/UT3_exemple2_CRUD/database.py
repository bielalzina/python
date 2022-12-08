import pymysql.cursors

class biblioteca(object):

    def carregaEditors():
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='biblioteca',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        
        cursor=db.cursor()
        sql="SELECT * FROM EDITORS"
        cursor.execute(sql)
        ResQuery=cursor.fetchall()
        db.close()
        return ResQuery

    def afegeixEditor(nom):
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='biblioteca',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)

        cursor=db.cursor()

        # calculam nou ID_EDIT
        sql="SELECT MAX(ID_EDIT)+1 nouId FROM EDITORS"
        cursor.execute(sql)
        Id=cursor.fetchone()
        sql="INSERT INTO EDITORS (ID_EDIT,NOM_EDIT)"
        sql=sql+" VALUES ("+str(Id['nouId'])+",'"+nom+"');"
        cursor.execute(sql)
        db.close
        
    def modificaEditor(nom,id_edit):
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='biblioteca',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)

        cursor=db.cursor()

        sql="UPDATE EDITORS SET NOM_EDIT='"+nom+"' WHERE id_edit="+str(id_edit)+";"
        cursor.execute(sql)
        db.close

    def eliminaEditor(id_edit):
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='biblioteca',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)

        cursor=db.cursor()
        sql="DELETE FROM EDITORS WHERE id_edit="+str(id_edit)+";"
        cursor.execute(sql)
        db.close