import tweepy
import config
from logger import logger


class TwitterService:
    def __init__(self):
        self.api = None
        self.client = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Twitter API using both v1.1 and v2"""
        try:
            # Twitter API v1.1 authentication (for legacy features if needed)
            auth = tweepy.OAuthHandler(
                config.TWITTER_API_KEY, config.TWITTER_API_SECRET
            )
            auth.set_access_token(
                config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET
            )
            self.api = tweepy.API(auth, wait_on_rate_limit=True)

            # Twitter API v2 authentication (for posting tweets)
            self.client = tweepy.Client(
                bearer_token=config.TWITTER_BEARER_TOKEN,
                consumer_key=config.TWITTER_API_KEY,
                consumer_secret=config.TWITTER_API_SECRET,
                access_token=config.TWITTER_ACCESS_TOKEN,
                access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET,
                wait_on_rate_limit=True,
            )

            # Test authentication
            self._test_authentication()
            logger.info("Successfully authenticated with Twitter API")

        except Exception as e:
            logger.error("Error authenticating with Twitter API: %s", e)
            raise

    def _test_authentication(self):
        """Test if authentication is working"""
        try:
            # Test v2 API
            me = self.client.get_me()
            logger.info("Authenticated as: %s (@%s)", me.data.name, me.data.username)
        except Exception as e:
            logger.error("Twitter API authentication test failed: %s", e)
            raise

    def post_tweet(self, message):
        """Post a tweet"""
        try:
            if len(message) > 280:
                logger.warning(
                    "Tweet message too long (%d chars), truncating", len(message)
                )
                message = message[:277] + "..."

            response = self.client.create_tweet(text=message)
            tweet_id = response.data["id"]

            logger.info("Successfully posted tweet with ID: %s", tweet_id)
            return tweet_id

        except tweepy.TooManyRequests:
            logger.error("Rate limit exceeded when posting tweet")
            return None
        except tweepy.Forbidden:
            logger.error("Forbidden: Check API permissions and authentication")
            return None
        except Exception as e:
            logger.error("Error posting tweet: %s", e)
            return None

    def post_thread(self, messages):
        """Post a Twitter thread"""
        tweet_ids = []
        previous_tweet_id = None

        for i, message in enumerate(messages):
            try:
                if len(message) > 280:
                    logger.warning(
                        "Thread message %d too long (%d chars), truncating",
                        i + 1,
                        len(message),
                    )
                    message = message[:277] + "..."

                if previous_tweet_id:
                    response = self.client.create_tweet(
                        text=message, in_reply_to_tweet_id=previous_tweet_id
                    )
                else:
                    response = self.client.create_tweet(text=message)

                tweet_id = response.data["id"]
                tweet_ids.append(tweet_id)
                previous_tweet_id = tweet_id

                logger.info(
                    "Posted thread tweet %d/%d with ID: %s",
                    i + 1,
                    len(messages),
                    tweet_id,
                )

            except Exception as e:
                logger.error("Error posting thread tweet %d: %s", i + 1, e)
                break

        return tweet_ids

    def get_account_info(self):
        """Get account information"""
        try:
            me = self.client.get_me(user_fields=["public_metrics"])
            return {
                "username": me.data.username,
                "name": me.data.name,
                "followers": me.data.public_metrics["followers_count"],
                "following": me.data.public_metrics["following_count"],
                "tweets": me.data.public_metrics["tweet_count"],
            }
        except Exception as e:
            logger.error("Error getting account info: %s", e)
            return None
