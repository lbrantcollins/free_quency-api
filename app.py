from flask import Flask, g 
from flask_cors import CORS
from flask_login import LoginManager
import models
import os

from api.user import user
from api.media import media
from api.favorite import favorite
from api.comment import comment


DEBUG = True
PORT = 8000

login_manager = LoginManager()

app = Flask(__name__, static_url_path="", static_folder="static")

# remove this later
app.secret_key = os.environ.get('REACT_APP_SECRET_KEY') or 'asdkfj;lsjf'

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):

	try:
		return models.User.get(models.User.id == user_id)
	except models.DoesNotExist:
		return None

# CORS
CORS(user, origins=['http://localhost:3000', "https://freequency.herokuapp.com/"], supports_credentials=True)
CORS(media, origins=['http://localhost:3000', "https://freequency.herokuapp.com/"], supports_credentials=True)
CORS(favorite, origins=['http://localhost:3000', "https://freequency.herokuapp.com/"], supports_credentials=True)
CORS(comment, origins=['http://localhost:3000', "https://freequency.herokuapp.com/"], supports_credentials=True)

app.register_blueprint(user)
app.register_blueprint(media)
app.register_blueprint(favorite)
app.register_blueprint(comment)

@app.before_request
def before_request():
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	g.db.close()
	return response

@app.route('/')
def index():
	return 'FREE_QUENCYYYYYYY'

if 'ON_HEROKU' in os.environ:
    print('hitting ')
    models.initialize

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)





