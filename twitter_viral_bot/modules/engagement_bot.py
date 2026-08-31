"""
Engagement automation - Intelligently engages with relevant Twitter users
"""
from openai import OpenAI
from typing import List, Dict, Optional
import json
import time
from datetime import datetime, timedelta
from .twitter_client import TwitterClient
from ..config import Config


class EngagementBot:
    """Automates intelligent Twitter engagement to grow followers"""

    def __init__(self, twitter_client: TwitterClient):
        self.twitter = twitter_client
        self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = "gpt-4-turbo-preview"
        self.engagement_count = 0
        self.hourly_limit = Config.ENGAGEMENT_LIMIT_PER_HOUR
        self.last_reset = datetime.now()

    def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits"""
        # Reset counter every hour
        if datetime.now() - self.last_reset > timedelta(hours=1):
            self.engagement_count = 0
            self.last_reset = datetime.now()

        return self.engagement_count < self.hourly_limit

    def find_relevant_tweets(
        self,
        topics: List[str],
        hashtags: Optional[List[str]] = None,
        max_per_topic: int = 5
    ) -> List[Dict]:
        """
        Find relevant tweets to engage with

        Args:
            topics: List of topics/keywords to search for
            hashtags: Optional list of hashtags to include
            max_per_topic: Maximum tweets per topic

        Returns:
            List of relevant tweet data
        """
        all_tweets = []

        # Use configured hashtags if none provided
        if not hashtags:
            hashtags = Config.TARGET_HASHTAGS

        # Search for each topic
        for topic in topics:
            queries = [
                f"{topic} -is:retweet lang:en",
                f"#{topic.replace('#', '')} -is:retweet lang:en"
            ]

            # Add hashtag queries
            for hashtag in hashtags:
                queries.append(f"{hashtag} {topic} -is:retweet lang:en")

            for query in queries[:2]:  # Limit queries per topic
                tweets = self.twitter.search_tweets(query, max_results=max_per_topic)
                all_tweets.extend(tweets)

                time.sleep(1)  # Rate limit consideration

        # Remove duplicates
        seen_ids = set()
        unique_tweets = []
        for tweet in all_tweets:
            if tweet['id'] not in seen_ids:
                seen_ids.add(tweet['id'])
                unique_tweets.append(tweet)

        return unique_tweets

    def analyze_tweet_relevance(
        self,
        tweet_text: str,
        our_niche: str
    ) -> Dict:
        """
        Use AI to analyze if a tweet is relevant and how to engage

        Args:
            tweet_text: The tweet text
            our_niche: Our content niche/focus

        Returns:
            Analysis with engagement recommendation
        """
        prompt = f"""Analyze this tweet for engagement opportunity:

Tweet: "{tweet_text}"
Our niche: {our_niche}

Determine:
1. Is this relevant to our niche? (true/false)
2. Engagement quality (1-10 score)
3. Best engagement type: "like", "retweet", "reply", or "skip"
4. If reply, suggest a thoughtful, value-adding comment (max 280 chars)

Respond in JSON:
{{
    "relevant": true/false,
    "quality_score": 8,
    "engagement_type": "reply",
    "suggested_reply": "Great insight! This aligns with...",
    "reasoning": "Why this engagement makes sense"
}}"""

        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a social media engagement strategist who helps build authentic connections."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            return json.loads(response.choices[0].message.content)

        except Exception as e:
            return {
                "relevant": False,
                "quality_score": 0,
                "engagement_type": "skip",
                "suggested_reply": "",
                "reasoning": f"Analysis failed: {str(e)}"
            }

    def engage_with_tweet(
        self,
        tweet: Dict,
        analysis: Dict,
        dry_run: bool = False
    ) -> bool:
        """
        Engage with a tweet based on analysis

        Args:
            tweet: Tweet data
            analysis: Engagement analysis
            dry_run: If True, only simulate engagement

        Returns:
            True if engagement was successful
        """
        if not self._check_rate_limit():
            print(f"⚠ Rate limit reached ({self.hourly_limit}/hour)")
            return False

        engagement_type = analysis.get("engagement_type", "skip")
        tweet_id = tweet['id']

        if dry_run:
            print(f"[DRY RUN] Would {engagement_type} tweet {tweet_id}")
            return True

        success = False

        if engagement_type == "like":
            success = self.twitter.like_tweet(tweet_id)
            if success:
                print(f"♥ Liked tweet {tweet_id}")

        elif engagement_type == "retweet":
            success = self.twitter.retweet(tweet_id)
            if success:
                print(f"🔄 Retweeted {tweet_id}")

        elif engagement_type == "reply":
            reply_text = analysis.get("suggested_reply", "")
            if reply_text:
                reply_id = self.twitter.reply_to_tweet(tweet_id, reply_text)
                success = reply_id is not None
                if success:
                    print(f"💬 Replied to tweet {tweet_id}")

        if success:
            self.engagement_count += 1

        return success

    def auto_engage(
        self,
        topics: List[str],
        our_niche: str,
        max_engagements: int = 20,
        min_quality_score: int = 6,
        dry_run: bool = False
    ) -> Dict:
        """
        Automatically find and engage with relevant tweets

        Args:
            topics: Topics to search for
            our_niche: Description of our content niche
            max_engagements: Maximum number of engagements
            min_quality_score: Minimum quality score (1-10)
            dry_run: If True, simulate without actual engagement

        Returns:
            Summary of engagement activity
        """
        print(f"\n{'='*60}")
        print(f"🤖 Starting Auto-Engagement")
        print(f"Topics: {', '.join(topics)}")
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
        print(f"{'='*60}\n")

        # Find relevant tweets
        print("🔍 Searching for relevant tweets...")
        tweets = self.find_relevant_tweets(topics, max_per_topic=10)
        print(f"Found {len(tweets)} potential tweets\n")

        engagements = {
            "analyzed": 0,
            "liked": 0,
            "retweeted": 0,
            "replied": 0,
            "skipped": 0
        }

        for tweet in tweets:
            if engagements["liked"] + engagements["retweeted"] + engagements["replied"] >= max_engagements:
                break

            if not self._check_rate_limit():
                break

            # Analyze tweet
            print(f"\nAnalyzing: {tweet['text'][:100]}...")
            analysis = self.analyze_tweet_relevance(tweet['text'], our_niche)
            engagements["analyzed"] += 1

            # Check if meets quality threshold
            if not analysis.get("relevant") or analysis.get("quality_score", 0) < min_quality_score:
                engagements["skipped"] += 1
                print(f"⊘ Skipped (Score: {analysis.get('quality_score', 0)}/10)")
                continue

            # Engage
            print(f"✓ Quality score: {analysis['quality_score']}/10")
            print(f"→ Action: {analysis['engagement_type']}")

            success = self.engage_with_tweet(tweet, analysis, dry_run=dry_run)

            if success:
                eng_type = analysis['engagement_type']
                if eng_type == "like":
                    engagements["liked"] += 1
                elif eng_type == "retweet":
                    engagements["retweeted"] += 1
                elif eng_type == "reply":
                    engagements["replied"] += 1

            # Small delay between engagements
            time.sleep(3)

        # Summary
        print(f"\n{'='*60}")
        print(f"📊 Engagement Summary")
        print(f"{'='*60}")
        print(f"Analyzed: {engagements['analyzed']}")
        print(f"Liked: {engagements['liked']}")
        print(f"Retweeted: {engagements['retweeted']}")
        print(f"Replied: {engagements['replied']}")
        print(f"Skipped: {engagements['skipped']}")
        print(f"{'='*60}\n")

        return engagements

    def find_influencers(
        self,
        topic: str,
        min_followers: int = 10000,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Find influencers in a topic area to potentially engage with

        Args:
            topic: Topic to search for
            min_followers: Minimum follower count
            max_results: Maximum number of influencers

        Returns:
            List of influencer data
        """
        # Search for high-engagement tweets in the topic
        query = f"{topic} min_faves:100 -is:retweet lang:en"
        tweets = self.twitter.search_tweets(query, max_results=max_results * 2)

        # Extract unique authors (basic influencer identification)
        influencers = []
        seen_authors = set()

        for tweet in tweets:
            author_id = tweet.get('author_id')
            if author_id not in seen_authors:
                seen_authors.add(author_id)
                influencers.append({
                    'author_id': author_id,
                    'sample_tweet': tweet
                })

        return influencers[:max_results]
