from models import Media

from flask import Blueprint, request, jsonify, url_for, send_file

from playhouse.shortcuts import model_to_dict

# set default url path for media (register blueprint in app.py)
user = Blueprint('medias', 'media', url_prefix='/media')

@user.route('/', methods=['POST'])
def add_media():

	payload = request.form.to_dict()

	if 'youtube.com' in payload['url']:
		payload['type'] = 'video'
	elif 'soundcloud.com' in payload['url']:
		payload['type'] = 'audio'
	else:
		return jsonify(data={}, status={'code': 401, 'message': 'URL input is not valid.'})

	# payload['user_id'] = ????
	

	if payload['type'] == 'video':


		url_id = ''

		for i, character in enumerate(payload['url']):
			if i > len(payload['url']) - 12:
				url_id += character


		payload['full_html'] = '<iframe width="560" height="315" src="https://www.youtube.com/embed/{}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'.format(url_id)

		payload['thumbnail_html'] = '<img src="http://i.ytimg.com/vi/{}/maxresdefault.jpg" />'.format(url_id)

	else:

		# SOUNDS CLOUD API HERE https://developers.soundcloud.com/docs/api/guide#playing


	media = Media.create(**payload)

	media_dict = model_to_dict(media)

	return jsonify(data=media_dict, status={'code': 201, 'message': 'Success'}) 




