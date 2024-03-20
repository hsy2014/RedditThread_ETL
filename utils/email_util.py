import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser

path_to_secrets = '/home/cissy/repos/RedditThread_ETL/secrets.ini'

config = configparser.ConfigParser()
config.read(path_to_secrets)
email = config["email_cred"]["email_account"]
email_password = config["email_cred"]["email_password"]
smtpServer = config["email_cred"]["smtp_server"]



def dbConnection_email(inserted_docs_count,thread_title, error=None):
    """
    Sends an email notification about the number of documents inserted or an error if occurred.

    Parameters:
    - inserted_docs_count: The number of new documents inserted into the database.
    - thread_title: the subreddit name
    - error: The error occurred during the process. Defaults to None.
    """
    sender_address = email
    receiver_address = email
    password = email_password  # Consider using environment variables or a safer method to store this!

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Reddit Pipeline Notification'
    
    if error:
        mail_content = f"""
        <html>
        <body>
            <p>Hello,</p>
            <p>The data pipeline for '<b>{thread_title}</b>' has encountered an error:</p>
            <p><i>{str(error)}</i></p>
            <p>Please check the system for more details.</p>
            <p>Best,<br>Redis to MongoDB Data Pipeline System</p>
        </body>
        </html>
        """
    else:
        mail_content = f"""
        <html>
        <body>
            <p>Hello,</p>
            <p>The data pipeline for '<b>{thread_title}</b>' has successfully completed its execution.</p>
            <p>Number of documents inserted: <b>{inserted_docs_count}</b></p>
            <p>Best,<br>Your Data Pipeline Notification System</p>
        </body>
        </html>
        """

    try:
        message.attach(MIMEText(mail_content, 'html'))
        session = smtplib.SMTP(smtpServer, 587)  
        session.starttls()  # enable security
        session.login(sender_address, password)  
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent Successfully')
    except Exception as e:
        print(f"Failed to send email: {e}")


def mysql_update_email(rows_added_cnt,database_title, error=None):
    """
    Sends an email notification about the number of SQL row updated or an error if occurred.

    Parameters:
    - rows_added_cnt: The number of new rows inserted into the MySQL database.
    - database_title: the title of the database in DBeaver.
    - error: The error occurred during the process. Defaults to None.
    """
    sender_address = email
    receiver_address = email
    password = email_password  # Consider using environment variables or a safer method to store this!

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'MySQL Update Notification'
    
    if error:
        mail_content = f"""
        <html>
        <body>
            <p>Hello,</p>
            <p>The database pipeline for '<b>{database_title}</b>' has encountered an error:</p>
            <p><i>{str(error)}</i></p>
            <p>Please check the system for more details.</p>
            <p>Best,<br>Your Data Pipeline System</p>
        </body>
        </html>
        """
    else:
        mail_content = f"""
        <html>
        <body>
            <p>Hello,</p>
            <p>The database pipeline for '<b>{database_title}</b>' has successfully completed its execution.</p>
            <p>Number of documents inserted: <b>{rows_added_cnt}</b></p>
            <p>Best,<br>Your Data Pipeline Notification System</p>
        </body>
        </html>
        """

    try:
        message.attach(MIMEText(mail_content, 'html'))
        session = smtplib.SMTP(smtpServer, 587)  
        session.starttls()  # enable security
        session.login(sender_address, password)  
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent Successfully')
    except Exception as e:
        print(f"Failed to send email: {e}")


    
