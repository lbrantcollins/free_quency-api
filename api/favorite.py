from models import Favorite

from flask import Blueprint, request, jsonify, url_for, send_file
from flask_login import current_user

from playhouse.shortcuts import model_to_dict

# set default url path for favorites (register blueprint in app.py)
favorite = Blueprint('favorites', 'favorite', url_prefix='/favorite')

# create/POST favorite
###############################################
@favorite.route('/', methods=['POST'])
def create_favorite():

	# must send media id with payload when favorite button clicked
	# the following assumes payload includes media_id and timestamp
	payload = request.form.to_dict()
	current_user_id = model_to_dict(current_user)['id']
	payload['user_id'] = current_user_id

	favorite = Favorite.create(**payload)

	favorite_dict = model_to_dict(favorite)

	return jsonify(data=favorite_dict, status={"code": 200, 
		"message": "Resource added"})

# DELETE a favorite ("un-favorite" a media entry)
@favorite.route('/<id>', methods=['DELETE'])
def delete_favorite(id):

	query = Favorite.delete().where(Favorite.id == id)
	query.execute()

	return jsonify(data={}, status={"code": 200, 
		"message": "Resource deleted"})







