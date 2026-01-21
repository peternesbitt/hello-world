"""
Main CLI interface for Twitter Viral Bot
"""
import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
import json
from pathlib import Path

from .config import Config
from .modules.research_engine import ResearchEngine
from .modules.thread_builder import ThreadBuilder
from .modules.infographic_generator import InfographicGenerator
from .modules.twitter_client import TwitterClient
from .modules.engagement_bot import EngagementBot

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    🚀 Twitter Viral Bot - AI-Powered Content Creation & Engagement

    Turn your ideas into viral Twitter threads with AI research,
    infographics, and automated engagement.
    """
    try:
        Config.validate()
    except ValueError as e:
        console.print(f"[red]Configuration Error:[/red] {str(e)}")
        raise click.Abort()


@cli.command()
@click.argument('idea')
@click.option('--depth', type=click.Choice(['quick', 'medium', 'deep']), default='deep',
              help='Research depth level')
@click.option('--style', type=click.Choice(['engaging', 'educational', 'controversial', 'storytelling']),
              default='engaging', help='Thread writing style')
@click.option('--optimize/--no-optimize', default=True, help='Apply viral optimization')
@click.option('--create-images/--no-images', default=True, help='Generate infographics')
@click.option('--post/--no-post', default=False, help='Post to Twitter immediately')
@click.option('--output', type=click.Path(), help='Save thread to JSON file')
def create(idea, depth, style, optimize, create_images, post, output):
    """
    Create a viral Twitter thread from an idea

    Example: twitter-bot create "The future of AI agents"
    """
    console.print(Panel.fit(
        f"[bold cyan]Creating viral thread from idea:[/bold cyan]\n{idea}",
        title="🎯 Twitter Viral Bot"
    ))

    # Initialize modules
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:

        # Research
        task = progress.add_task("[cyan]Researching topic...", total=None)
        research_engine = ResearchEngine()
        research_data = research_engine.research_topic(idea, depth=depth)
        progress.update(task, completed=True)

        console.print(f"[green]✓[/green] Research complete")
        console.print(f"  • Main topic: {research_data.get('main_topic', 'N/A')}")
        console.print(f"  • Viral potential: {research_data.get('viral_potential_score', 0)}/10")
        console.print(f"  • Key points: {len(research_data.get('key_points', []))}")

        # Build thread
        task = progress.add_task("[cyan]Building thread...", total=None)
        thread_builder = ThreadBuilder()
        tweets = thread_builder.build_thread(research_data, style=style)

        if optimize:
            tweets = thread_builder.optimize_for_virality(tweets)
            tweets = thread_builder.add_visual_markers(tweets)

        progress.update(task, completed=True)
        console.print(f"[green]✓[/green] Thread built ({len(tweets)} tweets)")

        # Generate infographics
        image_paths = []
        if create_images:
            task = progress.add_task("[cyan]Generating infographics...", total=None)
            infographic_gen = InfographicGenerator()
            image_paths = infographic_gen.create_from_research(research_data)
            progress.update(task, completed=True)
            console.print(f"[green]✓[/green] Generated {len(image_paths)} infographics")

    # Display thread
    console.print("\n" + "="*60)
    console.print("[bold]📱 Your Viral Thread:[/bold]")
    console.print("="*60 + "\n")

    for i, tweet in enumerate(tweets, 1):
        console.print(f"[bold cyan]Tweet {i}:[/bold cyan]")
        console.print(tweet)
        console.print()

    # Show images
    if image_paths:
        console.print("[bold]🖼️  Generated Images:[/bold]")
        for img_path in image_paths:
            console.print(f"  • {img_path}")
        console.print()

    # Save to file
    if output:
        output_data = {
            "idea": idea,
            "research": research_data,
            "tweets": tweets,
            "images": [str(p) for p in image_paths],
            "settings": {
                "depth": depth,
                "style": style,
                "optimized": optimize
            }
        }

        output_path = Path(output)
        output_path.write_text(json.dumps(output_data, indent=2))
        console.print(f"[green]✓[/green] Saved to {output}")

    # Post to Twitter
    if post:
        if click.confirm("\n🚀 Post this thread to Twitter now?", default=False):
            twitter = TwitterClient()

            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
                task = progress.add_task("[cyan]Posting to Twitter...", total=None)
                tweet_ids = twitter.post_thread(tweets, media_paths=image_paths if image_paths else None)
                progress.update(task, completed=True)

            if tweet_ids:
                console.print(f"\n[green]✓[/green] Thread posted successfully!")
                console.print(f"View at: https://twitter.com/user/status/{tweet_ids[0]}")
            else:
                console.print("[red]✗[/red] Failed to post thread")


@cli.command()
@click.option('--topics', '-t', multiple=True, required=True, help='Topics to search for')
@click.option('--niche', required=True, help='Your content niche description')
@click.option('--max-engagements', default=20, help='Maximum engagements per run')
@click.option('--min-quality', default=6, type=click.IntRange(1, 10), help='Minimum quality score (1-10)')
@click.option('--dry-run/--live', default=True, help='Dry run (simulate) or live engagement')
def engage(topics, niche, max_engagements, min_quality, dry_run):
    """
    Auto-engage with relevant tweets to grow your audience

    Example: twitter-bot engage -t AI -t "machine learning" --niche "AI education"
    """
    console.print(Panel.fit(
        f"[bold cyan]Auto-Engagement Mode[/bold cyan]\n"
        f"Topics: {', '.join(topics)}\n"
        f"Niche: {niche}\n"
        f"Mode: {'DRY RUN' if dry_run else 'LIVE'}",
        title="🤖 Engagement Bot"
    ))

    if not dry_run:
        if not click.confirm("\n⚠️  Running in LIVE mode. This will engage with real tweets. Continue?"):
            return

    # Initialize
    twitter = TwitterClient()
    bot = EngagementBot(twitter)

    # Run engagement
    results = bot.auto_engage(
        topics=list(topics),
        our_niche=niche,
        max_engagements=max_engagements,
        min_quality_score=min_quality,
        dry_run=dry_run
    )

    # Show results table
    table = Table(title="Engagement Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Count", style="green")

    table.add_row("Analyzed", str(results['analyzed']))
    table.add_row("Liked", str(results['liked']))
    table.add_row("Retweeted", str(results['retweeted']))
    table.add_row("Replied", str(results['replied']))
    table.add_row("Skipped", str(results['skipped']))

    console.print(table)


@cli.command()
@click.argument('idea')
@click.option('--count', default=5, help='Number of angles to generate')
def angles(idea, count):
    """
    Generate multiple viral angles for a topic

    Example: twitter-bot angles "Climate change solutions" --count 5
    """
    console.print(f"[cyan]Finding viral angles for:[/cyan] {idea}\n")

    research_engine = ResearchEngine()

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("[cyan]Generating angles...", total=None)
        angles_list = research_engine.find_viral_angles(idea)
        progress.update(task, completed=True)

    console.print("[bold]🎯 Viral Angles:[/bold]\n")
    for i, angle in enumerate(angles_list[:count], 1):
        console.print(f"{i}. {angle}")
    console.print()


@cli.command()
@click.option('--stat', required=True, help='Main statistic')
@click.option('--context', required=True, help='Context for the stat')
@click.option('--subtitle', help='Optional subtitle')
@click.option('--output', default='stat_card.png', help='Output filename')
def infographic(stat, context, subtitle, output):
    """
    Create a custom infographic

    Example: twitter-bot infographic --stat "85%" --context "Of users prefer AI" --output my_stat.png
    """
    infographic_gen = InfographicGenerator()

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("[cyan]Creating infographic...", total=None)
        path = infographic_gen.create_stat_card(stat, context, subtitle, output)
        progress.update(task, completed=True)

    console.print(f"[green]✓[/green] Infographic created: {path}")


@cli.command()
def status():
    """Check your Twitter account status and configuration"""
    console.print("[cyan]Checking configuration...[/cyan]\n")

    # Check config
    try:
        Config.validate()
        console.print("[green]✓[/green] Configuration valid")
    except ValueError as e:
        console.print(f"[red]✗[/red] Configuration error: {e}")
        return

    # Get Twitter info
    try:
        twitter = TwitterClient()
        info = twitter.get_my_info()

        if info:
            table = Table(title="Twitter Account Info")
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="green")

            table.add_row("Username", f"@{info.get('username', 'N/A')}")
            table.add_row("Name", info.get('name', 'N/A'))
            table.add_row("Followers", str(info.get('metrics', {}).get('followers_count', 0)))
            table.add_row("Following", str(info.get('metrics', {}).get('following_count', 0)))

            console.print(table)
        else:
            console.print("[red]✗[/red] Failed to get Twitter account info")

    except Exception as e:
        console.print(f"[red]✗[/red] Twitter API error: {e}")


@cli.command()
@click.argument('thread_file', type=click.Path(exists=True))
@click.option('--delay', default=2, help='Delay between tweets (seconds)')
def post(thread_file, delay):
    """
    Post a saved thread from JSON file

    Example: twitter-bot post my_thread.json
    """
    # Load thread
    thread_data = json.loads(Path(thread_file).read_text())
    tweets = thread_data.get('tweets', [])
    images = [Path(p) for p in thread_data.get('images', [])]

    console.print(f"[cyan]Loading thread from {thread_file}[/cyan]")
    console.print(f"  • {len(tweets)} tweets")
    console.print(f"  • {len(images)} images\n")

    if not click.confirm("Post this thread to Twitter?"):
        return

    twitter = TwitterClient()

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("[cyan]Posting to Twitter...", total=None)
        tweet_ids = twitter.post_thread(tweets, media_paths=images, delay_seconds=delay)
        progress.update(task, completed=True)

    if tweet_ids:
        console.print(f"\n[green]✓[/green] Thread posted successfully!")
        console.print(f"View at: https://twitter.com/user/status/{tweet_ids[0]}")
    else:
        console.print("[red]✗[/red] Failed to post thread")


if __name__ == '__main__':
    cli()
