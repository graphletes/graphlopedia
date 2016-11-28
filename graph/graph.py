# import os
# import json
# import codecs
# import ast
# from datetime import timedelta

# from flask import Flask, request #, g, render_template, url_for, redirect, flash, session
# from urllib.parse import urlparse, urljoin
# from flask_pymongo import PyMongo
# import flask_login

# from werkzeug.security import generate_password_hash, check_password_hash
# from pymongo import DESCENDING
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Email, Length, EqualTo
# from wtforms.csrf.session import SessionCSRF


# app = Flask(__name__)
# app.config.from_object(__name__)
# app.config.from_envvar('GRAPH_SETTINGS')
# app.secret_key = 'LOLOLOLOLOL'

# mongo = PyMongo(app)
# lm = flask_login.LoginManager()
# lm.init_app(app)
# lm.login_view = 'login'

# def connect_db():
# 	return mongo.db

# def get_db():
# 	if not hasattr(g, 'db'):
# 		g.db = connect_db()
# 	return g.db

# def is_safe_url(target):
#     ref_url = urlparse(request.host_url)
#     test_url = urlparse(urljoin(request.host_url, target))
#     return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

# @lm.user_loader
# def user_loader(email):
# 	u = User.get(email)
# 	return u

# class User(flask_login.UserMixin):
# 	def __init__(self, username):
# 		self.username = username

# 	def get(email):
# 		db = get_db()
# 		user = db.users.find_one({'email': email})
# 		if user:
# 			return User(user['email'])
# 		else:
# 			return None

# 	def get_id(self):
# 		return self.username

# 	@staticmethod
# 	def validate_login(pass_hash, passw):
# 		return check_password_hash(pass_hash, passw)

# class BaseForm(FlaskForm):
# 	class Meta:
# 		csrf = True
# 		csrf = SessionCSRF
# 		csrf_secret = app.config['CSRF_SECRET_KEY']
# 		csrf_time_limit = timedelta(minutes=20)

# 		@property
# 		def csrf_context(self):
# 			return session

# class LoginForm(FlaskForm):
# 	# def __init__(self, csrf_enabled=False, *args, **kwargs):
# 	# 	super(LoginForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)
# 	email = StringField('email', validators=[DataRequired(), Email()])
# 	password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=25)])

# class AddUserForm(FlaskForm):
# 	name = StringField('Name', validators=[DataRequired(), Length(max=25)], render_kw={"placeholder": "John Doe", "class": "texti"})
# 	email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "johndoe@example.com", "class": "texti"})
# 	pass1 = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=25), EqualTo('pass2', message='Passwords must match.')], render_kw={"class": "texti"})
# 	pass2 = PasswordField('Confirm Password', validators=[DataRequired()], render_kw={"class": "texti"})
# 	submit = SubmitField('submit', render_kw={'value':'Add!'})

# @app.teardown_appcontext
# def close_db(error):
# 	if hasattr(g, 'db'):
# 		# log that database has been closed
# 		print("database connection closed")

# @app.route('/')
# def index():
# 	return render_template('index.html')

# @app.route('/search', methods=['GET'])
# def make_search():
# 	if request.method == 'GET':
# 		results = []
# 		close_results = []
# 		# print('getting method')
# 		db = get_db()
# 		if 'deg_seq' in request.args:
# 			try:
# 				q = request.args['deg_seq']
# 				if not q:
# 					flash('Please enter a query.')
# 					return redirect(url_for('index'))

# 				nums = q.split(',')
# 				seq = [int(num.strip()) for num in nums]
				
# 				c = db.graphs.aggregate([
# 										{'$match': {'degrees' : seq}},
# 										{'$sort': {'name' : 1}}
# 										])
				
# 				for g in c:
# 					results.append(g)

# 				c = db.graphs.aggregate([
# 										{'$match' : {'degrees' : {'$size' : len(seq)}}},
# 										{'$sort' : {'degrees' : 1}}
# 										])

# 				for g in c:
# 					if g not in results:
# 						close_results.append(g)
				
# 			except ValueError:
# 				flash('Please enter only integers, commas, and whitespace for degree sequence query.')
# 				return redirect(url_for('index'))

# 		elif 'title' in request.args:
# 			q = request.args['title'].strip()
# 			if not q:
# 				flash('Please enter a query.')
# 				return redirect(url_for('index'))

# 			c = db.graphs.aggregate([
# 									{'$match': {'title' : q}},
# 									{'$sort': {'name' : 1}}
# 									])
			
# 			for g in c:
# 				results.append(g)

# 			c = db.graphs.aggregate([
# 									{'$match' : {'$text' : {'$search' : q}}},
# 									{'$sort' : { 'score': { '$meta': "textScore" } }}
# 									])

# 			for g in c:
# 				if g not in results:
# 					close_results.append(g)

# 			print(results, close_results)
# 		elif 'name' in request.args:
# 			q = request.args['name'].strip()
# 			if not q:
# 				flash('Please enter a query.')
# 				return redirect(url_for('index'))

# 			c = db.graphs.find_one({'name': q})

# 			if not c:
# 				flash('Invalid ID.')
# 				return redirect(url_for('index'))

# 			return redirect(url_for('get_graph', gid=q))


# 		return render_template('search.html', results=results, close_results=close_results, query=q)	
# 	else:
# 		return render_template('404.html'), 404

# @app.route('/graph', methods=['GET'])
# def get_graph():
# 	db = get_db()
# 	if 'gid' in request.args:
# 		gid = request.args['gid']	
# 		graph = db.graphs.find_one({'name':gid})

# 		if graph:
# 			#### Prep JSON for JS & D3
# 			gJSON = {'nodes' : [], 'edges': []}
# 			for node in graph['vertices']:
# 				gJSON['nodes'].append({'name': node, "group": 1})
# 			for edge in graph['edges']: 
# 				gJSON['edges'].append({'source': edge[0], 'target': edge[1], 'weight': 1})
# 			####
# 			return render_template('graph.html', graph=graph, gJSON=gJSON)
	
# 	return render_template('404.html'), 404

# @app.route('/admin', methods=['GET', 'POST'])
# def admin_page():
# 	au_form = AddUserForm(prefix='add')
# 	if au_form.validate_on_submit():
# 		email = au_form.email.data
		
# 		if User.get(email):
# 			flash('A user already exists for email: ' + email)
# 			return redirect(url_for('admin_page'))

# 		name = au_form.name.data
# 		hash_pass = generate_password_hash(au_form.pass1.data)
# 		db = get_db()
# 		res = db.users.insert_one({'name': name, 'email':email, 'hash_pass': hash_pass})
# 		if res:
# 			flash('User successfully added.', 'success')
# 		else:
# 			flash('Unable to add user.')
# 	return render_template('admin.html', au_form = au_form)

# @app.route('/add_user', methods=['GET','POST'])
# @flask_login.login_required
# def add_user():
# 	if request.method == 'POST':
# 		try:
# 			name = request.form['name']
# 			email = request.form['email']
# 			pass1 = generate_password_hash(request.form['pass1'])
# 			pass2 = generate_password_hash(request.form['pass2'])
# 			if pass2 != pass1:
# 				flash('Passwords do not match.')
# 				return redirect(url_for('admin_page'))
# 		except KeyError:
# 			flash('Please enter all fields')
# 			return redirect(url_for('admin_page'))
# 	return redirect(url_for('index'))

# @app.route('/add', methods=['POST'])
# def add_graph():
# 	if request.method == 'POST':
# 		try:
# 			title = request.form['title']
# 			vertices = ast.literal_eval(request.form['vertices']) 
# 			edges = ast.literal_eval(request.form['edges'])
# 			deg_seq = ast.literal_eval(request.form['deg_seq'])
# 			author = [ request.form['authors'] ]
# 			refs = []
# 			comments = []
# 			links = []
# 			if 'refs' in request.form and request.form['refs']:
# 				refs = ast.literal_eval(request.form['refs'])
# 			if 'comments' in request.form and request.form['comments']:
# 				comments = ast.literal_eval(request.form['comments'])
# 			if 'links' in request.form and request.form['links']:
# 				links = ast.literal_eval(request.form['links'])
# 			flash('Data succesfully received!', 'success')
# 			db = get_db()
# 			max_name = db.graphs.find().sort('name', DESCENDING).limit(1)[0]['name']
# 			new_max_name = 'G' + str(int(max_name[1:]) + 1).zfill(6)
# 			print(max_name, new_max_name)
# 			res = db.graphs.insert_one({'name':new_max_name, 'title':title, 'vertices':vertices, 'edges':edges, 'degrees': deg_seq,
# 								'authors':author, 'references':refs, 'comments': comments, 'links':links})
# 			if res:
# 				flash('Graph successfully added!', 'success')
# 			else:
# 				flash('Unable to add graph to database: Internal Server Error')
# 		except (KeyError, ValueError):
# 			flash('Please enter all req\'d fields in the proper format (see placeholder text).')
# 		return redirect(url_for('admin_page'))
# 	else:
# 		return render_template('404.html'), 404

# @app.route('/login', methods=['GET','POST'])
# def login():
# 	form = LoginForm(request.form)
	
# 	# print(request.form, request.method, form.validate_on_submit())
# 	# flash(form.errors)
# 	if request.method == 'POST' and form.validate():
# 		db = get_db()
# 		user = db.users.find_one({'email': form.email.data})
# 		# print(generate_password_hash(form.password.data), form.password.data)
# 		if user and User.validate_login(user['hash_pass'], form.password.data):
# 			user_o = User(user['email'])
# 			flask_login.login_user(user_o)
# 			flash('Successfully logged in.', 'success')
# 			nxt = request.args.get('next')
# 			if not is_safe_url(nxt):
# 				return render_template('404.html'), 404
# 			# print(nxt, url_for(nxt))
# 			return redirect(nxt or url_for('index'))
# 		else:
# 			flash('Invalid email or password.')
# 	return render_template('login.html', form=form)


# @app.route("/logout")
# @flask_login.login_required
# def logout():
#     flask_login.logout_user()
#     flash('Successfully logged out.', 'success')
#     return redirect(url_for('index'))


# @login_manager.request_loader
# def request_loader(request):
# 	email = request.form.get('email')

# 	user = User()
# 	user.id = email

# 	user.is_authenticated = request.form['pw'] == 'password'

# if __name__ == '__main__':
# 	app.run()