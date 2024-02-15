import praw
import configparser

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

for submission in reddit.subreddit("datascience").hot(limit=10):
    # print(submission.title) 
    print(submission.id) # id we are going to use for duplication check