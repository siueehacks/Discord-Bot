import tweepy

TWITTERID = 1470846677758185477

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
        
        # if a paragraph is longer than 280 characters, split it automatically
        # TODO: have this split on a space and have it add a '...' at the end
        if slice_index == -1:
            slice_index = 280


        message_to_send = message[:slice_index].strip()
        message = message[slice_index:].strip()

        if not first_tweet:
            tweet_to_reply_to = client.create_tweet(text = message_to_send, in_reply_to_tweet_id=tweet_to_reply_to).data['id']
        else:
            tweet_to_reply_to = client.create_tweet(text = message_to_send).data['id']
            first_tweet = False

    client.create_tweet(text = message)


def delete_tweet(client: tweepy.Client, tweet_num: int) -> None:
    """Delete test tweet from Twitter account through Discord"""
    response = client.get_users_tweets(id=TWITTERID, user_auth = True, max_results=tweet_num).data

    ids_to_delete = [x['id'] for x in response]
    for id in ids_to_delete:
        client.delete_tweet(id)