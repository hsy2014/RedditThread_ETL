import praw
import configparser
import sys
sys.path.append('/home/cissy/repos/RedditThread_ETL/utils')

from redis_util import RedisConnection

path_to_secrets = '/home/cissy/repos/RedditThread_ETL/secrets.ini'

config = configparser.ConfigParser()
config.read(path_to_secrets)
reddit_client_id = config["reddit_cred"]["client_id"]
reddit_client_secret = config["reddit_cred"]["client_secret"]


reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent="test_agent",
)

redis_connection = RedisConnection()

# get all reddit unique ids from redis
redis_unique_postids = redis_connection.get_all_post_ids()
postids_toadd = set()
for submission in reddit.subreddit("datascience").hot(limit=10):
    # print(submission.title) 
    # print(submission.id) # id we are going to use for duplication check
    if submission.id not in redis_unique_postids:
        postids_toadd.add(submission.id)

    if postids_toadd:
        redis_connection.add_postids(postids_toadd)

