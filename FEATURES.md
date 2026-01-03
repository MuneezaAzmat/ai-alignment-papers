# New Personalization Features

## Overview

Your AI Alignment Papers Tracker now includes powerful personalization and learning capabilities that allow you to customize rankings and help the AI learn your preferences.

## 🎯 Custom Affiliation Rankings

### What It Does
- Add your own trusted organizations to the ranking system
- Adjust scores for any affiliation (0-10 scale)
- System automatically re-ranks all papers when you update preferences

### How to Use
1. Click "⚙️ Manage Rankings" in the header
2. Add new affiliations using the form
3. Adjust scores using the number inputs
4. Delete custom affiliations if needed
5. Filter by "All", "Custom Only", or "Defaults Only"

### Example Use Cases
- Prioritize papers from specific research groups you follow
- Add emerging AI safety organizations not in the defaults
- Lower the ranking of sources you find less relevant

## ⭐ Summary Rating System

### What It Does
- Rate the quality of AI-generated summaries (1-5 stars)
- System learns from your ratings to improve future summaries
- Track which summaries are most helpful

### How to Use
1. Read a paper's summary
2. Click the stars to rate (1-5, where 5 is best)
3. Your rating is saved instantly
4. Future summaries will be adjusted based on aggregate feedback

### What It Learns
- Summary length preferences
- Level of technical detail you prefer
- Focus areas (methodology vs. results vs. implications)

## 🎚️ Manual Rank Overrides

### What It Does
- Override the calculated rank for specific papers
- Useful for promoting papers you find exceptionally valuable
- System tracks these preferences to learn your priorities

### How to Use
1. Find a paper on the main page
2. Click "Set Custom Rank" button
3. Enter a rank (0-10) or leave empty to clear override
4. Paper will immediately move to new position in the list

### Example Use Cases
- Boost a particularly insightful paper
- Demote papers that don't meet your quality standards
- Create your own "must read" category (rank 10+)

## 🧠 AI Learning System

### What It Learns

The system analyzes three types of feedback:

1. **Summary Ratings**: Which summary styles you prefer
2. **Rank Adjustments**: Which types of papers you value
3. **Affiliation Preferences**: Which organizations you trust

### How It Improves Summaries

When generating new summaries, the system:
- Incorporates preferences from highly-rated summaries
- Avoids patterns from poorly-rated summaries
- Adjusts technical depth based on your ratings
- Emphasizes aspects you've shown interest in

### Viewing Learning Insights

Visit the Preferences page to see:
- Average summary rating you've given
- Number of manual rank adjustments
- Affiliations you've boosted or lowered
- AI-generated insights about your preferences
- How future summaries will be tailored

## 📊 Analytics & Insights

### Available Metrics

The preferences page shows:
- **Summary Quality**: Your average rating and total ratings given
- **Ranking Adjustments**: How many papers you've manually ranked
- **Preferred Sources**: Affiliations you've consistently boosted
- **AI Learning Insights**: What the system has learned from your feedback

### Understanding Your Data

All your feedback is stored locally in the database:
- `summary_rating`: Your 1-5 star ratings
- `user_rank_override`: Manual rank overrides for papers
- `affiliation_preferences`: Your custom affiliation scores
- `user_feedback`: Historical log of all your adjustments

## 🔄 How Everything Works Together

1. **You fetch papers** → System ranks them by default affiliations
2. **You add custom affiliations** → Papers are re-ranked immediately
3. **You rate summaries** → System learns your preferences
4. **You override ranks** → System learns which papers you value
5. **New papers arrive** → Ranked using your preferences
6. **New summaries generated** → Tailored to your learned preferences

## 💡 Best Practices

### Getting Started
1. Start by rating 5-10 summaries to establish baseline preferences
2. Add a few custom affiliations for sources you specifically trust or follow
3. Override ranks for 2-3 papers to establish priority patterns

### Ongoing Use
- Rate summaries consistently to improve learning
- Adjust affiliation scores as your interests evolve
- Check the insights page periodically to see what the system has learned
- Use manual rank overrides sparingly for exceptional papers

### Maximizing Learning
- Be consistent with ratings (don't rate everything 5 stars)
- Use the full 1-5 scale to provide clear feedback
- Add specific organizations rather than broad categories
- Revisit preferences every few weeks as new papers arrive

## 🛠️ Technical Details

### Database Schema
- `papers.summary_rating`: INTEGER (1-5)
- `papers.user_rank_override`: FLOAT (0.0-10.0+)
- `affiliation_preferences`: Custom sources with scores
- `user_feedback`: Audit log of all preference changes

### Learning Algorithm
- Analyzes feedback patterns to generate prompt enhancements
- Identifies preferred vs. disliked summary characteristics
- Tracks affiliation adjustments to learn source preferences
- Applies learned preferences to future summary generation

### Privacy
- All data is stored locally in your SQLite database
- No data is sent to external services except paper summaries to Claude API
- You can export or delete your preferences at any time

## 🔮 Future Enhancements

Potential additions based on this foundation:
- Automatic affiliation discovery from your highly-rated papers
- Topic-based ranking in addition to affiliation-based
- Similarity matching to recommend papers based on what you've liked
- Export learning profiles to share with collaborators
- Multi-user support with separate preference profiles
