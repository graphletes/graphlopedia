from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
def home_search():
	return render_template('index.html')

@app.route('/search')
def make_search():
	pass

if __name__ == '__main__':
	app.run()