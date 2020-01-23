import tweepy
import boto3
from textblob import TextBlob


# Twitter access information. This should be changed later to use AWS STS/Parameter store.
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# AWS SNS access information. This should be changed later to use AWS STS/Parameter store.
client = boto3.client(
    'sns',
    aws_access_key_id="",
    aws_secret_access_key="",
    region_name="us-east-1" # or as desired
)


# Filter out retweets of those you're monitoring or else you'll be inundated with notices.
def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True


# Main function to monitor for tweets, print output, and publish to AWS SNS mobile number.
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if from_creator(status):
            try:
                # Prints out the extended tweet
                getattr(status, 'extended_tweet')
                analysis = TextBlob(status.extended_tweet['full_text'])
                # set sentiment
                if analysis.sentiment.polarity > 0:
                    analysis = 'positive'
                elif analysis.sentiment.polarity == 0:
                    analysis = 'neutral'
                else:
                    analysis = 'negative'
                # convert tuple to string for tweepy
                print(analysis.upper() + " " + status.user.screen_name + " " + status.extended_tweet['full_text'])
                client.publish(
                    TargetArn="", # Input AWS ARN for SNS
                    Message=analysis.upper() + " " + status.user.screen_name + " " + status.extended_tweet['full_text']
                )
                # Saves the extended tweet to a file
                with open("Test.txt", 'a') as file:
                    file.write(analysis.upper() + status.extended_tweet['full_text'])
            except AttributeError:
                # Prints out the regular length tweet
                analysis = TextBlob(status.text)
                # set sentiment
                if analysis.sentiment.polarity > 0:
                    analysis = 'positive'
                elif analysis.sentiment.polarity == 0:
                    analysis = 'neutral'
                else:
                    analysis = 'negative'
                # convert tuple to string for tweepy compliance
                print(analysis.upper() + " " + status.user.screen_name + " " + status.text)
                client.publish(
                    TargetArn="", # Input AWS ARN for SNS
                    Message=analysis + " " + status.user.screen_name + " " + status.text
                )
                # Saves the regular length tweet to a file.
                with open("Test.txt", 'a') as file:
                    file.write(analysis.upper() + status.text)
            return True
        return True

    def on_error(self, status_code):
        if status_code == 420:
            print("Error 420")
            # returning False in on_error disconnects the stream
            return False


# Setup the Tweepy stream listener.
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener(), tweet_mode="extended")
myStream.filter(follow=["", ""]) # Input any number of twitter account IDs you wish to follow within the double quotes, separated by a comma. 

