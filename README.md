#Graphlopedia Flask App

This app requires [Python 3](https://www.python.org/downloads/ "Download Python!") and several dependencies (all built around [Flask](http://flask.pocoo.org/ "Flask") ) to run.

These dependencies can be installed by running the following command (once [Python 3](https://www.python.org/downloads/ "Download Python!") is installed):

```
$ pip install flask flask-login Flask-WTF Flask-PyMongo
```

also, can install by downloading the included requirements.txt (coming soon!!!) file and running the below command from the same directory:

```
$ pip -r requirements.txt
```

Once you've taken care of all the dependencies, you can run graph_app from you computer by running the commands below:

```
$ export FLASK_DEBUG=1
$ python runserver.py
 * Running on http://127.0.0.1:5000
```

On Windows, `export` should be `set`. These commands should be run from the same directory as the file `runserver.py`.
