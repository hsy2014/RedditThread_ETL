from pymongo import MongoClient

user_name = "shuyanhuang2014"
password = "Kx825123!"

conn_str = f"mongodb+srv://{user_name}:{password}@cluster0.pzr6ccn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_Conn = MongoClient(conn_str)

mydb = mongo_Conn["Test_database"]
mycol = mydb["customers"]
mydict = { "name": "John", "address": "Highway 37", "pets": ["cat", "dog"], "friend": {"name": "cissy"}}

# x = mycol.insert_one(mydict)
print(mongo_Conn.list_database_names())

mylist = [
  { "name": "Amy", "address": "Apple st 652"},
  { "name": "Hannah", "address": "Mountain 21"},
  { "name": "Michael", "address": "Valley 345"},
  { "name": "Sandy", "address": "Ocean blvd 2"},
  { "name": "Betty", "address": "Green Grass 1"},
  { "name": "Richard", "address": "Sky st 331"},
  { "name": "Susan", "address": "One way 98"},
  { "name": "Vicky", "address": "Yellow Garden 2"},
  { "name": "Ben", "address": "Park Lane 38"},
  { "name": "William", "address": "Central st 954"},
  { "name": "Chuck", "address": "Main Road 989"},
  { "name": "Viola", "address": "Sideway 1633"}
]

# x = mycol.insert_many(mylist)

#print list of the _id values of the inserted documents:
# print(x.inserted_ids)

query = {"name": "John", "friend": {'name': 'cissy'}}
x = mycol.find(query)
#print([doc for doc in x])