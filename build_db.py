import codecs
from json import load as jload
from pprint import pprint
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import BulkWriteError, InvalidOperation

config = {}
with open('../settings.cfg', 'r') as f:
	for line in f:
		key, val = line.split('=')
		config[key.strip()] = val.strip().replace("'", '')

client = MongoClient() 
client.admin.authenticate(config['MONGO_USERNAME'], config['MONGO_PASSWORD'])
db = client[config['MONGO_DBNAME']]


# print(db.collection_names())

elems = jload(codecs.open('static/gdb.json', 'r', 'utf-8-sig'))

names = set()
for doc in db.graphs.find().sort('name', ASCENDING):
	print(doc['name'])
	names.add(doc['name'])

bulk = db.graphs.initialize_unordered_bulk_op()
for k, v in elems.items():
	if k not in names:
		bulk.insert(v)
try:
	res = bulk.execute()
except BulkWriteError as bwe:
	print(bwe.details)
except InvalidOperation as io:
	res = 'Nothing to add.'

pprint(res)
