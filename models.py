from peewee import *
from flask_login import UserMixin
import datetime

DATABASE = SqliteDatabase('free_quency.sqlite')

class User(UserMixin, Model):
	username = CharField()
	email = CharField()
	password = CharField()
	image = CharField()
	about_me = CharField(null=True)
	created_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

class Media(Model):
	user_id = ForeignKeyField(User, backref='posts')
	title = CharField()
	description = CharField(null=True)
	url = CharField()
	media_type = CharField()
	full_html = CharField()
	thumbnail_html = CharField()
	created_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

class Favorite(Model):
	user_id = ForeignKeyField(User, backref='favorites')
	media_id = ForeignKeyField(Media, backref='favorites')
	created_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

class Comment(Model):
	user_id = ForeignKeyField(User, backref='comments')
	media_id = ForeignKeyField(Media, backref='comments')
	content = CharField()
	created_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Media, Favorite, Comment], safe=True)
	print('tables created')
	DATABASE.close()







