import flask_login

from graph import app
from graph.forms import AddUserForm, LoginForm
from graph.utilities import DuplicateUserError, User, is_safe_url, get_db, get_graph, put_graph
from graph.search import *

from flask import request, g, render_template, url_for, redirect, flash, session
from werkzeug.security import generate_password_hash

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search', methods=['GET'])
def make_search():
	if request.method == 'GET':
		if 'prev' in request.args and request.args['prev']:
			if is_safe_url(request.host_url, request.args['prev']):
				return redirect(request.args['prev'])
		q = None
		results = None
		close_results = None
		
		if 'deg_seq' in request.args:
			
			try:
				q = validate_query(request.args['deg_seq'])
				if not isinstance(q, str):
					return q
				results, close_results = degree_search(q)
			except ValueError:
				flash('Please enter only integers, commas, and whitespace for degree sequence query.')
				return redirect(url_for('index'))

		elif 'title' in request.args:
			
			q = validate_query(request.args['title'])
			if not isinstance(q, str):
				return q
			results, close_results = title_search(q)
		
		elif 'name' in request.args:
			
			q = validate_query(request.args['name'])
			if not isinstance(q, str):
				return q
			return name_search(q)
		
		return render_template('search.html', results=results, close_results=close_results, query=q)	
	
	else:
		return render_template('404.html'), 404

@app.route('/graph', methods=['GET'])
def graph():
	if 'gid' in request.args:
		q = validate_query(request.args['gid'])
		if not isinstance(q, str):
				return q
		graph, gJSON = get_graph(q)

		if graph:
			return render_template('graph.html', graph=graph, gJSON=gJSON)
	
	return render_template('404.html'), 404

@app.route('/user', methods=['GET', 'POST'])
def user():
	if request.method == 'GET' and 'uid' in request.args:
		flash('Accessing user w/ ID: %s' % request.args['uid'].strip())
	return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
	au_form = AddUserForm(prefix='add')
	if au_form.validate_on_submit():
		email = au_form.email.data
		name = au_form.name.data.title()
		hash_pass = generate_password_hash(au_form.pass1.data)
		res = None
		try:
			res = User.create_new_user(email, name, hash_pass)
		except DuplicateUserError:
			flash('A user already exists for email: ' + email)
			return redirect(url_for('admin_page'))

		if res:
			flash('User successfully added.', 'success')
		else:
			flash('Unable to add user.')
	return render_template('admin.html', au_form = au_form)

@app.route('/add', methods=['POST'])
def add_graph():
	if request.method == 'POST':
		try:
			put_graph(request.form)
		except (KeyError, ValueError, SyntaxError):
			flash('Please enter all req\'d fields in the proper format (see placeholder text).')
		return redirect(url_for('admin_page'))
	else:
		return render_template('404.html'), 404

@app.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm(request.form)
	# flash(form.errors)
	if request.method == 'POST' and form.validate():
		user = User.get(form.email.data)
		if user and user.validate_login(form.password.data):
			flask_login.login_user(user)
			flash('Successfully logged in! Welcome %s.' % (user.get_name()), 'success')
			nxt = request.args.get('next')
			if not is_safe_url(request.host_url, nxt):
				return render_template('404.html'), 404
			return redirect(nxt or url_for('index'))
		else:
			flash('Invalid email or password.')
	return render_template('login.html', form=form)


@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    flash('Successfully logged out.', 'success')
    nxt = request.referrer
    if not is_safe_url(request.host_url, nxt):
    	return render_template('index')
    return redirect(nxt)