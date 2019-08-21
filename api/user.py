from models import User

import os
import sys
import secrets
from PIL import Image
import base64

from flask import Blueprint, request, jsonify, url_for, send_file

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

# set default url path for users (register blueprint in app.py)
user = Blueprint('users', 'user', url_prefix='/user')

def save_picture(form_picture):
	print(form_picture)

	# encode file as a string for storage in the database
	picture_byte = base64.b64encode(form_picture['file'].read())

	# print(str)

	str = picture_byte.decode()

	return str


# Register (POST) route
####################################################
@user.route('/register', methods=['POST'])
def register():

	print('REGISTER HIT')
	url_id = ''

	for i, character in enumerate('https://www.youtube.com/watch?v=85-F7wkUaiM'):
		if i > len('https://www.youtube.com/watch?v=85-F7wkUaiM') - 12:
			print(character)
			url_id += character

	print(url_id, 'url_id')

	# multipart form data (text fields and an image file)
	payload = request.form.to_dict()

	pay_file = request.files
	dict_file = pay_file.to_dict()

	payload['email'].lower()
	payload['image'] = save_picture(dict_file)

	print(payload)

	try:

		User.get(User.email == payload['email'])

		return jsonify(data={}, status={'code': 401, 'message': 'A User with that email already exists'})

	except User.DoesNotExist:

		try:

			User.get(User.username == payload['username'])

			return jsonify(data={}, status={'code': 401, 'message': 'A User with that username already exists'})

		except User.DoesNotExist:

			payload['password'] = generate_password_hash(payload['password'])

			user = User.create(**payload)

			login_user(user)

			user_dict = model_to_dict(user)

			del user_dict['password']

			print(user_dict)

			return jsonify(data=user_dict, status={'code': 201, 'message': 'Success'}) 

# Login (GET) route
@user.route('/login', methods=['GET'])
def login():

	payload = request.form.to_dict()

	try:

		user = User.get(User.username == payload['username'])

		passwordCheck = check_password_hash(user.password, payload['password'])

		print(passwordCheck, 'passwordCheck')

		if not passwordCheck:
			# we reach this point if neither username nor pwd correct
			return jsonify(data={}, status={'code': 401, 'message': 'Username or password is incorrect.'})

		else:
			# we only reach this point if both username and pwd correct
			login_user(user)

			user_dict = model_to_dict(user)

			del user_dict['password']

			return jsonify(data=user_dict, status={'code': 200, 'message': 'user logged in!'})


	except User.DoesNotExist:

		# we reach this point if username does not exist
		return jsonify(data={}, status={'code': 401, 'message': 'Username or password is incorrect.'})







