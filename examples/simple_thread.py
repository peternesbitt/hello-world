#!/usr/bin/env python
"""
Simple example: Create and post a viral thread
"""
import sys
sys.path.insert(0, '..')

from twitter_viral_bot.modules.research_engine import ResearchEngine
from twitter_viral_bot.modules.thread_builder import ThreadBuilder
from twitter_viral_bot.modules.infographic_generator import InfographicGenerator
from twitter_viral_bot.modules.twitter_client import TwitterClient
from twitter_viral_bot.config import Config


def main():
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration error: {e}")
        return

    # Your idea
    idea = "The rise of AI coding assistants and their impact on software development"

    print(f"Creating thread about: {idea}\n")

    # Step 1: Research the topic
    print("1. Researching topic...")
    research_engine = ResearchEngine()
    research_data = research_engine.research_topic(idea, depth="deep")
    print(f"   ✓ Research complete")
    print(f"   • Main topic: {research_data.get('main_topic')}")
    print(f"   • Viral potential: {research_data.get('viral_potential_score')}/10\n")

    # Step 2: Build the thread
    print("2. Building thread...")
    thread_builder = ThreadBuilder()
    tweets = thread_builder.build_thread(research_data, style="engaging")

    # Optimize for virality
    tweets = thread_builder.optimize_for_virality(tweets)
    tweets = thread_builder.add_visual_markers(tweets)
    print(f"   ✓ Thread built ({len(tweets)} tweets)\n")

    # Step 3: Generate infographics
    print("3. Generating infographics...")
    infographic_gen = InfographicGenerator()
    images = infographic_gen.create_from_research(research_data)
    print(f"   ✓ Generated {len(images)} images\n")

    # Display the thread
    print("=" * 60)
    print("YOUR VIRAL THREAD:")
    print("=" * 60)
    for i, tweet in enumerate(tweets, 1):
        print(f"\nTweet {i}:")
        print(tweet)
    print("\n" + "=" * 60)

    # Ask to post
    response = input("\nPost this thread to Twitter? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        print("\n4. Posting to Twitter...")
        twitter = TwitterClient()
        tweet_ids = twitter.post_thread(tweets, media_paths=images[:len(tweets)])

        if tweet_ids:
            print(f"   ✓ Thread posted successfully!")
            print(f"   View at: https://twitter.com/user/status/{tweet_ids[0]}")
        else:
            print("   ✗ Failed to post thread")
    else:
        print("\nThread not posted. You can post it later using:")
        print("  twitter-bot post <saved_thread.json>")


if __name__ == "__main__":
    main()
