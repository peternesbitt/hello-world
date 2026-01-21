#!/usr/bin/env python
"""
Example: Auto-engage with relevant tweets to grow your audience
"""
import sys
sys.path.insert(0, '..')

from twitter_viral_bot.modules.twitter_client import TwitterClient
from twitter_viral_bot.modules.engagement_bot import EngagementBot
from twitter_viral_bot.config import Config


def main():
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration error: {e}")
        return

    # Initialize
    twitter = TwitterClient()
    bot = EngagementBot(twitter)

    # Define your niche and topics
    your_niche = "AI and machine learning education for developers"
    topics_to_search = [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "AI coding",
        "ChatGPT"
    ]

    print("=" * 60)
    print("AUTO-ENGAGEMENT BOT")
    print("=" * 60)
    print(f"Niche: {your_niche}")
    print(f"Topics: {', '.join(topics_to_search)}")
    print("=" * 60)

    # Ask for mode
    print("\nChoose mode:")
    print("1. Dry run (simulate without actual engagement)")
    print("2. Live mode (actual engagement)")

    choice = input("\nEnter choice (1 or 2): ")

    dry_run = True if choice == "1" else False

    if not dry_run:
        confirm = input("\n⚠️  LIVE MODE: This will engage with real tweets. Continue? (yes/no): ")
        if confirm.lower() not in ['yes', 'y']:
            print("Cancelled.")
            return

    # Run engagement bot
    results = bot.auto_engage(
        topics=topics_to_search,
        our_niche=your_niche,
        max_engagements=20,
        min_quality_score=7,
        dry_run=dry_run
    )

    # Summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"Tweets analyzed:  {results['analyzed']}")
    print(f"Tweets liked:     {results['liked']}")
    print(f"Tweets retweeted: {results['retweeted']}")
    print(f"Tweets replied:   {results['replied']}")
    print(f"Tweets skipped:   {results['skipped']}")
    print("=" * 60)

    total_engagements = results['liked'] + results['retweeted'] + results['replied']
    print(f"\nTotal engagements: {total_engagements}")

    if dry_run:
        print("\nThis was a dry run. Run in live mode to actually engage.")
    else:
        print("\n✓ Engagement complete! Check your Twitter activity.")


if __name__ == "__main__":
    main()
