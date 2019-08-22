from models import User, Media, Comment, Favorite

import os
import sys
import secrets
from PIL import Image
import base64

from flask import Blueprint, request, jsonify, url_for, send_file

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

# set default url path for users (register blueprint in app.py)
user = Blueprint('users', 'user', url_prefix='/user')

def save_picture(form_picture):
	print(form_picture)

	# encode file as a string for storage in the database
	picture_byte = base64.b64encode(form_picture['file'].read())

	# print(str)

	string = picture_byte.decode()

	return 'data:image/png;base64,{}'.format(string)


# Register (POST) route
####################################################
@user.route('/register', methods=['POST'])
def register():

	payload = request.form.to_dict()

	if len(request.files.to_dict()):
		pay_file = request.files
		dict_file = pay_file.to_dict()
		payload['image'] = save_picture(dict_file)
	else:
		payload['image'] = '../static/images/default.jpg'		

	# multipart form data (text fields and an image file)

	payload['email'].lower()

	print(payload)

	try:

		User.get(User.email == payload['email'])

		return jsonify(data={}, status={'code': 401, 'message': 'A User with that email already exists'})

	except User.DoesNotExist:

		try:

			User.get(User.username == payload['username'])

			print('A User with that username already exists')

			return jsonify(data={}, status={'code': 401, 'message': 'A User with that username already exists'})

		except User.DoesNotExist:

			payload['password'] = generate_password_hash(payload['password'])

			user = User.create(**payload)

			login_user(user)

			user_dict = model_to_dict(user)

			del user_dict['password']

			print(user_dict)

			return jsonify(data=user_dict, status={'code': 201, 'message': 'Success'}) 

# Login (POST) route
####################################################
@user.route('/login', methods=['POST'])
def login():

	print('LOGIN')

	payload = request.form.to_dict()

	print(payload,'payload')

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


# Logout (GET) route
####################################################
@user.route('/logout', methods=['GET'])
def logout():
	logout_user()

	return jsonify(data={}, status={'code': 200, 'message': 'User logged out.'})


# show/GET route (show profile)
####################################################
@user.route('/<id>', methods=['GET'])
def show_user(id):

	try:

		user = User.get_by_id(id)

		medias = Media.select().where(Media.user_id == id)

		medias_dict = [model_to_dict(media) for media in medias]

		for media in medias_dict:
			comments = Comment.select().where(Comment.media_id == media['id'])
			comments_dict = [model_to_dict(comment) for comment in comments]
			media['comments'] = comments_dict

			favorites = Favorite.select().where(Favorite.media_id == media['id'])
			favorites_dict = [model_to_dict(favorite) for favorite in favorites]
			media['favorites'] = favorites_dict


		favorites = Favorite.select().where(Favorite.user_id == id)	

		favorites_media = [favorite.media_id for favorite in favorites]

		fav_dict = [model_to_dict(favorite) for favorite in favorites_media]

		# print(favorites_dict)

		for fav in fav_dict:
			comments = Comment.select().where(Comment.media_id == fav['id'])
			comments_dict = [model_to_dict(comment) for comment in comments]
			fav['comments'] = comments_dict
			print(fav, 'FAVS')

			favorites = Favorite.select().where(Favorite.media_id == fav['id'])
			favorites_dict = [model_to_dict(favorite) for favorite in favorites]
			fav['favorites'] = favorites_dict


		user_dict = model_to_dict(user)

		user_dict['posted_media'] = medias_dict
		user_dict['favorited_media'] = fav_dict

		# print(user_dict, 'user_dict')

		del user_dict['password']

	# 	#################
	# 	# Need to join with users posted media (with comments and fav counts), plus join to user's favorited media (with comments, fav counts). Also, comments need to join with user to associate username with each comment. 
	# 	#################

		return jsonify(data = user_dict, status={'code': 200, 
			'message': 'User found on resource.'})

	except User.DoesNotExist:

		return jsonify(data={}, status={'code': 401, 
			'message': 'User not found on resource.'})


# edit/PUT route (edit profile)
####################################################
@user.route('/<id>', methods=['PUT'])
def update_user(id):

	try:
		# get current user data populate image if not changed
		user = User.get_by_id(id)

		# multipart form data (text fields and an image file)

		# text fields
		payload = request.form.to_dict()

		# image file
		# check if new image file was submitted
		# if so, encode image for storage in the database
		if len(request.files.to_dict()):
			pay_file = request.files.to_dict()
			payload['image'] = save_picture(pay_file) 
		# do we need an else here?
		# else:
			# payload['image'] = user['image']

		payload['password'] = generate_password_hash(payload['password'])


		query = User.update(**payload).where(User.id == id)
		query.execute()

		updated_user = model_to_dict(User.get_by_id(id))

		return jsonify(data=updated_user, status={'code': 200, 
			'message': 'User successfully updated.'})
		
	except User.DoesNotExist:

		return jsonify(data={}, status={'code': 401, 
			'message': 'User not found on resource.'})

# destroy/DELETE route (delete user and all assoc data)
####################################################
@user.route('/<id>', methods=['DELETE'])
def delete_user(id):

	User.delete().where(User.id == id).execute()
	Media.delete().where(Media.user_id == id).execute()
	Favorite.delete().where(Favorite.user_id== id).execute()
	Comment.delete().where(Comment.user_id == id).execute()

	return jsonify(data={}, status={'code': 200,
		'message': 'User deleted from all resources'})





