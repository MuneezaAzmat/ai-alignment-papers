from apscheduler.schedulers.background import BackgroundScheduler
from app.fetcher import fetch_recent_papers
from app.summarizer import summarize_papers
from app.config import CHECK_INTERVAL_HOURS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scheduled_fetch_and_summarize():
    """
    Scheduled job to fetch new papers and generate summaries.
    """
    logger.info("Running scheduled paper fetch and summarization...")

    try:
        # Fetch new papers
        new_papers = fetch_recent_papers(days_back=CHECK_INTERVAL_HOURS // 24 + 1, max_results=100)
        logger.info(f"Fetched {new_papers} new papers")

        # Generate summaries for papers without them
        if new_papers > 0:
            summarized = summarize_papers(limit=20)
            logger.info(f"Generated {summarized} summaries")

    except Exception as e:
        logger.error(f"Error in scheduled job: {e}")

def start_scheduler():
    """
    Start the background scheduler for periodic paper fetching.
    """
    scheduler = BackgroundScheduler()

    # Schedule the job to run every CHECK_INTERVAL_HOURS
    scheduler.add_job(
        func=scheduled_fetch_and_summarize,
        trigger='interval',
        hours=CHECK_INTERVAL_HOURS,
        id='fetch_papers',
        name='Fetch and summarize AI alignment papers',
        replace_existing=True
    )

    scheduler.start()
    logger.info(f"Scheduler started. Will check for new papers every {CHECK_INTERVAL_HOURS} hours.")

    return scheduler
