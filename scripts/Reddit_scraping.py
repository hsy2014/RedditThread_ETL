import praw
import configparser
import sys
from datetime import datetime
sys.path.append('/home/cissy/repos/RedditThread_ETL/utils')

from redis_util import RedisConnection
from mongodb_util import MongodbConnection

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

# get all reddit unique ids from redis
redis_connection = RedisConnection()
mongo_connection = MongodbConnection(user_name="shuyanhuang2014",password="Kx825123!")
dup_check = 0

# get all reddit unique ids from redis
redis_unique_postids = redis_connection.get_all_post_ids()
postids_toadd = set()
submissions_list=[]

for submission in reddit.subreddit("datascience").hot(limit=10):
    # print(submission.title) 
    # print(submission.id) # id we are going to use for duplication check
    if submission.id not in redis_unique_postids:
        submissions_list.append({"submission_id": submission.id, "submission_title": submission.title})
        postids_toadd.add(submission.id)
            
if postids_toadd:
    dup_check = 1
    document = {
            "timestamp": datetime.utcnow(),
            "RedditTopic": "datascience",
            "submissions": submissions_list,
            "db_duplicated_checked": dup_check
            }
    mongo_connection.insert_doc(document)
    redis_connection.add_postids(postids_toadd)

