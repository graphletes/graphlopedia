import os
import json
import codecs
import ast

from flask import Flask, request, g, render_template, url_for, redirect, flash, session
from flask_pymongo import PyMongo
import flask_login

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('GRAPH_SETTINGS')
# app.secret_key = 'LOLOLOLOLOL'

mongo = PyMongo(app)


class User(flask_login.UserMixin):
	pass

def connect_db():
	return mongo.db

def get_db():
	if not hasattr(g, 'db'):
		g.db = connect_db()
	return g.db

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'db'):
		# log that database has been closed
		print("database connection closed")

@app.route('/')
def index():
	return render_template('index.html')

login_manager = flask_login.LoginManager()
# login_manager.init_app(app)

@app.route('/search', methods=['GET'])
def make_search():
	if request.method == 'GET':
		results = []
		close_results = []
		print('getting method')
		# db = mongo.db
		db = get_db()
		try:
			deg_seq = request.args['deg_seq']
			# print(deg_seq)
			if not deg_seq:
				flash('Please enter a query.')
				return redirect(url_for('index'))

			nums = deg_seq.split(',')
			# print(nums)
			seq = [int(num.strip()) for num in nums]
			# print(seq)
			
			c = db.graphs.find({"degrees":seq})
			
			for g in c:
				results.append(g)

			# if not results:
			c = db.graphs.aggregate([
									{'$match' : {'degrees' : {'$size' : len(seq)}}},
									{'$sort' : {'name' : 1}}
									])

			for g in c:
				if g not in results:
					close_results.append(g)
			
		except ValueError:
			flash('Please enter only integers, commas, and whitespace for degree sequence query.')
			return redirect(url_for('index'))
		
		return render_template('search.html', results=results, close_results=close_results, query=deg_seq)	
	else:
		return render_template('404.html'), 404

@app.route('/graph', methods=['GET'])
def get_graph():
	db = mongo.db
	gid = request.args['gid']	
	graph = db.graphs.find_one({'name':gid})

	if graph:
		#### Prep JSON for JS & D3
		gJSON = {'nodes' : [], 'edges': []}
		for node in graph['vertices']:
			gJSON['nodes'].append({'name': node, "group": 1})
		for edge in graph['edges']: 
			gJSON['edges'].append({'source': edge[0], 'target': edge[1], 'weight': 1})
		####
		return render_template('graph.html', graph=graph, gJSON=gJSON)
	else:
		return render_template('404.html'), 404

@app.route('/admin')
def admin_page():
	return render_template('admin.html')

@app.route('/add', methods=['POST'])
def add_graph():
	if request.method == 'POST':
		try:
			title = [ request.form['title'] ]
			vertices = ast.literal_eval(request.form['vertices']) 
			edges = ast.literal_eval(request.form['edges'])
			deg_seq = ast.literal_eval(request.form['deg_seq'])
			author = [ request.form['authors'] ]
			refs = []
			comments = []
			links = []
			if 'refs' in request.form:
				refs = ast.literal_eval(request.form['refs'])
			if 'comments' in request.form:
				comments = ast.literal_eval(request.form['comments'])
			if 'links' in request.form:
				links = ast.literal_eval(request.form['links'])
			flash('Data succesfully received!')
			return redirect(url_for('admin_page'))
		except KeyError:
			flash('Please enter all req\'d fields in the proper format (see placeholder text).')
			return redirect(url_for('admin_page'))
		except ValueError:
			flash('Please enter all req\'d fields in the proper format (see placeholder text).')
			return redirect(url_for('admin_page'))
	else:
		return render_template('404.html'), 404



@login_manager.user_loader
def user_loader(email):
	user = User()
	user.id = email
	return user

@login_manager.request_loader
def request_loader(request):
	email = request.form.get('email')

	user = User()
	user.id = email

	user.is_authenticated = request.form['pw'] == 'password'

# def array_cmp(a, b):
# 	if type(a) != list or type(b) != list:
# 		return False
# 	elif len(a) == 0 or len(b) == 0:
# 		return False
# 	elif len(a) != len(b):
# 		return False
# 	else:
# 		for i in range(len(a)):
# 			if a[i] != b[i]:
# 				return False
# 	return True

if __name__ == '__main__':
	app.run()