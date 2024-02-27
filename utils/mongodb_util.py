from pymongo import MongoClient
import configparser
from difflib import SequenceMatcher

path_to_secrets = '/home/cissy/repos/RedditThread_ETL/secrets.ini'

config = configparser.ConfigParser()
config.read(path_to_secrets)
mongo_user = config["mongodb_cred"]["mongo_user"]
mongo_secret = config["mongodb_cred"]["mongo_secret"]

class MongodbConnection:

    def __init__(self,db_name="RedditThread_Titles",col_name = "thread_collection"):
        """
        Initialize a MongoDB connection with specific parameters. Created databse and collection.
        It checks if the specified database and collection exist based on user input, 
        it can create them if they don't.

        Parameters:
        - db_name: Name of your database
        - col_name: Name of your collection
        """
        self.conn_str = f"mongodb+srv://{mongo_user}:{mongo_secret}@cluster0.pzr6ccn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.mongo_Conn = MongoClient(self.conn_str)
        self.db = db_name
        self.col = col_name
        self.db_name = self.mongo_Conn[self.db]
        self.col_name = self.db_name[self.col]

        # db_list = self.mongo_Conn.list_database_names()
        # db_col_list = self.mongo_Conn[self.db_name].list_collection_names()

        try:
            if self.db not in self.mongo_Conn.list_database_names():
                # If the database does not exist, it's safe to insert the initialization document
                print("Database does not exist. Creating and initializing with a test document.")
                self.col_name.insert_one({"init": "initDocument"})
            elif self.col not in self.db_name.list_collection_names():
                # If the database exists but the collection does not, insert the initialization document
                print("Collection does not exist. Creating and initializing with a test document.")
                self.col_name.insert_one({"init": "initDocument"})
            else:
                # Both the database and collection exist, no need to insert the initialization document
                print("Database and collection already exist. No initialization document inserted.")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")


    def insert_doc(self,documents):
        """
        Inserts a single document or multiple documents into the configured MongoDB collection. 

        Parameters:
        - documents: The document(s) to be inserted into the collection. 
        """
        test_case_exists = self.col_name.find_one({"init": "initDocument"})
        
        if test_case_exists:
            self.col_name.delete_many({"init": "initDocument"})
            print("Test case removed successfully.")

        if isinstance(documents, dict):
            result = self.col_name.insert_one(documents)
            print("1 has been inserted")
        elif isinstance(documents, list):
            result = self.col_name.insert_many(documents)
            print(f"{len(x.inserted_ids)} has been inserted")
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
        - list of found document(s) or a message indicating no matches directly to the console.
        """
        if find_one:
            # Find a single document based on the query
            document = self.col_name.find_one(query)
            if not document:
                print("No document matches the query.")
            return document
        else:
            documents = self.col_name.find(query)
            # Attempt to limit the results if limit is specified
            if limit is not None:
                documents = documents.limit(limit)
            # Convert cursor to list to evaluate its size
            documents_list = [doc for doc in documents]
            
            # # Check if the list is empty
            # if documents_list:
            #     return print(documents_list)
            # else:
            #     print(f'documents are {documents_list}')
            #     print("No documents match the query.")

            return documents_list
                

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
            del_obj = self.col_name.delete_one(query)
            if del_obj:
                print(f"{del_obj.deleted_count} has been deleted")
        else:
            # Find all documents matching the query
            del_obj = self.col_name.delete_many(query)
            if del_obj:
                print(f"{del_obj.deleted_count} has been deleted")

def get_mongDB_connection():
    mongo_connection = MongodbConnection(db_name="RedditThread_Titles",col_name = "thread_collection")
    return mongo_connection


if __name__ == "__main__":
    mongo_connection = get_mongDB_connection()
    # mylist = [
    # { "name": "Amy", "address": "Apple st 652"},
    # { "name": "Hannah", "address": "Mountain 21"},
    # { "name": "Michael", "address": "Valley 345"},
    # { "name": "Sandy", "address": "Ocean blvd 2"},
    # { "name": "Betty", "address": "Green Grass 1"},
    # { "name": "Richard", "address": "Sky st 331"},
    # { "name": "Susan", "address": "One way 98"},
    # { "name": "Vicky", "address": "Yellow Garden 2"},
    # { "name": "Ben", "address": "Park Lane 38"},
    # { "name": "William", "address": "Central st 954"},
    # { "name": "Chuck", "address": "Main Road 989"},
    # { "name": "Viola", "address": "Sideway 1633"}
    # ]
    # mydict = { "name": "John", "address": "Highway 37", "pets": ["cat", "dog"], "friend": {"name": "cissy"}}
    # mytest = { "name": "Michael", "address": "Valley 345"}
    # test_2 = {"name": "yokoo"}
    # #mongo_connection.insert_doc(mydict)
    # # print(mongo_connection.find_doc(query=test_2,find_one=True, limit=1))
    # #print(mongo_connection.mongo_Conn[dbs_name][db_collection])
    # print(mongo_connection.del_doc(query=test_2))
    




    