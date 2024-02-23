from pymongo import MongoClient

class MongodbConnection:

    def __init__(self,user_name,password,db_name="RedditThread_Titles",col_name = "thread_collection"):
        """
        Initialize a MongoDB connection with specific parameters. Created databse and collection.
        It checks if the specified database and collection exist based on user input, 
        it can create them if they don't.

        Parameters:
        - user_name: MongoDB user name (not in email form)
        - password: MangoDB password associated with user name
        - db_name: Name of your database
        - col_name: Name of your collection
        """
        self.user_name = user_name
        self.password = password
        self.conn_str = f"mongodb+srv://{self.user_name}:{self.password}@cluster0.pzr6ccn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.mongo_Conn = MongoClient(self.conn_str)
        self.db_name = db_name
        self.col_name = col_name

        db_list = self.mongo_Conn.list_database_names()
        db_col_list = self.mongo_Conn[self.db_name].list_collection_names()

        if self.db_name not in db_list:
            print(f"No database named '{self.db_name}' exist.\
                   Creating database '{self.db_name}' and \
                    collection '{self.col_name}': [Yes/No]")
            choice = input().lower()   
            if choice.lower() == 'yes':
                self.mydb=self.mongo_Conn[self.db_name]
                self.mycol = self.mydb[self.col_name]
                print(f"Successfully create database '{self.db_name}' and collection '{self.col_name}'")
            else:
                print("Please enter a valid database name")
                
        elif self.col_name in db_col_list:
            self.mydb=self.mongo_Conn[self.db_name]
            self.mycol = self.mydb[self.col_name]
            print(f"The collection '{self.col_name}' and the database '{self.db_name}' already existed.")

        else:
            self.mydb=self.mongo_Conn[self.db_name]
            self.mycol = self.mydb[self.col_name]
            print("Collection created")


    def insert_doc(self,documents):
        """
        Inserts a single document or multiple documents into the configured MongoDB collection. 

        Parameters:
        - documents: The document(s) to be inserted into the collection. 
        """
        if isinstance(documents, (dict, set)):
            result = self.mycol.insert_one(documents)
            print("Insert one document successfully")
        elif isinstance(documents, list):
            result = self.mycol.insert_many(documents)
            print("Insert many documents successfully")
        else:
            print("Error: Insertion failed.")

    def find_doc(self,query=None, find_one=False, limit = None):
        """
        Searches for documents in a MongoDB collection based on the provided query criteria. 

        Parameters:
        - query: The query criteria used to filter documents. 
            Defaults to None, which matches all documents in the collection.
        - find_one (bool, optional): A booleen specify whether to return only the first document that matches the query. 
            Defaults to False.
        - limit (int, optional): The maximum number of documents to return. 
            This parameter is ignored if find_one is True. Defaults to None, which means no limit.

        return:
        - Print the found document(s) or a message indicating no matches directly to the console.
        """
        if find_one:
            # Find a single document based on the query
            document = self.mycol.find_one(query)
            if document:
                return print(document)
            else:
                return print("No document matches the query.")
        else:
            documents = self.mycol.find(query)
            # Attempt to limit the results if limit is specified
            if limit is not None:
                documents = documents.limit(limit)
            
            # Convert cursor to list to evaluate its size
            documents_list = [doc for doc in documents]
            
            # Check if the list is empty
            if documents_list:
                return print(documents_list)
            else:
                return print("No documents match the query.")
                

    def del_doc(self,query=None, del_one=False):
        """
        Deletes documents from a MongoDB collection based on the provided query.
    
        Parameters:
        - query: The deletion criteria using a MongoDB query. Defaults to None, 
            which could delete all documents if not handled cautiously.
        - del_one (bool, optional): Flag indicating whether to delete only the first 
            document matching the query (True) or all documents that match the query (False). 
            Defaults to False.
    
        Returns:
        - Prints a message indicating the number of documents deleted.
        """
        if del_one:
            # Find a single document based on the query
            document = self.mycol.delete_one(query)
            if document:
                return print(f"{document.deleted_count} has been deleted")
        else:
            # Find all documents matching the query
            documents = self.mycol.delete_many(query)
            if documents:
                return print(f"{documents.deleted_count} has been deleted")


if __name__ == "__main__":
    mongo_connection = MongodbConnection(user_name="shuyanhuang2014",password="Kx825123!")
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
    mydict = { "name": "John", "address": "Highway 37", "pets": ["cat", "dog"], "friend": {"name": "cissy"}}
    mytest = { "name": "Michael", "address": "Valley 345"}
    #mongo_connection.insert_doc(mydict)
    mongo_connection.find_doc(query=mytest,find_one=False,limit=1)
    #print(mongo_connection.mongo_Conn[dbs_name][db_collection])
    



    