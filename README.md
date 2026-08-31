# 🚀 Twitter Viral Bot

**AI-Powered Twitter Content Creation & Engagement Automation**

Turn your initial ideas into viral Twitter threads with AI-powered research, professional infographics, and intelligent engagement automation.

## ✨ Features

- 🧠 **AI Research Engine**: Uses GPT-4 to deeply research topics, find sources, statistics, and expert insights
- 🧵 **Thread Generation**: Creates viral Twitter threads optimized for engagement
- 🎨 **Infographic Creation**: Automatically generates professional infographics from data
- 🤖 **Smart Engagement**: Intelligently finds and engages with relevant tweets to grow your audience
- 📊 **Viral Optimization**: Applies psychological triggers and viral mechanics to maximize reach
- 💡 **Multiple Angles**: Generate different perspectives on any topic
- 🎯 **Targeted Growth**: Engage with users in your niche to build authentic connections

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Twitter API credentials (API v2 with OAuth 1.0a)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/peternesbitt/hello-world.git
   cd hello-world
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package**
   ```bash
   pip install -e .
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   TWITTER_API_KEY=your_twitter_api_key
   TWITTER_API_SECRET=your_twitter_api_secret
   TWITTER_ACCESS_TOKEN=your_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
   TWITTER_BEARER_TOKEN=your_bearer_token
   ```

### Getting API Keys

#### OpenAI API
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Add billing information if needed

#### Twitter API
1. Apply for Twitter Developer access at https://developer.twitter.com
2. Create a new app in the Developer Portal
3. Generate API keys and tokens with Read/Write permissions
4. Enable OAuth 1.0a authentication

## 📖 Usage

### Check Configuration
```bash
twitter-bot status
```

### Create a Viral Thread

**Basic usage:**
```bash
twitter-bot create "The future of AI agents"
```

**Advanced options:**
```bash
twitter-bot create "Climate change solutions" \
  --depth deep \
  --style controversial \
  --optimize \
  --create-images \
  --output my_thread.json
```

**Post immediately:**
```bash
twitter-bot create "Productivity hacks for developers" --post
```

### Auto-Engagement

Automatically find and engage with relevant tweets to grow your audience:

**Dry run (recommended first):**
```bash
twitter-bot engage \
  -t "artificial intelligence" \
  -t "machine learning" \
  --niche "AI education and tutorials" \
  --max-engagements 20 \
  --min-quality 7 \
  --dry-run
```

**Live engagement:**
```bash
twitter-bot engage \
  -t "python programming" \
  -t "web development" \
  --niche "Python tutorials and tips" \
  --live
```

### Generate Content Angles

Find multiple viral angles for a topic:
```bash
twitter-bot angles "Remote work" --count 5
```

### Create Custom Infographics

```bash
twitter-bot infographic \
  --stat "85%" \
  --context "Of developers prefer remote work" \
  --subtitle "2024 Developer Survey" \
  --output remote_work_stat.png
```

### Post Saved Threads

```bash
twitter-bot post my_thread.json --delay 3
```

## 🎯 Use Cases

### 1. Content Creator
Create a week's worth of viral threads:
```bash
for topic in "AI trends" "Productivity tips" "Career advice"; do
  twitter-bot create "$topic" --optimize --create-images --output "${topic// /_}.json"
done
```

### 2. Thought Leader
Build authority in your niche:
```bash
# Research and post
twitter-bot create "The impact of AI on software engineering" --depth deep --post

# Engage with community
twitter-bot engage -t "software engineering" -t "AI" --niche "Tech leadership" --live
```

### 3. Growth Hacker
Maximize follower growth:
```bash
# Create viral content
twitter-bot create "10 ChatGPT prompts that changed my life" --style engaging --post

# Automated engagement
twitter-bot engage -t "ChatGPT" -t "AI prompts" --niche "AI productivity" --max-engagements 50 --live
```

## 🏗️ Architecture

```
twitter_viral_bot/
├── config.py                 # Configuration management
├── cli.py                    # Main CLI interface
└── modules/
    ├── research_engine.py    # AI-powered research
    ├── thread_builder.py     # Thread creation & optimization
    ├── infographic_generator.py  # Visual content creation
    ├── twitter_client.py     # Twitter API wrapper
    └── engagement_bot.py     # Automated engagement
```

## 🔧 Configuration Options

Edit `.env` to customize:

```bash
# Content Settings
MAX_THREAD_LENGTH=10          # Maximum tweets per thread
RESEARCH_DEPTH=deep           # quick, medium, or deep
VIRAL_OPTIMIZATION=True       # Apply viral optimization

# Engagement Settings
AUTO_ENGAGE=True              # Enable auto-engagement
ENGAGEMENT_LIMIT_PER_HOUR=30  # Rate limit for engagements
TARGET_HASHTAGS=#AI,#Tech     # Default hashtags to target
```

## 🤖 How It Works

### Content Creation Pipeline

1. **Research Phase**
   - AI analyzes your initial idea
   - Conducts deep research on the topic
   - Finds statistics, expert insights, and sources
   - Identifies viral angles and trending connections

2. **Thread Building**
   - Creates engaging hook (first tweet)
   - Structures content for maximum readability
   - Applies psychological triggers
   - Adds hashtags strategically
   - Includes call-to-action

3. **Visual Enhancement**
   - Generates stat cards for key statistics
   - Creates key points infographics
   - Designs quote cards for expert insights
   - Optimizes images for Twitter (16:9 ratio)

4. **Viral Optimization**
   - Adds power words and emotional triggers
   - Creates curiosity gaps
   - Includes social proof elements
   - Optimizes for engagement metrics

### Engagement Bot

1. **Discovery**
   - Searches for tweets matching your topics
   - Filters by language, engagement, and relevance

2. **AI Analysis**
   - Evaluates tweet relevance to your niche
   - Scores engagement quality (1-10)
   - Determines best engagement type

3. **Smart Engagement**
   - Likes high-quality relevant tweets
   - Retweets exceptional content
   - Replies with thoughtful, value-adding comments
   - Respects rate limits (default 30/hour)

## 📊 Best Practices

### Content Creation
- Use **deep research** for thought leadership content
- Apply **controversial style** for engagement
- Enable **viral optimization** for maximum reach
- Create **infographics** for visual appeal

### Engagement Automation
- Start with **dry-run mode** to test
- Set **min-quality 7+** for authentic engagement
- Target **specific hashtags** in your niche
- Keep **engagement limits reasonable** (20-30/hour)

### Growth Strategy
1. Post 1-2 viral threads per day
2. Run engagement bot 2-3 times daily
3. Focus on specific niche topics
4. Engage authentically, not spammy
5. Mix content styles (educational, controversial, storytelling)

## ⚠️ Rate Limits & Safety

- **Twitter API**: Respects all Twitter rate limits
- **Engagement Bot**: Default 30 engagements/hour (configurable)
- **OpenAI API**: Uses GPT-4 Turbo (costs apply)
- **Dry Run Mode**: Test without making actual posts/engagements

## 🐛 Troubleshooting

### "Configuration Error: Missing required configuration"
- Ensure all API keys are set in `.env`
- Check that `.env` is in the project root
- Verify API keys are valid

### "Twitter API error: 403 Forbidden"
- Check Twitter app permissions (Read/Write)
- Verify OAuth 1.0a is enabled
- Regenerate access tokens if needed

### "OpenAI API error"
- Verify API key is valid
- Check billing status on OpenAI platform
- Ensure sufficient credits

### Images not generating
- Install system fonts: `apt-get install fonts-dejavu`
- Check output directory exists and is writable

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Add support for other AI models (Claude, Gemini)
- Implement scheduling features
- Add analytics dashboard
- Support for other social platforms
- A/B testing capabilities
- Web scraping for real-time data

## 📄 License

MIT License - feel free to use for personal or commercial projects

## ⚡ Advanced Examples

### Schedule Daily Posts (with cron)
```bash
# Add to crontab (crontab -e)
0 9 * * * cd /path/to/hello-world && /path/to/venv/bin/twitter-bot create "Daily tip $(date +\%A)" --post
0 12,18 * * * cd /path/to/hello-world && /path/to/venv/bin/twitter-bot engage -t "your_topic" --niche "your niche" --live
```

### Batch Process Ideas
```bash
# Create ideas.txt with one idea per line
while IFS= read -r idea; do
  twitter-bot create "$idea" --output "threads/$(echo $idea | tr ' ' '_').json"
done < ideas.txt
```

### Hook Variations for A/B Testing
```bash
twitter-bot angles "Your topic" --count 10 > angles.txt
# Pick the best angle and create thread
```

## 🎓 Tips for Going Viral

1. **Hook is Everything**: First tweet must stop scrolling
2. **Use Numbers**: "7 ways to..." performs better than "Ways to..."
3. **Visual Content**: Threads with images get 2-3x more engagement
4. **Controversy**: Hot takes and contrarian views spark discussion
5. **Timing**: Post when your audience is most active
6. **Engagement**: Reply to comments quickly to boost algorithm
7. **Call-to-Action**: Always end with "Follow for more" or "RT if you agree"

## 🔮 Roadmap

- [ ] Analytics dashboard
- [ ] A/B testing for hooks
- [ ] Multi-platform support (LinkedIn, Threads)
- [ ] Automated reply bot
- [ ] Influencer collaboration finder
- [ ] Trending topic detector
- [ ] Content calendar integration

---

**Built with ❤️ using OpenAI GPT-4 and Twitter API v2**

For questions or issues, please open a GitHub issue.
