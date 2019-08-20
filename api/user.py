import models

import os
import sys
import secrets
from PIL import Image
import base64

from flask import Blueprint, request, jsonify, url_for, send_file

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user', url_prefix='/user')

def save_picture(form_picture):
	print(form_picture)


	str = base64.b64encode(form_picture['file'].read())

	print(str)



@user.route('/register', methods=['POST'])
def register():

	print('REGISTER HIT')

	pay_file = request.files

	payload = request.form.to_dict()
	dict_file = pay_file.to_dict()

	save_picture(dict_file)

	# payload['email'].lower()

	# try:

	# 	models.User.get(models.User.email == payload['email'])

	# 	return jsonify(data={}, status={'code': 401, 'message': 'A User with that email already exists'})

	# except models.DoesNotExist:

	# 	try:

	# 		models.User.get(models.User.username == payload['username'])

	# 		return jsonify(data={}, status={'code': 401, 'message': 'A User with that username already exists'})

	# 	except models.DoesNotExist:

	# 		payload['password'] = generate_password_hash(payload['password'])

	# 		user = models.User.create(**payload)

	# 		login_user(user)

	# 		user_dict = model_to_dict(user)

	# 		del user_dict['password']

	# 		return jsonify(data=user_dict, status={'code': 201, 'message': 'Success'}) 

@user.route('/login', methods=['GET'])
def login():

	payload = request.form.to_dict()

	try:

		user = models.User.get(models.User.username == payload['username'])

		passwordCheck = check_password_hash(user.password, payload['password'])

		print(passwordCheck, 'passwordCheck')

		if not passwordCheck:
			return jsonify(data={}, status={'code': 401, 'message': 'Username or password is incorrect.'})

		else:

			login_user(user)

			user_dict = model_to_dict(user)

			del user_dict['password']

			return jsonify(data=user_dict, status={'code': 200, 'message': 'user logged in!'})


	except models.DoesNotExist:

		return jsonify(data={}, status={'code': 401, 'message': 'No user exists with that username'})







