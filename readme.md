# Reddit Pipeline ETL project

## Objectives

The primary goal of this project is to create a scalable and efficient pipeline that automates the extraction, transformation, and loading of Reddit data into a format that is ready for analysis. This involves:

* Extracting data from Reddit using Reddit's API or a third-party data source.
* Transforming the raw data to clean, organize, and prepare it for analysis. This may include removing duplicates, handling missing values, and structuring the data into a suitable format.
* Loading the transformed data into a database or data warehouse for easy access and analysis.

### Scope of the project

* Selection of relevant data sources on Reddit, such as "Data Science" related threads are chosen in this case
* Determination of the data extraction frequency (e.g., real-time, hourly, daily)
* Definition of the data transformation processes needed to clean and structure the data.
* Choice of storage solution (e.g., SQL database, NoSQL database, data lake, **Redis**) for the processed data.
* Implementation of monitoring and logging to track the pipeline's performance and data quality.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Python 3.10
* A PC that can run 24/7, at least 16GB + 500G hard disk
* Reddit Developer account
* Linux / Ubuntu 


### Tools needed for this project

* Programming Languages: Python due to their extensive libraries and frameworks for data processing and API interactions.
* APIs: Reddit API for data extraction.
* ETL Frameworks: Apache Airflow, Apache NiFi, or similar for orchestrating the ETL pipeline.
* Databases/Data Warehouses: PostgreSQL, **MongoDB**, Amazon Redshift, or similar for data storage.
* Data Processing Libraries: Pandas for data manipulation, NLTK or spaCy for text processing (if needed).
* Data Storage: My SQL, SQL database, NoSQL database, data lake, **Redis**

## Authors
* **Shuyan Huang** - **Inital Work**