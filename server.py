# flask server that links to a DAO
# author: Michael Allen

from flask import Flask, request, jsonify, abort
#from projectDAOskeleton import projectDAO
#import projectDAO
from projectDAO import projectDAO
#import pyautogui
#import deleteRow
#from termcolor import colored

app = Flask(__name__, static_url_path='', static_folder='.')
#app = Flask(__name__)

@app.route('/')
def index():
        #message =  print(colored('Web Services and Applications Project', 'green', attrs=['bold']))
        #return message
        return 'Web Services and Applications Project'

# find by id
# curl http://127.0.0.1:5000/project/1

@app.route('/project/<int:id>', methods=['GET'])
def findbyid(id):
        return jsonify(projectDAO.findByID(id))

@app.route('/resident/<int:id>', methods=['GET'])
def findresbyid(id):
        return jsonify(projectDAO.findResByID(id))

@app.route('/resident/<name>', methods=['GET'])
def findresbyname(name):
       return jsonify(projectDAO.findResByName(name))

@app.route('/project/<name>', methods=['GET'])
def findbyname(name):
       return jsonify(projectDAO.findByName(name))

# getall
# curl http://127.0.0.1:5000/project

@app.route('/project', methods=['GET'])
def getall():
        return jsonify(projectDAO.getAll())

@app.route('/resident', methods=['GET'])
def getallres():
        return jsonify(projectDAO.getAllRes())

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"id\":5,\"name\":\"High Support Needs\",\"staff\":12}" http://127.0.0.1:5000/project
@app.route('/project', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    # other checking 
    project = {
        "id": request.json['id'],
        "name": request.json['name'],
        "staff": request.json['staff'],
        "residents": request.json['residents'],
    }
    addedproject = projectDAO.create(project)
    #pyautogui.hotkey('f5') #Simulates F5 key press = page refresh
    return jsonify(addedproject)

@app.route('/resident', methods=['POST'])
def createres():
    
    if not request.json:
        abort(400)
    # other checking 
    resident = {
        "id": request.json['id'],
        "name": request.json['name'],
        "age": request.json['age'],
        "ppsn": request.json['ppsn'],
    }
    addedresident = projectDAO.createres(resident)
    #pyautogui.hotkey('f5') #Simulates F5 key press = page refresh
    return jsonify(addedresident)

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"id\":5,\"name\":\"High Support Needs\",\"staff\":111}" http://127.0.0.1:5000/project/5
@app.route('/project/<int:id>', methods=['PUT'])
def update(id):
    foundProject = projectDAO.findByID(id)
    print(foundProject)
    if not foundProject:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    print(reqJson)
    #if 'id' in reqJson and type(reqJson['id']) is not int:
        #print("id is not an integer")
        #abort(400)
    if 'id' in reqJson:
        foundProject['id'] = reqJson['id']
    if 'name' in reqJson:
        foundProject['name'] = reqJson['name']
    if 'staff' in reqJson:
        foundProject['staff'] = reqJson['staff']
    if 'residents' in reqJson:
        foundProject['residents'] = reqJson['residents']
    projectDAO.update(id,foundProject)
    #pyautogui.hotkey('f5') #Simulates F5 key press = page refresh
    return jsonify(foundProject)  

@app.route('/resident/<int:id>', methods=['PUT'])
def updateres(id):
    foundResident = projectDAO.findResByID(id)
    print(foundResident)
    if not foundResident:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    print(reqJson)
    #if 'id' in reqJson and type(reqJson['id']) is not int:
        #print("id is not an integer")
        #abort(400)
    if 'id' in reqJson:
        foundResident['id'] = reqJson['id']
    if 'name' in reqJson:
        foundResident['name'] = reqJson['name']
    if 'age' in reqJson:
        foundResident['age'] = reqJson['age']
    if 'ppsn' in reqJson:
        foundResident['ppsn'] = reqJson['ppsn']
    projectDAO.updateres(id,foundResident)
    #pyautogui.hotkey('f5') #Simulates F5 key press = page refresh
    return jsonify(foundResident)   

@app.route('/project/<int:id>' , methods=['DELETE'])
def delete(id):
    projectDAO.delete(id)
    return jsonify({"done":True})
    #print("Delete done. Row " +id+ "was deleted successfully.")
    #return jsonify(projectDAO.delete(id))

@app.route('/resident/<int:id>' , methods=['DELETE'])
def deleteres(id):
    projectDAO.deleteres(id)
    return jsonify({"done":True})
    #print("Delete done. Row " +id+ "was deleted successfully.")
    #return jsonify(projectDAO.delete(id))

if __name__ == "__main__":
    app.run(debug = True)
