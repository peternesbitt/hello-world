"""
Twitter API client - Handles all Twitter interactions
"""
import tweepy
from typing import List, Dict, Optional
from pathlib import Path
import time
from ..config import Config


class TwitterClient:
    """Manages Twitter API interactions"""

    def __init__(self):
        """Initialize Twitter API client"""
        # OAuth 1.0a authentication for posting
        auth = tweepy.OAuth1UserHandler(
            Config.TWITTER_API_KEY,
            Config.TWITTER_API_SECRET,
            Config.TWITTER_ACCESS_TOKEN,
            Config.TWITTER_ACCESS_TOKEN_SECRET
        )

        # API v1.1 for media upload
        self.api_v1 = tweepy.API(auth)

        # API v2 for tweets
        self.client = tweepy.Client(
            bearer_token=Config.TWITTER_BEARER_TOKEN,
            consumer_key=Config.TWITTER_API_KEY,
            consumer_secret=Config.TWITTER_API_SECRET,
            access_token=Config.TWITTER_ACCESS_TOKEN,
            access_token_secret=Config.TWITTER_ACCESS_TOKEN_SECRET,
            wait_on_rate_limit=True
        )

    def post_thread(
        self,
        tweets: List[str],
        media_paths: Optional[List[Path]] = None,
        delay_seconds: int = 2
    ) -> List[str]:
        """
        Post a Twitter thread

        Args:
            tweets: List of tweet texts
            media_paths: Optional list of image paths to attach
            delay_seconds: Delay between tweets to avoid rate limits

        Returns:
            List of tweet IDs
        """
        tweet_ids = []
        previous_tweet_id = None

        for i, tweet_text in enumerate(tweets):
            try:
                # Upload media if provided for this tweet
                media_ids = []
                if media_paths and i < len(media_paths):
                    media_path = media_paths[i]
                    if media_path and media_path.exists():
                        media = self.api_v1.media_upload(str(media_path))
                        media_ids = [media.media_id]

                # Post tweet
                response = self.client.create_tweet(
                    text=tweet_text,
                    in_reply_to_tweet_id=previous_tweet_id,
                    media_ids=media_ids if media_ids else None
                )

                tweet_id = response.data['id']
                tweet_ids.append(tweet_id)
                previous_tweet_id = tweet_id

                print(f"✓ Posted tweet {i+1}/{len(tweets)}: {tweet_id}")

                # Delay between tweets
                if i < len(tweets) - 1:
                    time.sleep(delay_seconds)

            except Exception as e:
                print(f"✗ Failed to post tweet {i+1}: {str(e)}")
                break

        return tweet_ids

    def post_single_tweet(
        self,
        text: str,
        media_path: Optional[Path] = None
    ) -> Optional[str]:
        """
        Post a single tweet

        Args:
            text: Tweet text
            media_path: Optional image path

        Returns:
            Tweet ID if successful
        """
        try:
            media_ids = []
            if media_path and media_path.exists():
                media = self.api_v1.media_upload(str(media_path))
                media_ids = [media.media_id]

            response = self.client.create_tweet(
                text=text,
                media_ids=media_ids if media_ids else None
            )

            tweet_id = response.data['id']
            print(f"✓ Posted tweet: {tweet_id}")
            return tweet_id

        except Exception as e:
            print(f"✗ Failed to post tweet: {str(e)}")
            return None

    def search_tweets(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Search for tweets matching a query

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            List of tweet data dictionaries
        """
        try:
            response = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=['author_id', 'created_at', 'public_metrics']
            )

            if not response.data:
                return []

            tweets = []
            for tweet in response.data:
                tweets.append({
                    'id': tweet.id,
                    'text': tweet.text,
                    'author_id': tweet.author_id,
                    'created_at': tweet.created_at,
                    'metrics': tweet.public_metrics
                })

            return tweets

        except Exception as e:
            print(f"✗ Search failed: {str(e)}")
            return []

    def like_tweet(self, tweet_id: str) -> bool:
        """Like a tweet"""
        try:
            # Get authenticated user ID
            me = self.client.get_me()
            user_id = me.data.id

            self.client.like(user_id=user_id, tweet_id=tweet_id)
            return True
        except Exception as e:
            print(f"✗ Failed to like tweet {tweet_id}: {str(e)}")
            return False

    def retweet(self, tweet_id: str) -> bool:
        """Retweet a tweet"""
        try:
            me = self.client.get_me()
            user_id = me.data.id

            self.client.retweet(user_id=user_id, tweet_id=tweet_id)
            return True
        except Exception as e:
            print(f"✗ Failed to retweet {tweet_id}: {str(e)}")
            return False

    def reply_to_tweet(self, tweet_id: str, text: str) -> Optional[str]:
        """Reply to a tweet"""
        try:
            response = self.client.create_tweet(
                text=text,
                in_reply_to_tweet_id=tweet_id
            )
            return response.data['id']
        except Exception as e:
            print(f"✗ Failed to reply to tweet {tweet_id}: {str(e)}")
            return None

    def get_user_tweets(self, username: str, max_results: int = 10) -> List[Dict]:
        """Get recent tweets from a user"""
        try:
            # Get user ID from username
            user = self.client.get_user(username=username)
            if not user.data:
                return []

            user_id = user.data.id

            # Get user tweets
            response = self.client.get_users_tweets(
                id=user_id,
                max_results=max_results,
                tweet_fields=['created_at', 'public_metrics']
            )

            if not response.data:
                return []

            tweets = []
            for tweet in response.data:
                tweets.append({
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'metrics': tweet.public_metrics
                })

            return tweets

        except Exception as e:
            print(f"✗ Failed to get tweets from {username}: {str(e)}")
            return []

    def get_my_info(self) -> Dict:
        """Get authenticated user information"""
        try:
            me = self.client.get_me(user_fields=['public_metrics'])
            return {
                'id': me.data.id,
                'username': me.data.username,
                'name': me.data.name,
                'metrics': me.data.public_metrics
            }
        except Exception as e:
            print(f"✗ Failed to get user info: {str(e)}")
            return {}
