import pymysql.cursors

class Biblioteca(object):
   
    def carregaDepartaments():
        # Connexió a la BBDD del servidor mysql
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='biblioteca',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql="SELECT * from DEPARTAMENTS"
        cursor.execute(sql)
        ResQuery=cursor.fetchall()
        db.close
        return ResQuery

    def carregaLlibres(departament):
        # Connexió a la BBDD del servidor mysql
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='biblioteca',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql="SELECT LLIBRES.TITOL, AUTORS.NOM_AUT FROM LLIBRES, AUTORS, LLI_AUT"
        sql=sql+" WHERE LLI_AUT.FK_IDLLIB=LLIBRES.ID_LLIB AND"
        sql=sql+" LLI_AUT.FK_IDAUT=AUTORS.ID_AUT AND"
        sql=sql+" LLIBRES.FK_DEPARTAMENT='"+departament+"';"
        cursor.execute(sql)
        ResQuery=cursor.fetchall()
        db.close
        return ResQuery