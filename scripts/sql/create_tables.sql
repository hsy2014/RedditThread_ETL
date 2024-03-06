CREATE DATABASE IF NOT EXISTS RedditPost_DataScience;

CREATE TABLE subreddit_topic(
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Topic_Name VARCHAR(100)
);

CREATE TABLE subreddit_sentiment (
    SubmissionID VARCHAR(20) PRIMARY KEY,
    SourceID VARCHAR(100),
    Date_Generated DATE,
    Date_Loaded DATE,
    Polarity FLOAT,
    SubredditID INT FOREIGN KEY REFERENCES subreddit_topic(ID),
    subjectivity FLOAT
);

-- subreddit_sentiment:
--     id, (PK, varchar)
--     source_id (varchar)
--     date_generated (mongdb_time, timestamp / date),
--     date_loaded (mysql_time, timestamp / date),
--     polarity (double),
--     subreddit_id, (secondary key, int)
--     subjectivity (optional)

-- subreddit_topic:
--     id, (PK, int, auto increament)
--     topic_name (varchar)