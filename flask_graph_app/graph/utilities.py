from graph import app
from flask_login import UserMixin, current_user
from urllib.parse import urlparse, urljoin
from flask import g, flash
from flask_pymongo import PyMongo
from pymongo import DESCENDING
from werkzeug.security import check_password_hash
from ast import literal_eval as make_obj

mongo = PyMongo(app)

def _connect_db():
	return mongo.db

def get_db():
	if not hasattr(g, 'db'):
		g.db = _connect_db()
	return g.db

def get_graph(gid):
	db = get_db()
	graph = db.graphs.find_one({'name':gid})
	gJSON = {}
	
	if graph:
		#### Prep JSON for JS & D3
		gJSON['nodes'] = []
		gJSON['edges'] = []
		for node in graph['vertices']:
			gJSON['nodes'].append({'name': node, "group": 1})
		for edge in graph['edges']: 
			gJSON['edges'].append({'source': edge[0], 'target': edge[1], 'weight': 1})

		####
		# print(gJSON)
	
	return graph, gJSON

def put_graph(g):
	title = g['title']
	vertices = make_obj(g['vertices']) 
	edges = make_obj(g['edges'])
	deg_seq = make_obj(g['deg_seq'])
	# author = [ g['authors'] ]
	refs = []
	comments = []
	links = []
	if current_user.is_authenticated:
		name = current_user.name
		email = current_user.email
		author = [{'name':name, 'email':email}]
	elif 'authors' in g and g['authors']:
		author = [ g['authors'] ]
	if 'refs' in g and g['refs']:
		refs = make_obj(g['refs'])
	if 'comments' in g and g['comments']:
		comments = make_obj(g['comments'])
	if 'links' in g and g['links']:
		links = make_obj(g['links'])
	flash('Data succesfully received!', 'success')
	db = get_db()
	max_name = db.graphs.find().sort('name', DESCENDING).limit(1)[0]['name']
	new_max_name = 'G' + str(int(max_name[1:]) + 1).zfill(6)
	# print(max_name, new_max_name)
	res = db.graphs.insert_one({'name':new_max_name, 'title':title, 'vertices':vertices, 'edges':edges, 'degrees': deg_seq,
						'authors':author, 'references':refs, 'comments': comments, 'links':links})
	if res:
		flash('Graph successfully added!', 'success')
		flash('New Graph ID: %s' % new_max_name, 'success')
	else:
		flash('Unable to add graph to database: Internal Server Error')

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'db'):
		# log that database has been closed
		print("database connection closed")

def is_safe_url(host_url, target):
    ref_url = urlparse(host_url)
    test_url = urlparse(urljoin(host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

class DuplicateUserError(ValueError):
	pass


class User(UserMixin):
	def __init__(self, email, name, pass_hash):
		self.email = email
		self.name = name
		self.pass_hash = pass_hash

	def get_id(self):
		return self.email

	def get_name(self):
		return self.name

	def validate_login(self, passw):
		return check_password_hash(self.pass_hash, passw)

	def change_pass(self, new_pass_hash):
		db = get_db()
		return db.users.update_one({'email':self.email}, {'$set':{'hash_pass':new_pass_hash}})

	@staticmethod
	def get(email):
		db = get_db()
		user = db.users.find_one({'email': email})
		if user:
			return User(user['email'], user['name'], user['hash_pass'])
		else:
			return None

	@staticmethod
	def rm_user(email):
		db = get_db()
		return db.users.delete_one({'email':email})

	@staticmethod
	def create_new_user(email, name, pass_hash):
		if User.get(email):
			raise DuplicateUserError

		db = get_db()
		return db.users.insert_one({'name': name, 'email':email, 'hash_pass': hash_pass})
	
	@staticmethod
	def validate_any_login(pass_hash, passw):
		return check_password_hash(pass_hash, passw)


