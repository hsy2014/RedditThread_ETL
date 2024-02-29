import praw
import sys
from datetime import datetime
sys.path.append('/home/cissy/repos/RedditThread_ETL/utils')

from redis_util import get_redis_connection, get_reddit_connection
from mongodb_util import get_mongDB_connection





def update_subreddit_post(subredit_name,limit=20):
    """
     Updating a MongoDB collection with new subreddit posts while ensuring that duplicates are not added 
     by leveraging a Redis set for fast duplication checks

     Parameters:
     - subredit_name: The name of the subreddit from which to retrieve posts.
     - user_name: MongoDB user name (not in email form).
     - password: MongoDB password associated with the user name.
     - db: The Redis database index to use (default is 0).
     - set_name: The name of the Redis set used to store and check for unique post IDs (default is 'reddit_post').
     - limit: The maximum number of hot posts to retrieve from the subreddit (default is 10).
     - db_name: The name of the MongoDB database where subreddit posts will be stored (default is "RedditThread_Titles").
     - col_name: The name of the MongoDB collection within the database where posts will be stored (default is "thread_collection").
    """
    redis_connection = get_redis_connection()
    mongo_connection = get_mongDB_connection()
    reddit_connection = get_reddit_connection()

    # get all reddit unique ids from redis
    redis_unique_postids = redis_connection.get_all_post_ids()
    postids_toadd = set()
    submissions_list=[]

    for submission in reddit_connection.subreddit(subredit_name).hot(limit=limit):
        # print(submission.title) 
        # print(submission.id) # id we are going to use for duplication check
        if submission.id not in redis_unique_postids:
            submissions_list.append({"submission_id": submission.id, "submission_title": submission.title})
            postids_toadd.add(submission.id)
            
    if postids_toadd:
        dup_check = 1
        document = {
                "timestamp": datetime.now(),
                "RedditTopic": subredit_name,
                "submissions": submissions_list,
                "db_duplicated_checked": dup_check
            }
        mongo_connection.insert_doc(document)
        redis_connection.add_postids(postids_toadd)

def run_update():
    try:
        reddit_thread_title = "datascience"
        update_subreddit_post(reddit_thread_title)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_update()
