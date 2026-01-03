# AI Alignment Papers Tracker

An automated web application that monitors the latest AI alignment research papers from arXiv, ranks them by institutional impact, and generates AI-powered summaries using Claude.

## Features

### Core Functionality
- **Automatic Paper Fetching**: Retrieves AI alignment papers from arXiv based on relevant keywords
- **Intelligent Ranking**: Papers are ranked by author affiliations (OpenAI, Anthropic, Google DeepMind, etc.)
- **AI-Powered Summaries**: Claude generates concise, accessible summaries of each paper
- **Scheduled Updates**: Background scheduler checks for new papers at configurable intervals
- **Web Interface**: Clean, responsive UI to browse and filter papers
- **Filtering**: Filter papers by minimum rank score to focus on high-impact research

### Personalization & Learning
- **Custom Affiliation Rankings**: Add your own trusted sources and adjust ranking scores
- **Summary Ratings**: Rate summaries with a 5-star system to provide feedback
- **Manual Rank Overrides**: Set custom ranking scores for individual papers
- **AI Learning**: The system learns from your feedback to improve future summaries
- **Preference Insights**: View analytics about your preferences and what the system has learned

## Ranking System

Papers are automatically ranked based on author affiliations:

- **Score 10**: OpenAI, Anthropic
- **Score 9**: Google, DeepMind, Google DeepMind
- **Score 8**: Meta, Meta AI, Microsoft Research, Redwood Research, Alignment Research Center
- **Score 7**: Stanford, MIT, Berkeley, Oxford, Cambridge, CMU, ARC, CHAI, MIRI
- **Score 6**: ETH Zurich, University of Toronto, MILA, and other top institutions

Higher scores indicate papers from more prominent AI safety organizations and research groups.

## Installation

### Prerequisites

- Python 3.8 or higher
- An Anthropic API key ([get one here](https://console.anthropic.com/))

### Setup

1. Clone or navigate to the project directory:
```bash
cd ai-alignment-papers
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment configuration:
```bash
cp .env.example .env
```

5. Edit `.env` and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_actual_api_key_here
FLASK_SECRET_KEY=your_random_secret_key_here
CHECK_INTERVAL_HOURS=24
```

## Usage

### Starting the Application

Run the application:
```bash
python run.py
```

The web interface will be available at `http://localhost:5000`

### Initial Setup

1. Open `http://localhost:5000` in your browser
2. Click "Fetch New Papers" to retrieve recent AI alignment papers from arXiv
3. Click "Generate Summaries" to create AI summaries for the fetched papers
4. Papers will be displayed in order of rank score (highest first)

### Customizing Rankings

1. Click "⚙️ Manage Rankings" in the header to access preferences
2. **Add Custom Affiliations**: Enter organization names and assign ranking scores (0-10)
3. **Adjust Existing Scores**: Modify the score for any affiliation (custom or default)
4. **View Learning Insights**: See what the system has learned from your feedback
5. All papers are automatically re-ranked when you update preferences

### Rating & Feedback

On the main page, for each paper you can:
- **Rate Summaries**: Click the stars (1-5) to rate summary quality
- **Set Custom Ranks**: Click "Set Custom Rank" to override the calculated rank for a paper
- **View Learning**: Visit the preferences page to see how your feedback influences future summaries

The system analyzes your ratings and adjustments to:
- Tailor future summaries to your preferences
- Learn which types of papers you find most valuable
- Improve ranking accuracy based on your priorities

### Filtering Papers

Use the "Minimum Rank Score" dropdown to filter papers:
- **All Papers**: Show all papers regardless of ranking
- **High Impact (7+)**: Papers from top universities and research institutions
- **Very High Impact (8+)**: Papers from leading AI labs and safety organizations
- **Top Tier (9+)**: Papers from the most prominent AI research organizations

### Automatic Updates

The application runs a background scheduler that automatically:
- Checks for new papers every 24 hours (configurable)
- Fetches papers from the last day
- Generates summaries for new papers

## Project Structure

```
ai-alignment-papers/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── config.py            # Configuration and ranking settings
│   ├── database.py          # SQLAlchemy models and database setup
│   ├── fetcher.py           # arXiv paper fetching logic
│   ├── ranker.py            # Affiliation ranking system
│   ├── summarizer.py        # Claude API integration for summaries
│   └── routes.py            # Flask routes and API endpoints
├── templates/
│   └── index.html           # Main web interface
├── static/
│   └── css/
│       └── style.css        # Application styling
├── scheduler.py             # Background job scheduler
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variable template
└── README.md               # This file
```

## API Endpoints

### POST /api/fetch
Fetch new papers from arXiv.

Request body:
```json
{
  "days_back": 7,
  "max_results": 100
}
```

### POST /api/summarize
Generate summaries for papers without them.

Request body:
```json
{
  "limit": 10,
  "paper_ids": null
}
```

### GET /api/stats
Get database statistics.

Response:
```json
{
  "total_papers": 45,
  "papers_with_summaries": 30,
  "papers_without_summaries": 15,
  "high_rank_papers": 12
}
```

## Customization

### Modifying Alignment Keywords

Edit `app/config.py` and update the `ALIGNMENT_KEYWORDS` list to change which papers are fetched.

### Adjusting Affiliation Rankings

Edit `app/config.py` and modify the `PROMINENT_AFFILIATIONS` dictionary to add or change organization scores.

### Changing Check Interval

Update the `CHECK_INTERVAL_HOURS` value in your `.env` file to change how often the scheduler checks for new papers.

## Technical Details

### Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **APScheduler**: Background job scheduling
- **arxiv**: Python wrapper for arXiv API
- **anthropic**: Claude API client
- **SQLite**: Local database storage

### Database Schema

Papers are stored with:
- arXiv ID, title, authors, affiliations
- Abstract and AI-generated summary
- Published and fetched dates
- arXiv and PDF URLs
- Calculated rank score

## Troubleshooting

### No papers appearing
- Ensure you clicked "Fetch New Papers" at least once
- Check that there are recent AI alignment papers on arXiv
- Verify the alignment keywords match current research topics

### Summaries not generating
- Verify your `ANTHROPIC_API_KEY` is correct in `.env`
- Check that you have API credits available
- Look for error messages in the console output

### Scheduler not running
- The scheduler starts automatically with `run.py`
- Check console output for scheduler confirmation messages
- Ensure `CHECK_INTERVAL_HOURS` is set in `.env`

## Future Enhancements

Potential improvements:
- Add support for Alignment Forum posts
- Include citation counts and paper impact metrics
- Email notifications for high-priority papers
- Export functionality (PDF, CSV)
- User accounts and personalized filters
- Paper recommendations based on interests

## License

MIT License - feel free to modify and distribute as needed.

## Contributing

Contributions welcome! Areas for improvement:
- Additional paper sources beyond arXiv
- Enhanced ranking algorithms
- Better affiliation extraction from papers
- Improved UI/UX
- Test coverage
