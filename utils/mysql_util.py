import pymysql
import configparser
from datetime import datetime

path_to_secrets = '/home/cissy/repos/RedditThread_ETL/secrets.ini'

config = configparser.ConfigParser()
config.read(path_to_secrets)
mysql_user = config["mysql_cred"]["mysql_user"]
mysql_secret = config["mysql_cred"]["mysql_secret"]

class mysqlconnection:
    def __init__(self, host='localhost', user=mysql_user, password=mysql_secret, db='RedditPost_DataScience'):
        """
        Initializes a new instance of the database connection class.
        
        Parameters:
        - host: The hostname or IP address of the MySQL server. Default is 'localhost'.
        - user: The username used to authenticate with MySQL.
        - password: The password for the specified user.
        - db: The name of the database to connect to. Default is 'RedditPost_DataScience'.
        """
        
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        
            
    def get_connection(self):
        """
        Establishes a connection to the MySQL database
        
        Returns:
        pymysql.connections.Connection: An established connection to the MySQL database.
        
        """
        try:
            self.connection = pymysql.connect(host=self.host,
                                         user=self.user,
                                         password=self.password,
                                         db=self.db)
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"MySQL Database version: {version[0]}")
            return self.connection
        except pymysql.MySQLError as e:
           print(f"Error connecting to MySQL Database: {e}")
            
      

def get_mysql_connection():
    """
    Creates and returns an instance of the mysqlconnection class, configured with the MySQL database credentials.
    """
    return mysqlconnection(user=mysql_user , password=mysql_secret)


# if __name__ == "__main__":
#     db_manager = get_mysql_connection()
#     db_manager.add_subreddit_topic('DataScience')
#     submission_data = {'SourceID': '123', '_id': 'abc', 'date_loaded': datetime.now().date()}
#     sentiment_data = {'Polarity': 0.5, 'Subjectivity': 0.75}
#     db_manager.add_subreddit_sentiment(submission_data, sentiment_data,red)
#     print(db_manager._get_subreddit_id("DataScience"))