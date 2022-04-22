import requests
import os
from pprint import pprint

import tweepy

TWITTERID = 1470846677758185477

def send_groupme(bot_id: str, message: str) -> None:
    """Receive a message and copy message into groupMe

    Args:
        message (str): Message to be sent to GroupMe
    """
    def send_message(bot_id: str, message: str) -> None:
        """Send a message to GroupMe

        Args:
            bot_id (str): GroupMe bot id
            message (str): Message to be sent to GroupMe
        """
        url = f"https://api.groupme.com/v3/bots/post"
        data = {
            "bot_id": bot_id,
            "text": message
        }
        r = requests.post(url, json=data)
        print(f"GroupMe Status: {r.status_code}, {r.reason}")


    message = f"{message.author.display_name}: {message.clean_content}"

    # While loop controls handling for large messages
    while len(message) > 1000:
        sliced_message = message[:1000]
        slice_index = sliced_message.rfind('\n\n')
        message_to_send = sliced_message[:slice_index+2]
        message = message[slice_index+2:]

        send_message(bot_id, message_to_send)
    
    send_message(bot_id, message)


def tweet(client: tweepy.Client, message: str) -> None:
    """Receive a message and tweet message to Twitter account

    Args:
        message (str): Message to be tweeted
    """
    message = message.clean_content
    first_tweet = True
    tweet_to_reply_to = None

    # If the length of the announcment is greater than 280 characters, 
    # split it into multiple tweets in a thread
    while len(message) > 280:
        sliced_message = message[:280]
        slice_index = sliced_message.rfind('\n\n')
        message_to_send = sliced_message[:slice_index+2]
        message = message[slice_index+2:]

        print(f"Message: {message}")
        print(f"Message to send: {message_to_send}")
        if not first_tweet:
            print('Not first tweet')
            tweet_to_reply_to = client.create_tweet(text = message_to_send, in_reply_to_tweet_id=tweet_to_reply_to).data['id']
        else:
            tweet_to_reply_to = client.create_tweet(text = message_to_send).data['id']
            first_tweet = False
            print(f'Tweet to reply to: {tweet_to_reply_to}')

    client.create_tweet(text = message)


def delete_tweet(client: tweepy.Client, id: str) -> None:
    """Delete test tweet from Twitter account"""
    response = client.delete_tweet(id)
    pprint(f"Tweet Status: {response}")