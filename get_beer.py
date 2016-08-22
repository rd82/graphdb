from neo4jrestclient.client import GraphDatabase as graphDB
from config import GRAPHDB_URL, GRAPHDB_USER, GRAPHDB_PASSWD
from neo4jrestclient import client
from pprint import pprint

# Add labels
def createLabel(db,label):
	return db.labels.create(label)

# Create nodes with only one property 'name'
def createNodes(db,names):
	nodes = []
	for name in names:
		node = db.nodes.create(name=name)
		nodes.append(node)

	return nodes

def addLabel(label,nodes):
	#for node in nodes:
	#	label.add(node)
	for node in nodes:
		label.add(node)

if __name__ == '__main__':
	db = graphDB(GRAPHDB_URL,username=GRAPHDB_USER,password=GRAPHDB_PASSWD)

	# Clean all the data first 
	q = 'MATCH (n) DETACH DELETE n'
	results = db.query(q, returns=(None))


	users = ['Marco','Daniela']
	beers = ['Punk IPA','Hoergaarden Rosee']

	userLabel = createLabel(db,'User')
	beerLabel = createLabel(db,'Beer')


	userNodes = createNodes(db,users)
	addLabel(userLabel,userNodes)

	beerNodes = createNodes(db,beers)
	addLabel(beerLabel,beerNodes)

	marco = db.query("MATCH (u:User)  where u.name = 'Marco' return u", returns=(client.Node))[0][0]
	daniela = db.query("MATCH (u:User)  where u.name = 'Daniela' return u",returns=(client.Node))[0][0]

	punkBeer = db.query("MATCH (b:Beer)  where b.name = 'Punk IPA' return b",returns=(client.Node))[0][0]
	hoerBeer = db.query("MATCH (b:Beer)  where b.name = 'Hoergaarden Rosee' return b",returns=(client.Node))[0][0]

	marco.relationships.create('likes',punkBeer)
	marco.relationships.create('likes',hoerBeer)
	daniela.relationships.create('likes',hoerBeer)
	
	print 'Users are->'
	q= 'Match (u:User) return u order by u.name'
	results = db.query(q, returns=(client.Node))
	for r in results:
		print("\t(%s) " % (r[0]["name"] ))

	print 'Beers are->'
	q= 'Match (b:Beer) return b order by b.name'
	results = db.query(q, returns=(client.Node))
	for r in results:
		print("\t(%s) " % (r[0]["name"] ))

	print 'Relationships are->'
	q= 'Match (u:User)-[r:likes]-(b:Beer)  return u,type(r),b order by u.name'
	results = db.query(q, returns=(client.Node))
	for r in results:
		# print("(%s)-[%s]->(%s)" % (r[0]["name"], r[1], r[2]["name"]))
		userName,rel, relDel = r
		print("\t(%s)-[%s]->(%s)" % (userName["name"], rel, relDel['data']['name']))
		

	"""
	#pprint(results[0])
	userName,rel, relDel = results[0]

	print userName['name']
	print rel
	print relDel['data']['name']


	q = 'MATCH (u:User)-[r:likes]->(m:Beer) WHERE u.name="Marco" RETURN u, type(r), m'
	# "db" as defined above
	results = db.query(q, returns=(client.Node, str, client.Node))
	for r in results:
	    print("(%s)-[%s]->(%s)" % (r[0]["name"], r[1], r[2]["name"]))
	# The output:
	# (Marco)-[likes]->(Punk IPA)
	# (Marco)-[likes]->(Hoegaarden Rosee)
	"""