#!/usr/bin/env python
"""
Example: Batch create multiple threads from a list of ideas
"""
import sys
sys.path.insert(0, '..')

import json
from pathlib import Path
from twitter_viral_bot.modules.research_engine import ResearchEngine
from twitter_viral_bot.modules.thread_builder import ThreadBuilder
from twitter_viral_bot.modules.infographic_generator import InfographicGenerator
from twitter_viral_bot.config import Config


def create_thread(idea, style="engaging", depth="deep"):
    """Create a thread from an idea"""
    print(f"\n{'='*60}")
    print(f"Creating thread: {idea}")
    print(f"{'='*60}")

    # Research
    print("Researching...")
    research_engine = ResearchEngine()
    research_data = research_engine.research_topic(idea, depth=depth)

    # Build thread
    print("Building thread...")
    thread_builder = ThreadBuilder()
    tweets = thread_builder.build_thread(research_data, style=style)
    tweets = thread_builder.optimize_for_virality(tweets)
    tweets = thread_builder.add_visual_markers(tweets)

    # Generate infographics
    print("Generating infographics...")
    infographic_gen = InfographicGenerator()
    images = infographic_gen.create_from_research(research_data)

    print(f"✓ Complete: {len(tweets)} tweets, {len(images)} images")

    return {
        "idea": idea,
        "research": research_data,
        "tweets": tweets,
        "images": [str(img) for img in images],
        "viral_score": research_data.get('viral_potential_score', 0)
    }


def main():
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration error: {e}")
        return

    # List of ideas to create threads for
    ideas = [
        "10 ChatGPT prompts that will 10x your productivity",
        "The future of remote work in 2026",
        "How AI is transforming software development",
        "5 coding habits that separate senior from junior developers",
        "The rise of AI agents and what it means for jobs"
    ]

    print("="*60)
    print("BATCH THREAD CREATION")
    print("="*60)
    print(f"Creating {len(ideas)} threads...\n")

    # Create output directory
    output_dir = Path("output/threads")
    output_dir.mkdir(parents=True, exist_ok=True)

    all_threads = []

    # Process each idea
    for i, idea in enumerate(ideas, 1):
        print(f"\n[{i}/{len(ideas)}]", end=" ")

        try:
            thread_data = create_thread(idea, style="engaging", depth="medium")
            all_threads.append(thread_data)

            # Save individual thread
            filename = idea.lower().replace(" ", "_")[:50] + ".json"
            filepath = output_dir / filename
            filepath.write_text(json.dumps(thread_data, indent=2))
            print(f"   Saved to: {filepath}")

        except Exception as e:
            print(f"   ✗ Error: {str(e)}")
            continue

    # Save summary
    summary = {
        "total_threads": len(all_threads),
        "threads": [
            {
                "idea": t["idea"],
                "tweets_count": len(t["tweets"]),
                "images_count": len(t["images"]),
                "viral_score": t["viral_score"]
            }
            for t in all_threads
        ]
    }

    summary_file = output_dir / "summary.json"
    summary_file.write_text(json.dumps(summary, indent=2))

    # Print summary
    print("\n" + "="*60)
    print("BATCH CREATION COMPLETE")
    print("="*60)
    print(f"Total threads created: {len(all_threads)}")
    print(f"Output directory: {output_dir}")
    print(f"\nThreads ranked by viral potential:")

    sorted_threads = sorted(all_threads, key=lambda x: x['viral_score'], reverse=True)
    for i, thread in enumerate(sorted_threads, 1):
        print(f"  {i}. [{thread['viral_score']}/10] {thread['idea'][:60]}...")

    print(f"\nSummary saved to: {summary_file}")
    print("\nYou can now review and post these threads using:")
    print("  twitter-bot post <thread_file.json>")


if __name__ == "__main__":
    main()
