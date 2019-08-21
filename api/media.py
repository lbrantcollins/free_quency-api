from models import Media, Comment, Favorite

from flask import Blueprint, request, jsonify, url_for, send_file
from flask_login import current_user

from playhouse.shortcuts import model_to_dict

# set default url path for media (register blueprint in app.py)
media = Blueprint('medias', 'media', url_prefix='/media')

@media.route('/', methods=['POST'])
def add_media():

	try:
		payload = request.form.to_dict()
		print('ADD MEDIA')

		payload['user_id'] = str(model_to_dict(current_user)['id'])


		if 'www.youtube.com/watch?v=' in payload['url']:
			payload['media_type'] = 'video'
		else:
			return jsonify(data={}, status={'code': 401, 'message': 'URL input is not valid.'})
		
		if payload['media_type'] == 'video':


			v_location = payload['url'].index('v')

			eq_location = payload['url'].index('=')

			if eq_location == v_location + 1:
				url_id = payload['url'][eq_location + 1: eq_location + 12]
			else:
				return jsonify(data={}, status={'code': 401, 'message': 'URL input is not valid.'})


			payload['full_html'] = '<iframe width="560" height="315" src="https://www.youtube.com/embed/{}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'.format(url_id)

			payload['thumbnail_html'] = '<img src="http://i.ytimg.com/vi/{}/maxresdefault.jpg" />'.format(url_id)


		print(payload,'payload')
		media = Media.create(**payload)

		media_dict = model_to_dict(media)

		return jsonify(data=media_dict, status={'code': 201, 'message': 'Success'}) 
	except:
		return jsonify(data={}, status={'code': 401, 'message': 'Something went wrong!'})


@media.route('/', methods=['GET'])
def get_all_media():

	try:
		all_media = [ model_to_dict(media) for media in Media.select()]

		return jsonify(data=all_media, status={"code": 200, "message": "Success"})

	except Media.DoesNotExist:
		return jsonify(data={}, status={"code": 401, "message": "There was an error getting the resource"})

@media.route('/<id>', methods=['GET'])
def get_one_media(id):

	try:
		media = model_to_dict(Media.get_by_id(id))

		return jsonify(data=media, status={"code": 200, "message": "Success"})

	except Media.DoesNotExist:
		return jsonify(data={}, status={"code": 401, "message": "There was an error getting the resource"})


@media.route('/<id>', methods=['Delete'])
def delete_media(id):

	try:
		query = Media.delete().where(Media.id == id)
		query.execute()

		query2 = Comment.delete().where(Comment.media_id == id)
		query2.execute()

		query3 = Favorite.delete().where(Favorite.media_id == id)
		query3.execute()

		return jsonify(data={}, status={"code": 200, "message": "resource deleted"})

	except Media.DoesNotExist:
		return jsonify(data={}, status={"code": 401, "message": "There is no media at that id"})


@media.route('/<id>', methods=['PUT'])
def update_media(id):

	payload = request.form.to_dict()

	if 'www.youtube.com/watch?v=' in payload['url']:
		payload['media_type'] = 'video'
	else:
		return jsonify(data={}, status={'code': 401, 'message': 'URL input is not valid.'})
	
	if payload['media_type'] == 'video':


		v_location = payload['url'].index('v')

		eq_location = payload['url'].index('=')

		if eq_location == v_location + 1:
			url_id = payload['url'][eq_location + 1: eq_location + 12]
		else:
			return jsonify(data={}, status={'code': 401, 'message': 'URL input is not valid.'})


		payload['full_html'] = '<iframe width="560" height="315" src="https://www.youtube.com/embed/{}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'.format(url_id)

		payload['thumbnail_html'] = '<img src="http://i.ytimg.com/vi/{}/maxresdefault.jpg" />'.format(url_id)


	query = Media.update(**payload).where(Media.id == id)
	query.execute()

	media_dict = model_to_dict(Media.get_by_id(id))

	return jsonify(data=media_dict, status={'code': 201, 'message': 'Success'}) 

