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

	string = picture_byte.decode()

	return string


# Register (POST) route
####################################################
@user.route('/register', methods=['POST'])
def register():

	print('REGISTER HIT')

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









# show/GET route (show profile)
####################################################
@user.route('/<id>', methods=['GET'])
def show_user(id):

	try:

		user = User.get_by_id(id)
		user_dict = model_to_dict(user)

		return jsonify(data = user_dict, status={'code': 200, 
			'message': 'User found on resource.'})

	except DoesNotExist:

		return jsonify(data={}, status={'code': 401, 
			'message': 'User not found on resource.'})


# edit/PUT route (edit profile)
####################################################
@user.route('/<id>', methods=['PUT'])
def update_user(id):

	try:

		# multipart form data (text fields and an image file)

		# text fields

		payload = request.form.to_dict()

		# image file

		# it seems there would need to be a way to determine
		# if the image has been changed or not by the user.
		# If no change, code wrapped in #------# below is not needed
		# (because the database already holds an encoded image,
		# or there is no image loaded by the user)

		# Perhaps on edit page... 
		# user first clicks a "change image" button.
		# which returns a 'new_image' boolean back here thru the payload?
		# payload['new_image'] = True or False

		# On submit of the "change image" button, 
		# then we would display a "choose file" button?

		#--------------------------#
		if payload['new_image']:
			payload_file = request.files.to_dict()
			payload['image'] = base64.b64encode(payload_file['file'].read())
		#--------------------------#

		User.update(**payload).where(User.id == id)

		updated_user = User.get_by_id(id).to_dict()

		return jsonify(data=updated_user, status={'code': 200, 
			'message': 'User successfully updated.'})
		
	except DoesNotExist:

		return jsonify(data={}, status={'code': 401, 
			'message': 'User not found on resource.'})



