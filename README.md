# TwitterMonitor
A simple Python app that uses the Twitter API to monitor specified twitter accounts, analyze the sentiment of a tweet, and send the tweet, language polarity, and content of tweet to specified end-points in AWS SNS (e.g., mobile phone number). The tweets are then saved to a text file. 

Uses boto3, tweepy, and textblob.
