import praw
import configparser
import sys
sys.path.append('/home/cissy/repos/RedditThread_ETL/utils')

from redis_util import RedisConnection 

class RedditToRedis:
    def __init__(self, path_to_secrets, subreddit_name, limit=10, user_agent="test_agent"):
        """
        Initializes the RedditToRedis instance with subreddit and limit for fetching posts,
        and sets up the Reddit and Redis clients using provided credentials.

        Parameters:
        - path_to_secrets: Path to the configuration file with Reddit credentials.
        - subreddit_name: Name of the subreddit to scrape.
        - limit: Number of posts to fetch. Defaults to 10.
        - user_agent: User agent for Reddit API requests.
        """
        self.subreddit_name = subreddit_name
        self.limit = limit
        self.reddit = self._init_reddit_client(path_to_secrets, user_agent)
        self.redis_connection = RedisConnection()

    def _init_reddit_client(self, path_to_secrets, user_agent):
        """
        Initializes the Reddit client with credentials obtained 
        from a configuration file and returns an instance of the client.

        Parameters:
        - path_to_secrets (str): Path to the configuration file with Reddit credentials. 
                This file should be in ini format.
        - user_agent (str): A string that identifies the application making requests to the Reddit API. 

        Return:
        - praw.Reddit instance: An initialized Reddit client object ready for making API requests. 
        """
        config = configparser.ConfigParser()
        config.read(path_to_secrets)
        reddit_client_id = config["reddit_cred"]["client_id"]
        reddit_client_secret = config["reddit_cred"]["client_secret"]
        return praw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_client_secret,
            user_agent="test_agent",
            )
        
     

    def update_posts_to_redis(self):
        """
        Fetches posts from a predefined subreddit, checks for duplicates in Redis, 
        and stores the IDs of new and unique posts.

        """
        redis_unique_postids = self.redis_connection.get_all_post_ids()
        postids_to_add = set()

        for submission in self.reddit.subreddit(self.subreddit_name).hot(limit=self.limit):
            if submission.id not in redis_unique_postids:
                postids_to_add.add(submission.id)

        if postids_to_add:
            self.redis_connection.add_postids(postids_to_add)
            print(f"Added {len(postids_to_add)} new post IDs to Redis.")
        else:
            print("No new posts to add.")

# Example usage
if __name__ == "__main__":

    # Load Reddit credentials from a configuration file
    path_to_secrets = '/home/cissy/repos/RedditThread_ETL/secrets.ini'
    subreddit_name = "datascience" 
    reddit_to_redis = RedditToRedis(path_to_secrets=path_to_secrets, subreddit_name=subreddit_name)
    reddit_to_redis.update_posts_to_redis()