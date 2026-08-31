"""
Thread builder - Creates viral Twitter threads from research
"""
from openai import OpenAI
from typing import Dict, List
import json
from ..config import Config


class ThreadBuilder:
    """Builds viral Twitter threads from research data"""

    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = "gpt-4-turbo-preview"
        self.max_tweet_length = 280

    def build_thread(self, research_data: Dict, style: str = "engaging") -> List[str]:
        """
        Build a Twitter thread from research data

        Args:
            research_data: Research results from ResearchEngine
            style: Writing style - 'engaging', 'educational', 'controversial', 'storytelling'

        Returns:
            List of tweets forming a thread
        """
        style_guides = {
            "engaging": "Write in a friendly, conversational tone with emojis and hooks",
            "educational": "Write in a clear, informative style with numbered points",
            "controversial": "Write with bold, debate-sparking statements that challenge common beliefs",
            "storytelling": "Write as a compelling narrative with a beginning, middle, and end"
        }

        prompt = f"""Create a viral Twitter thread from this research:

{json.dumps(research_data, indent=2)}

Style: {style_guides.get(style, style_guides['engaging'])}

Requirements:
1. First tweet MUST be a powerful hook that stops scrolling (max 280 chars)
2. Each tweet MUST be under 280 characters
3. Create 5-{Config.MAX_THREAD_LENGTH} tweets
4. Use line breaks for readability
5. End with a call-to-action (follow, retweet, comment)
6. Include relevant hashtags naturally (not all in one tweet)
7. Make it shareable and quotable

Return as JSON:
{{
    "tweets": [
        "Tweet 1 text here",
        "Tweet 2 text here",
        ...
    ],
    "thread_summary": "Brief description of thread content"
}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a viral Twitter content creator who understands engagement psychology and creates threads that get thousands of retweets."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            tweets = result.get("tweets", [])

            # Validate tweet lengths
            validated_tweets = []
            for tweet in tweets:
                if len(tweet) <= self.max_tweet_length:
                    validated_tweets.append(tweet)
                else:
                    # Truncate if needed
                    validated_tweets.append(tweet[:277] + "...")

            return validated_tweets

        except Exception as e:
            raise Exception(f"Thread building failed: {str(e)}")

    def optimize_for_virality(self, tweets: List[str]) -> List[str]:
        """
        Optimize thread for maximum virality

        Args:
            tweets: List of tweets in the thread

        Returns:
            Optimized list of tweets
        """
        prompt = f"""Optimize this Twitter thread for maximum virality:

{json.dumps(tweets, indent=2)}

Apply these viral optimization techniques:
1. Add power words and emotional triggers
2. Use curiosity gaps
3. Include social proof hints
4. Add urgency or scarcity
5. Make the first tweet irresistible
6. Each tweet must still be under 280 characters

Return optimized thread as JSON:
{{
    "tweets": ["optimized tweet 1", "optimized tweet 2", ...]
}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a viral marketing expert specializing in Twitter growth."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            return result.get("tweets", tweets)

        except Exception as e:
            return tweets

    def add_visual_markers(self, tweets: List[str]) -> List[str]:
        """
        Add visual elements like thread numbers and visual breaks

        Args:
            tweets: List of tweets

        Returns:
            Tweets with visual markers added
        """
        marked_tweets = []

        for i, tweet in enumerate(tweets):
            if i == 0:
                # First tweet gets a thread indicator
                marked_tweets.append(f"{tweet}\n\n🧵")
            elif i == len(tweets) - 1:
                # Last tweet
                marked_tweets.append(f"{tweet}\n\n---\n\nFound this helpful? Follow for more insights!")
            else:
                # Middle tweets
                marked_tweets.append(tweet)

        return marked_tweets

    def create_hook_variations(self, main_hook: str, count: int = 5) -> List[str]:
        """
        Create multiple variations of a hook to A/B test

        Args:
            main_hook: The original hook
            count: Number of variations to create

        Returns:
            List of hook variations
        """
        prompt = f"""Create {count} variations of this Twitter hook:

"{main_hook}"

Each variation should:
- Be max 280 characters
- Use different psychological triggers
- Maintain the core message
- Be attention-grabbing

Return as JSON:
{{
    "hooks": ["variation 1", "variation 2", ...]
}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            return result.get("hooks", [main_hook])

        except Exception as e:
            return [main_hook]
