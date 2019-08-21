from models import Comment

from flask import Blueprint, request, jsonify, url_for

from playhouse.shortcuts import model_to_dict

from flask_login import current_user

comment = Blueprint('comments', 'comment', url_prefix='/comment')

@comment.route('/', methods=["POST"])
def add_comment():

	payload = request.form.to_dict()

	payload['user_id'] = model_to_dict(current_user)['id']

	print(payload, current_user)

	new_comment = model_to_dict(Comment.create(**payload))

	return jsonify(data=new_comment, status={'code': 201, 'message': 'Success: Comment created!'}) 

@comment.route('/<id>', methods=['DELETE'])
def delete_comment(id):

	query = Comment.delete().where(Comment.id == id)
	query.execute()

	return jsonify(data={}, status={'code': 201, 'message': 'Successful deletion'}) 

@comment.route('/', methods=['GET'])
def get_comments():
	comments = [model_to_dict(comment) for comment in Comment.select()]


	return jsonify(data=comments, status={'code': 201, 'message': 'Success'})



