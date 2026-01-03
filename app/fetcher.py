import arxiv
import json
from datetime import datetime, timedelta
from app.database import get_session, Paper
from app.config import ALIGNMENT_KEYWORDS
from app.ranker import calculate_rank_score, extract_affiliations_from_authors

def is_alignment_paper(title, abstract):
    """
    Check if a paper is related to AI alignment based on keywords.

    Args:
        title: Paper title
        abstract: Paper abstract

    Returns:
        bool: True if paper is alignment-related
    """
    text = (title + ' ' + abstract).lower()

    for keyword in ALIGNMENT_KEYWORDS:
        if keyword.lower() in text:
            return True

    return False

def fetch_recent_papers(days_back=7, max_results=100):
    """
    Fetch recent AI papers from arXiv and filter for alignment-related content.

    Args:
        days_back: Number of days to look back
        max_results: Maximum number of papers to fetch

    Returns:
        int: Number of new papers added
    """
    session = get_session()
    new_papers_count = 0

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)

    # Build arXiv query for AI papers
    query = 'cat:cs.AI'

    # Create arXiv client and search
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    print(f"Fetching papers from arXiv (last {days_back} days)...")

    for result in client.results(search):
        # Check if paper is within date range
        if result.published.replace(tzinfo=None) < start_date:
            continue

        # Check if paper is alignment-related
        if not is_alignment_paper(result.title, result.summary):
            continue

        # Check if paper already exists in database
        existing_paper = session.query(Paper).filter_by(id=result.entry_id).first()
        if existing_paper:
            continue

        # Extract author information
        authors_list = [author.name for author in result.authors]
        affiliations = extract_affiliations_from_authors(result.authors)

        # Calculate rank score
        rank_score = calculate_rank_score(authors_list, affiliations)

        # Create new paper entry
        paper = Paper(
            id=result.entry_id,
            title=result.title,
            authors=json.dumps(authors_list),
            affiliations=json.dumps(affiliations) if affiliations else None,
            abstract=result.summary,
            published_date=result.published.replace(tzinfo=None),
            arxiv_url=result.entry_id,
            pdf_url=result.pdf_url,
            rank_score=rank_score,
            summary=None  # Will be generated separately
        )

        session.add(paper)
        new_papers_count += 1

        print(f"  Added: {result.title[:60]}... (rank: {rank_score})")

    session.commit()
    session.close()

    print(f"Fetched {new_papers_count} new alignment papers.")
    return new_papers_count

def get_papers_needing_summaries(limit=10):
    """
    Get papers that don't have summaries yet.

    Args:
        limit: Maximum number of papers to return

    Returns:
        List of Paper objects
    """
    session = get_session()
    papers = session.query(Paper).filter(Paper.summary.is_(None)).order_by(Paper.rank_score.desc()).limit(limit).all()
    session.close()
    return papers
