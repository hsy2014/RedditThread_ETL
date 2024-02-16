import redis

class RedisConnection:

    def __init__(self, host='127.0.0.1', port=6379, db=0, set_name='reddit_post'):
        """Objectivs: It initializes a new instance of the class with the necessary 
            configuration to connect to a Redis server and specifies the name of 
            the set where post_ids will be stored
            
            Parameters:
            host: The hostname or IP address of the Redis server. Defaults to '127.0.0.1'.
            port: The port number on which the Redis server is connecting. The default Redis port is 6379.
            db: This parameter selects which database to use. Default database is 0
            set_name: The name of the Redis set where post_ids are stored. Default name is 'reddit_post'
        """
        self.host = host 
        self.db = db
        self.port = port
        self.client = redis.Redis(host=self.host, port=self.port, db=self.db)
        self.set_name = set_name
        try:
            self.client.ping()
            print(f"Successfully connected to Redis at port: {self.port}, db: {self.db}")
        except Exception as e:
            print(f"Error: {e} \n Error conneting to redis at port: {self.port}, db: {self.db}")


    def add_postids(self, post_ids: set) -> None:
        """Objectivs: Adds one or multiple post_ids to the specified Redis set.
            Parameters:
            post_ids: A set of post_ids to add. 

            Return: None. 
        """
        if not isinstance(post_ids, set):
            raise TypeError("post_ids must be provided as a set.")
        self.client.sadd(self.set_name, *post_ids)


    def remove_post_ids(self, post_ids=None):
        """Objectivs:Removes specified post_ids from the subreddit set.
            If no post_ids are specified (i.e., post_ids is None), 
            it deletes the entire set, removing all post_ids.
            
            Parameters:
            post_ids: An optional parameter, if provided, should be a set of post_ids to remove.
                If None, the entire subreddit set is deleted. 

            Return: None. 
        """
        if post_ids is None:
            self.client.delete(self.set_name)
        elif isinstance(post_ids, set):
            self.client.srem(self.set_name, *post_ids)
        else:
            raise TypeError("post_ids must be provided as a set or None to remove all.")
            

    def get_all_post_ids(self):
        """Objectivs: Retrieves all post_ids currently stored in the subreddit set.
            
            Parameters:
            None

            Return: Returns all the elements of the Redis set  
        """
       
        return self.client.smembers(self.set_name)
            

if __name__ == "__main__":
    test_connection = RedisConnection()
    test_connection.add_post_ids("cissy")
