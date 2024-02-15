import redis

class redis_functions:

    def __init__(self, host='127.0.0.1', port=6379, db=0, set_name='reddit_post'):
        """Objectivs: It initializes a new instance of the class with the necessary 
            configuration to connect to a Redis server and specifies the name of 
            the set where posts will be stored
            
            Parameters:
            host: The hostname or IP address of the Redis server. Defaults to '127.0.0.1'.
            port: The port number on which the Redis server is connecting. The default Redis port is 6379.
            db: This parameter selects which database to use. Default database is 0
            set_name: The name of the Redis set where posts are stored. Default name is 'reddit_post'
            Return: None. 

            Return: None
        """
        self.db = redis.Redis(host=host, port=port, db=db)
        self.redit_post = set_name


    def add_posts(self, posts):
        """Objectivs: Adds one or multiple posts to the specified Redis set.
            
            Parameters:
            posts: A set of posts to add. 

            Return: None. 
        """
        if not isinstance(posts, set):
            raise TypeError("Posts must be provided as a set.")
        self.db.sadd(self.redit_post, *posts)


    def remove_posts(self, posts=None):
        """Objectivs:Removes specified posts from the subreddit set.
            If no posts are specified (i.e., posts is None), 
            it deletes the entire set, removing all posts.
            
            Parameters:
            posts: An optional parameter, if provided, should be a set of posts to remove.
                If None, the entire subreddit set is deleted. 

            Return: None. 
        """
        if posts is None:
            self.db.delete(self.redit_post)
        elif isinstance(posts, set):
            self.db.srem(self.redit_post, *posts)
        else:
            raise TypeError("Posts must be provided as a set or None to remove all.")
            

    def get_all_posts(self):
        """Objectivs: Retrieves all posts currently stored in the subreddit set.
            
            Parameters:
            None

            Return: Returns all the elements of the Redis set  
        """
       
        return self.db.smembers(self.redit_post)
            
