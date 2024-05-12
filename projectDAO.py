# Project dao 
# this data layer connects to a database
# Author: Michael Allen

import mysql.connector
import dbconfig as cfg
class ProjectDAO:
    connection=""
    cursor =''
    host=       ''
    user=       ''
    password=   ''
    database=   ''
    
    def __init__(self):
        self.host=       cfg.mysql['host']
        self.user=       cfg.mysql['user']
        self.password=   cfg.mysql['password']
        self.database=   cfg.mysql['database']

    def getcursor(self): 
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password,
            database=   self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        self.connection.close()
        self.cursor.close()
         
    def getAll(self):
        cursor = self.getcursor()
        sql="select * from project"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        #print(results)
        for result in results:
            #print(result)
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def findByID(self, id):
        cursor = self.getcursor()
        sql="select * from project where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def convertToDictionary(self, resultLine):
        attkeys=['id','name','staff']
        project = {}
        currentkey = 0
        for attrib in resultLine:
            project[attkeys[currentkey]] = attrib
            currentkey = currentkey + 1 
        return project

    def delete(self, id):
        cursor = self.getcursor()
        sql="delete from project where id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll()
        
        print("Delete done. Row " +str(id)+ " was deleted successfully.")
        return

    def create(self, project):
        cursor = self.getcursor()
        sql="insert into project (name,staff) values (%s,%s)"
        values = (project.get("name"), project.get("staff"))
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        project["id"] = newid
        self.closeAll()
        return project
    
    def update(self,id,project):
        cursor = self.getcursor()
        sql="update project set name=%s,staff=%s where id = %s"
        print(f"update project {project}")
        values = (project.get("name"),project.get("staff"),id)
        print(values)
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        
projectDAO = ProjectDAO()