# TwitterMonitor
A simple Python app that uses the Twitter API to monitor specified twitter accounts, analyze the sentiment of a tweet, and send the tweet and language polarity to specified end-points in AWS SNS (e.g., mobile phone number or email). The tweets are then saved to a text file. 

Uses boto3, tweepy, and textblob.
