# extract data
# mongodb - extract mongodb
import sys
from datetime import datetime
from textblob import TextBlob
import pymysql
sys.path.append('/home/cissy/repos/RedditThread_ETL/utils')

from mongodb_util import get_mongDB_connection
from mysql_util import get_mysql_connection
from email_util import mysql_update_email



def data_extration(reddit_topic='datascience'):
    """
    Retrieves a list of submissions from a MongoDB database based on a specified Reddit topic and the current date.
    
    Parameters:
    - reddit_topic: The Reddit topic for which to fetch submissions. Defaults to 'datascience'.
    
    Returns:
    submission_list: A list of dictionaries, where each dictionary contains information about submission(s)
        related to the specified Reddit topic. 
    
    """
    connection = get_mongDB_connection()
    query = {"RedditTopic": f"{reddit_topic}", "date_loaded": str(datetime.now().date())}
    # submission list is a list of dict, each dict contains 1 entry of MongoDB document
    submission_list = connection.find_doc(query)
    return submission_list



def sentiment_processing(submission_list=None):
    """
    Analyzes and extracts sentiment information from a list of Reddit submissions.
    
    Parameters:
    - submission_list : A list of dictionaries, each containing information about Reddit submission(s).
    
    Returns:
    list of dict: A list of dictionaries, each representing the sentiment analysis result for a submission.
        Each dictionary contains the title of the submission, its sentiment polarity, 
        and its sentiment subjectivity.
    """
    sentiments = []
    
    for i in range(len(submission_list)):
        submission_titles=[submission['submission_title'] for submission in submission_list[i]['submissions']]
  
        for submission in submission_titles:
            analysis = TextBlob(submission)
            sentiment = {
                'title': submission,
                'polarity': analysis.sentiment.polarity,
                'subjectivity': analysis.sentiment.subjectivity
            }
            sentiments.append(sentiment)
    return sentiments


def add_subreddit_topic(reddit_topic):
        """
        Inserts a new Reddit topic into the autoascending 'subreddit_topic' table if it does not already exist,
        and retrieves the ID of the topic from the database.
        
        Parameters:
        - reddit_topic: The name of the Reddit topic to add or find in the database.
        
        Returns:
        The ID of the Reddit topic from the 'subreddit_topic' table.
        
        """
        connection = get_mysql_connection().get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT ID FROM subreddit_topic WHERE Topic_Name = '{reddit_topic}'")
                result = cursor.fetchone()
                if not result:
                    cursor.execute(f"INSERT INTO subreddit_topic (Topic_Name) VALUES ('{reddit_topic}')")
                    connection.commit()
        except pymysql.MySQLError as e:
            print(f"Failed to insert subreddit topic: {e}")
        
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT ID FROM subreddit_topic WHERE Topic_Name = '{reddit_topic}'")
            result = cursor.fetchone()
            return result[0]
    

def load_data_to_sql(reddit_topic):
    """
    Loads sentiment analysis data into the MySQL database for a specified Reddit topic.
    
    Parameters:
    - reddit_topic: The name of the Reddit topic for which sentiment data is to be loaded into the database.
    
    Returns:
    The total number of daily submissions processed and attempted to be loaded into the database.
    """
    topic_id = add_subreddit_topic(reddit_topic)
    daily_data = data_extration()
    total_rows = 0
    for daily_submission in daily_data:
        query = """
        INSERT INTO subreddit_sentiment 
        (SubmissionID, SourceID, Date_Generated, Date_Loaded, Polarity, SubredditID, Subjectivity)
        VALUES 
        """
        source_id = str(daily_submission['_id'])
        date_loaded = str(datetime.now().date())
        date_generated = daily_submission['date_loaded']
        
        total_rows += 1
        
        for submission_dict in daily_submission['submissions']:
            submission_id = submission_dict['submission_id']
            text_blob_obj = TextBlob(submission_dict['submission_title'])
            polarity = text_blob_obj.sentiment.polarity
            subjectivity = text_blob_obj.sentiment.subjectivity
            values_tuple = f"""("{submission_id}", "{source_id}", "{date_generated}", "{date_loaded}", {polarity}, {topic_id}, {subjectivity}), \n"""
            query += values_tuple
        print("We are about to execute query: ", query[:-3] + "; ")
        
        query = query[:-3] + "; "
        connection = get_mysql_connection()
        mysql_server = connection.get_connection()
        new_cursor = mysql_server.cursor()
        new_cursor.execute(query)
        mysql_server.commit()
        return total_rows
    
def update_mysql():
    """
    Updates the MySQL database with sentiment analysis data for a specified Reddit topic,
    and sends an email notification with the update status.
    """
    try:
        db_title = "RedditPost_DataScience"
        reddit_topic = 'DataScience'
        row_added_cnt = load_data_to_sql(reddit_topic)
        mysql_update_email(rows_added_cnt= row_added_cnt,database_title = db_title)
    except Exception as e:
        mysql_update_email(0, db_title, error=e)
        print(f"Error: {e}")

# if __name__ == "__main__":
#     reddit_topic = 'datascience'
#     submission_list = data_extration(reddit_topic=reddit_topic)
#     print(submission_list)
#     sentiments = sentiment_processing(submission_list)
#     print ("\n")
#     print(sentiments)
#     update_mysql()
    


    