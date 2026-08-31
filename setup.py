"""
Setup configuration for Twitter Viral Bot
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="twitter-viral-bot",
    version="1.0.0",
    author="Your Name",
    description="AI-powered Twitter content creation and engagement automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/peternesbitt/hello-world",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "tweepy>=4.14.0",
        "pillow>=10.0.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0",
        "aiohttp>=3.9.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
        "click>=8.1.0",
        "rich>=13.0.0",
        "schedule>=1.2.0",
        "python-dateutil>=2.8.0",
    ],
    entry_points={
        "console_scripts": [
            "twitter-bot=twitter_viral_bot.cli:cli",
        ],
    },
)
