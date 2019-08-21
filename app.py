from flask import Flask, g 
from flask_cors import CORS
from flask_login import LoginManager
import models

from api.user import user

DEBUG = True
PORT = 8000

login_manager = LoginManager()

app = Flask(__name__)

# app.config.from_pyfile('./instance/config.py')

app.secret_key = 'SECRET_KEY'

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	try:
		return models.User.get(models.User.id == user_id)
	except models.DoesNotExist:
		return None

CORS(user, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(user)

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


if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)







