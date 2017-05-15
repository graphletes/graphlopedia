from flask import flash, redirect, url_for
from graph.utilities import get_db

def validate_query(q):
	q = q.strip()
	if not q:
		flash('Please enter a valid query.')
		return redirect(url_for('index'))
	return q

def degree_search(q):
	results = []
	close_results = []
	db = get_db()

	nums = q.split(',')
	seq = [int(num.strip()) for num in nums]
	
	c = db.graphs.aggregate([
							{'$match': {'degrees' : seq}},
							{'$sort': {'name' : 1}}
							])
	
	for g in c:
		results.append(g)

	c = db.graphs.aggregate([
							{'$match' : {'degrees' : {'$size' : len(seq)}}},
							{'$sort' : {'degrees' : 1}}
							])

	for g in c:
		if g not in results:
			close_results.append(g)

	return results, close_results

def title_search(q):
	results = []
	close_results = []
	db = get_db()

	c = db.graphs.aggregate([
							{'$match': {'title' : q}},
							{'$sort': {'name' : 1}}
							])
	
	for g in c:
		results.append(g)

	c = db.graphs.aggregate([
							{'$match' : {'$text' : {'$search' : q}}},
							{'$sort' : { 'score': { '$meta': "textScore" } }}
							])

	for g in c:
		if g not in results:
			close_results.append(g)

	return results, close_results

def name_search(q):
	db = get_db()

	c = db.graphs.find_one({'name': q})

	if not c:
		flash('Invalid ID.')
		return redirect(url_for('index'))

	return redirect(url_for('graph', gid=q))
