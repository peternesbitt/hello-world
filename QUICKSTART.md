# 🚀 Quick Start Guide

Get started with Twitter Viral Bot in 5 minutes!

## 1️⃣ Install

```bash
# Clone and navigate
git clone https://github.com/peternesbitt/hello-world.git
cd hello-world

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install
pip install -r requirements.txt
pip install -e .
```

## 2️⃣ Configure

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env  # or use your favorite editor
```

Add your keys:
```
OPENAI_API_KEY=sk-...
TWITTER_API_KEY=...
TWITTER_API_SECRET=...
TWITTER_ACCESS_TOKEN=...
TWITTER_ACCESS_TOKEN_SECRET=...
TWITTER_BEARER_TOKEN=...
```

### Getting API Keys

**OpenAI**: https://platform.openai.com/api-keys
**Twitter**: https://developer.twitter.com/en/portal/dashboard

## 3️⃣ Test Configuration

```bash
twitter-bot status
```

You should see your Twitter account info.

## 4️⃣ Create Your First Thread

```bash
twitter-bot create "Why AI will change everything in 2026"
```

This will:
- Research the topic with GPT-4
- Generate a viral thread (5-10 tweets)
- Create infographics
- Display the complete thread

## 5️⃣ Post to Twitter (Optional)

```bash
twitter-bot create "Your idea here" --post
```

Or save for later:
```bash
twitter-bot create "Your idea" --output my_thread.json
twitter-bot post my_thread.json
```

## 6️⃣ Auto-Engagement

Grow your audience by engaging with relevant tweets:

```bash
# Dry run first (recommended)
twitter-bot engage \
  -t "AI" \
  -t "machine learning" \
  --niche "AI education" \
  --dry-run

# Then go live
twitter-bot engage \
  -t "AI" \
  -t "machine learning" \
  --niche "AI education" \
  --live
```

## 📚 Common Commands

### Create Thread with Options
```bash
twitter-bot create "Topic" \
  --depth deep \
  --style controversial \
  --optimize \
  --create-images
```

### Generate Different Angles
```bash
twitter-bot angles "Your topic" --count 5
```

### Create Custom Infographic
```bash
twitter-bot infographic \
  --stat "85%" \
  --context "of users love this" \
  --output stat.png
```

## 🎯 Your First Day Strategy

1. **Morning** (9 AM): Create and post a thread
   ```bash
   twitter-bot create "Morning productivity tip" --post
   ```

2. **Midday** (12 PM): Run engagement bot
   ```bash
   twitter-bot engage -t "your_topic" --niche "your niche" --live
   ```

3. **Evening** (6 PM): Create and post another thread
   ```bash
   twitter-bot create "Evening insight" --post
   ```

4. **Night** (9 PM): Final engagement round
   ```bash
   twitter-bot engage -t "your_topic" --niche "your niche" --live
   ```

## 🔥 Pro Tips

1. **Start with deep research**: `--depth deep` for best results
2. **Test styles**: Try `engaging`, `educational`, `controversial`, `storytelling`
3. **Use dry-run first**: Always test engagement bot in dry-run mode
4. **Save good threads**: Use `--output` to save for posting at optimal times
5. **Track what works**: Higher viral scores (8+) typically perform better

## ⚠️ Important Notes

- **API Costs**: OpenAI GPT-4 is not free (typically $0.01-0.03 per thread)
- **Rate Limits**: Twitter has rate limits - the bot respects them automatically
- **Engagement**: Start with 20-30 engagements per hour to stay safe
- **Quality > Quantity**: Focus on high-quality engagement (score 7+)

## 🆘 Troubleshooting

**"Configuration Error"**
→ Check your `.env` file has all required keys

**"Twitter API error: 403"**
→ Verify your Twitter app has Read/Write permissions

**"OpenAI API error"**
→ Check your API key and billing status

**Images not generating**
→ Install fonts: `sudo apt-get install fonts-dejavu`

## 📖 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [examples/](examples/) for Python API usage
- Join the community for tips and tricks

---

**Ready to go viral? Start creating!** 🚀
