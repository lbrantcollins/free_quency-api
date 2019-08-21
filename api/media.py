from models import Media

from flask import Blueprint, request, jsonify, url_for, send_file

from playhouse.shortcuts import model_to_dict

# set default url path for media (register blueprint in app.py)
media = Blueprint('medias', 'media', url_prefix='/media')

@media.route('/', methods=['POST'])
def add_media():

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


	media = Media.create(**payload)

	media_dict = model_to_dict(media)

	return jsonify(data=media_dict, status={'code': 201, 'message': 'Success'}) 


@media.route('/', methods=['GET'])
def get_all_media():

	try:
		all_media = [ model_to_dict(media) for media in Media.select()]

		return jsonify(data=all_media, status={"code": 200, "message": "Success"})

	except models.DoesNotExist:
		return jsonify(data={}, status={"code": 401, "message": "There was an error getting the resource"})



