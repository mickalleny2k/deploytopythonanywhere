# flask server that links to a DAO
# author: Michael Allen

from geopy.geocoders import Nominatim
from gmplot import gmplot
import os
import webbrowser
from googlesearch import search
from flask import Flask, request, jsonify, abort
#from projectDAOskeleton import projectDAO
#import projectDAO
from projectDAO import projectDAO
#import pyautogui
#import deleteRow

app = Flask(__name__, static_url_path='', static_folder='.')
#app = Flask(__name__)

@app.route('/')
def index():
        return "Hello World ! Web Services and Applications Project"

# find by id
# curl http://127.0.0.1:5000/project/1

@app.route('/project/<int:id>', methods=['GET'])
def findbyid(id):
        return jsonify(projectDAO.findByID(id))

# getall
# curl http://127.0.0.1:5000/project

@app.route('/project', methods=['GET'])
def getall():
        return jsonify(projectDAO.getAll())

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"id\":5,\"name\":\"High Support Needs\",\"staff\":12}" http://127.0.0.1:5000/project
@app.route('/project', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    # other checking 
    project = {
        "id": request.json['id'],
        "name": request.json['name'],
        "area": request.json['area'],
    }
    addedproject = projectDAO.create(project)
    #pyautogui.hotkey('f5') #Simulates F5 key press = page refresh
    return jsonify(addedproject)

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
    projectDAO.update(id,foundProject)
    #pyautogui.hotkey('f5') #Simulates F5 key press = page refresh
    return jsonify(foundProject)    

@app.route('/project/<int:id>' , methods=['DELETE'])
def delete(id):
    projectDAO.delete(id)
    return jsonify({"done":True})
    #print("Delete done. Row " +id+ "was deleted successfully.")
    #return jsonify(projectDAO.delete(id))

@app.route('/map/<loc>')
def map(loc):
    geolocator = Nominatim(user_agent="MyApp")

    #loc = input("please enter City name: ") 
    location = geolocator.geocode(loc)
    lat = location.latitude
    long = location.longitude

    gmap = gmplot.GoogleMapPlotter(lat, long, 10)

    # Add a marker
    gmap.marker(lat, long, 'cornflowerblue')

    # Draw map into HTML file
    gmap.draw("my_map.html")

    filename = 'file:///'+os.getcwd()+'/' + 'my_map.html'
    webbrowser.open_new_tab(filename)

if __name__ == "__main__":
    app.run(debug = True)