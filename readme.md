# Reddit Pipeline ETL project
The primary goal of this project is to create a scalable and efficient pipeline that automates the extraction, transformation, and loading of Reddit data into a format that is ready for analysis.

## Table of contents
- [Objectives](#Objectives)
    - [Project Scope](#Scope-of-the-project)
- [Getting Started](#Getting-Started)
    - [Prerequisites](#prerequisites)
    - [Tools](#Tools-needed-for-this-project)
    - [System Setup](#system-setup)
    - [Project Structure](#Project-Structure)

## Objectives

. This involves:

* Extracting data from Reddit using Reddit's API or a third-party data source.
* Transforming the raw data to clean, organize, and prepare it for analysis. This may include removing duplicates, handling missing values, and structuring the data into a suitable format.
* Loading the transformed data into a database or data warehouse for easy access and analysis.

### Scope of the project

* Selection of relevant data sources on Reddit, such as "Data Science" related threads are chosen in this case
* Determination of the data extraction frequency (e.g., real-time, hourly, daily)
* Definition of the data transformation processes needed to clean and structure the data.
* Choice of storage solution (e.g., SQL database, NoSQL database, data lake, **[Redis](https://redis.io/)**) for the processed data.
* Implementation of monitoring and logging to track the pipeline's performance and data quality.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Python 3.10
* A PC that can run 24/7, at least 16GB + 500G hard disk
* Reddit Developer account
* Linux / Ubuntu 
* Redis
* Airflow


### Tools needed for this project

* Programming Languages: Python due to their extensive libraries and frameworks for data processing and API interactions.
* APIs: Reddit API for data extraction.
* ETL Frameworks: Apache Airflow, Apache NiFi, or similar for orchestrating the ETL pipeline.
* Databases/Data Warehouses: PostgreSQL, **MongoDB**, Amazon Redshift, or similar for data storage.
* Data Processing Libraries: Pandas for data manipulation, NLTK or spaCy for text processing (if needed).
* Data Storage: My SQL, SQL database, NoSQL database, data lake, **[Redis](https://redis.io/)**

### System Setup
1. Clone the Repository.
```python
    git clone https://github.com/hsy2014/RedditThread_ETL.git
    cd RedditThread_ETL
```

2. Set Up Reddit API Credentials.
* Obtain your Reddit API client_id and client_secret by creating an application a [Reddit's Developer API Portal](https://www.reddit.com/wiki/api/)

* Create a **secrets.ini** file in the project root with your credentials:
```python
    [reddit_cred]
    client_id=YOUR_CLIENT_ID
    client_secret=YOUR_CLIENT_SECRET
```
3. Open a project Directory.
```python
    cd path\to\your\project
```

4. create a virtual environment to execute all the program.
```python
    virtualenv new_venv
    source new_venv/bin/activate
```

5. Install the dependencies.
```python
    pip install -r requirements.txt
```


### Project Structure
- **`Scripts`**: Contains the main Reddit Thread_ETL code.
    - **`Reddit_scrapping`**: 
        Check Redis for Submission ID: Each fetched submission's ID is checked against a list of IDs stored in Redis t0 determine if it has been processed before.
        - **If Submission ID is Not in Redis:**
            * The submission is considered new.
            * The new submission's data is added to the MongoDB database for persistent storage.
            * The new submission ID is then added to Redis to mark it as processed.
        - **If Submission ID is in Redis:**
            * The submission is recognized as already processed.
            * The pipeline skips adding this submission to MongoDB to prevent duplicates.
- **`utils`**: Hold utility functions and constants.
    - The **RedisConnection** class provides a simple interface to interact with a Redis data store, specifically tailored to handle Reddit post IDs for an ETL pipeline.
        - Establish a connection to a Redis server.
        - Add new post IDs to a Redis set.
        - Remove post IDs from a Redis set.
        - Retrieve all post IDs stored in a Redis set.
    - **Initialization**
    ```python
        from redis_util import RedisConnection

        # Initialize with default parameters
        redis_connection = RedisConnection()

        # Or initialize with custom parameters
        redis_connection = RedisConnection(host='your_host', port=your_port, db=your_db, set_name='your_set_name')
    ```
    - The **MongodbConnection** class provides an easy way to connect to a MongoDB database, create databases and collections, insert documents, and query or delete them.
        - Establish a connection to MongoDB using credentials.
        - Automatically create a database and collection if they don't exist.
        - Insert single or multiple documents into a collection.
        - Find documents with optional query filters, with support for finding a single document or limiting the number of documents returned.
        - Delete documents based on a query, with an option to delete only the first document matching the criteria.
    - **Initialization**
    ```python
        from pymongo import MongoClient
        
        mongo_connection = MongodbConnection(user_name="your_username", password="your_password")
    ```

## Contribution
Contributions to improve the project are welcome. Please follow these steps:

* Fork the repository.
* Create a new branch (**git checkout -b new-branch**).
* Commit your changes (**git commit -am 'Add some feature'**).
* Push to the branch (**git push origin new-branch**).
* Open a Pull Request.

## Authors
* **Shuyan Huang** - **Inital Work**