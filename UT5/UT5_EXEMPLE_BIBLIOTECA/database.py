import pymysql.cursors
import sqlalchemy as db
import configparser

class biblioteca(object):
    def conecta(self):
        # CONNEXIÓ A BBDD
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  db='biblioteca',
                                  charset='utf8mb4',
                                  autocommit=True,
                                  cursorclass=pymysql.cursors.DictCursor)
        self.cursor=self.db.cursor()
    
    def desconecta(self):
        self.db.close()
    
    def tornaLlibrePerID(self, id_llibre):
        sql = "SELECT * FROM LLIBRES WHERE ID_LLIB="+str(id_llibre)
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchone()
        return ResQuery
    
    def tornaLlibresPerIDautor(self, id_autor):
        sql="SELECT LLIBRES.* FROM LLIBRES, LLI_AUT "
        sql=sql+"WHERE LLI_AUT.FK_IDLLIB=LLIBRES.ID_LLIB AND "
        sql=sql+"LLI_AUT.FK_IDAUT="+str(id_autor)
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        return ResQuery
    
    def tornaEditors(self):
        sql="SELECT * FROM EDITORS"
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        return ResQuery
    
    def nouEditor(self, camps):
        # Obtenim ID pel nou editor
        sql="SELECT MAX(ID_EDIT)+1 nouID FROM EDITORS"
        self.cursor.execute(sql)
        nouID=self.cursor.fetchone()
        sql="INSERT INTO EDITORS (ID_EDIT"
        for a in camps:
            sql = sql + ","+a
        sql = sql + ") VALUES ("+str(nouID['nouID'])
        for a in camps:
            sql = sql + ",'"+camps[a]+"'"
        sql = sql + ")"
        print(sql)
        self.cursor.execute(sql)
        sql = "SELECT * FROM EDITORS WHERE ID_EDIT="+str(nouID['nouID'])
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchone()
        return ResQuery
    
    def tornaEditorPerID(self, id_editor):
        sql = "SELECT * FROM EDITORS WHERE ID_EDIT="+str(id_editor)
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchone()
        return ResQuery
    
    def modificaEditor(self,id_editor,camps):
        for canvi in camps:
            sql = "UPDATE EDITORS SET "+canvi+"='"+camps[canvi]+"' "
            sql = sql +"WHERE ID_EDIT="+str(id_editor)
            print(sql)
            self.cursor.execute(sql)
        sql = "SELECT * FROM EDITORS WHERE ID_EDIT="+str(id_editor)
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchone()
        return ResQuery
    
    def eliminaEditor(self, id_editor):
        sql = "DELETE FROM EDITORS WHERE ID_EDIT="+str(id_editor)
        self.cursor.execute(sql)
        