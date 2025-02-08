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
        sql="select * from training"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        #print(results)
        for result in results:
            #print(result)
            returnArray.append(self.convertToDictionaryTrain(result))
        
        self.closeAll()
        return returnArray
    
    def getAllTrain(self):
            cursor = self.getcursor()
            sql="select * from training"
            cursor.execute(sql)
            results = cursor.fetchall()
            returnArray = []
            #print(results)
            for result in results:
                #print(result)
                returnArray.append(self.convertToDictionaryTrain(result))
            
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
        
    def findByTrainID(self, id):
        cursor = self.getcursor()
        sql="select * from training where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def convertToDictionaryTrain(self, resultLine):
        attkeys=['id','name','happy','overall','venue','tutor','materials','admin','feedback_tutor','anycomments','courses']
        project = {}
        currentkey = 0
        for attrib in resultLine:
            project[attkeys[currentkey]] = attrib
            currentkey = currentkey + 1 
        return project

    def convertToDictionary(self, resultLine):
            attkeys=['id','name','happy','overall','venue','tutor','materials']
            training = {}
            currentkey = 0
            for attrib in resultLine:
                training[attkeys[currentkey]] = attrib
                currentkey = currentkey + 1 
            return training

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
        sql="insert into project (name,staff,residents) values (%s,%s,%s)"
        values = (project.get("name"), project.get("staff"), project.get("residents"))
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        project["id"] = newid
        self.closeAll()
        return project

    def createTrain(self, training):
            #print(training)
            print(training.get("courses"))
            allcourses = str(training.get("courses"))+' '+str(training.get("courses1"))+' '+str(training.get("courses2"))+' '+str(training.get("courses3"))+' '+ str(training.get("courses4"))+' '+ str(training.get("courses5"))+' '+ str(training.get("courses6"))
            print(allcourses)
            cursor = self.getcursor()
            sql="insert into training (name,happy,overall,venue,tutor,materials,admin,feedback_tutor,anycomments,courses) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (training.get("name"), training.get("happy"), training.get("overall"), training.get("venue"), training.get("tutor"), training.get("materials"), training.get("admin"), training.get("feedback_tutor"), training.get("anycomments"), allcourses)
            #cursor.execute(sql,(values,))
            cursor.execute(sql,values)

            self.connection.commit()
            newid = cursor.lastrowid
            training["id"] = newid
            self.closeAll()
            return training
        
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