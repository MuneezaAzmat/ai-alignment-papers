import arxiv
import json
import re
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

def extract_arxiv_id(input_string):
    """
    Extract arXiv ID from various input formats.

    Supports:
    - arXiv ID: 2301.12345
    - arXiv URL: https://arxiv.org/abs/2301.12345
    - arXiv PDF URL: https://arxiv.org/pdf/2301.12345.pdf

    Args:
        input_string: User input (ID or URL)

    Returns:
        str: Normalized arXiv ID or None if invalid
    """
    input_string = input_string.strip()

    # Pattern for arXiv ID (e.g., 2301.12345 or 2301.12345v2)
    arxiv_id_pattern = r'(\d{4}\.\d{4,5})(v\d+)?'

    # Try to extract from URL
    url_patterns = [
        r'arxiv\.org/abs/(\d{4}\.\d{4,5}(?:v\d+)?)',
        r'arxiv\.org/pdf/(\d{4}\.\d{4,5}(?:v\d+)?)',
    ]

    for pattern in url_patterns:
        match = re.search(pattern, input_string)
        if match:
            return match.group(1)

    # Try direct ID match
    match = re.match(arxiv_id_pattern, input_string)
    if match:
        return match.group(0)

    return None

def fetch_paper_by_id(arxiv_id):
    """
    Fetch a specific paper by arXiv ID and add it to database.

    Args:
        arxiv_id: arXiv ID (e.g., "2301.12345")

    Returns:
        dict: Result with success status and message
    """
    session = get_session()

    # Check if paper already exists
    existing = session.query(Paper).filter_by(id__contains=arxiv_id).first()
    if existing:
        session.close()
        return {
            'success': False,
            'message': 'Paper already exists in database',
            'paper_id': existing.id
        }

    try:
        # Search arXiv
        client = arxiv.Client()
        search = arxiv.Search(id_list=[arxiv_id])

        results = list(client.results(search))

        if not results:
            session.close()
            return {
                'success': False,
                'message': f'Paper not found on arXiv: {arxiv_id}'
            }

        result = results[0]

        # Extract author information
        authors_list = [author.name for author in result.authors]
        affiliations = extract_affiliations_from_authors(result.authors)

        # Calculate rank score
        rank_score = calculate_rank_score(authors_list, affiliations)

        # Create paper entry
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
            summary=None
        )

        session.add(paper)
        session.commit()

        paper_id = paper.id
        session.close()

        return {
            'success': True,
            'message': 'Paper added successfully',
            'paper_id': paper_id,
            'title': result.title
        }

    except Exception as e:
        session.close()
        return {
            'success': False,
            'message': f'Error fetching paper: {str(e)}'
        }
