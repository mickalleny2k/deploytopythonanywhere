from flask import Flask
#from projectDAOskeleton import projectDAO
#import projectDAO
#from projectDAO import projectDAO
#import deleteRow

#app = Flask(__name__, static_url_path='', static_folder='.')
app = Flask(__name__)

@app.route('/')
def index():
        return "Web Services and Applications Project"

if __name__ == "__main__":
    app.run(debug = True)