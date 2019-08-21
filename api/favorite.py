from models import Favorite

from flask import Blueprint, request, jsonify, url_for, send_file

from playhouse.shortcuts import model_to_dict

# set default url path for favorites (register blueprint in app.py)
favorite = Blueprint('favorites', 'favorite', url_prefix='/favorite')

# create/POST favorite
###############################################
@favorite.route('/', methods=['POST'])
def create_favorite:

	# must send media id with payload when favorite button clicked
	# payload includes media_id and timestamp
	payload = request.form.to_dict()
	payload['user_id'] = current_user

	favorite = Favorite.create(**payload)

	favorite_dict = model_to_dict(favorite)

	return jsonify(data=favorite_dict, status={"code": 200, 
		"message": "Resource added"})





