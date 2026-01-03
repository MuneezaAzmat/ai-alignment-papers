import json
from app.config import PROMINENT_AFFILIATIONS

def get_user_preferences():
    """
    Get user affiliation preferences from database.
    Returns a dictionary merged with defaults.
    """
    from app.database import get_session, AffiliationPreference

    session = get_session()
    prefs = session.query(AffiliationPreference).all()
    session.close()

    # Start with default preferences
    all_prefs = dict(PROMINENT_AFFILIATIONS)

    # Override with user preferences
    for pref in prefs:
        all_prefs[pref.affiliation_name.lower()] = pref.rank_score

    return all_prefs

def calculate_rank_score(authors_data, affiliations_data, use_user_prefs=True):
    """
    Calculate a ranking score for a paper based on author affiliations.
    Higher scores indicate more prominent affiliations.

    Args:
        authors_data: List of author names (strings)
        affiliations_data: List of affiliation strings or None
        use_user_prefs: Whether to use user preferences (default: True)

    Returns:
        float: Rank score (0.0 to 10.0+)
    """
    if not affiliations_data:
        return 0.0

    max_score = 0.0

    # Get preferences (user + defaults)
    prefs = get_user_preferences() if use_user_prefs else PROMINENT_AFFILIATIONS

    # Parse affiliations if they're JSON strings
    if isinstance(affiliations_data, str):
        try:
            affiliations = json.loads(affiliations_data)
        except:
            affiliations = [affiliations_data]
    else:
        affiliations = affiliations_data or []

    # Check each affiliation against our prominent list
    for affiliation in affiliations:
        if not affiliation:
            continue

        affiliation_lower = affiliation.lower()

        for org, score in prefs.items():
            if org in affiliation_lower:
                max_score = max(max_score, score)

    return max_score

def extract_affiliations_from_authors(authors):
    """
    Extract affiliations from author objects if available.
    arXiv API doesn't always provide affiliations, but we'll try to extract them.

    Args:
        authors: List of author objects from arXiv

    Returns:
        List of affiliation strings
    """
    affiliations = []

    for author in authors:
        if hasattr(author, 'affiliation') and author.affiliation:
            affiliations.append(author.affiliation)

    return affiliations if affiliations else None

def rank_papers(papers):
    """
    Sort papers by rank score (highest first), then by published date.
    Uses user_rank_override if available.

    Args:
        papers: List of Paper objects

    Returns:
        List of sorted Paper objects
    """
    def get_sort_key(paper):
        # Use manual override if present, otherwise use calculated rank
        rank = paper.user_rank_override if paper.user_rank_override is not None else paper.rank_score
        return (rank, paper.published_date)

    return sorted(papers, key=get_sort_key, reverse=True)

def recalculate_paper_ranks():
    """
    Recalculate rank scores for all papers based on current user preferences.
    Called after preference updates.
    """
    from app.database import get_session, Paper
    import json

    session = get_session()
    papers = session.query(Paper).all()

    for paper in papers:
        authors_list = json.loads(paper.authors)
        new_rank = calculate_rank_score(authors_list, paper.affiliations, use_user_prefs=True)
        paper.rank_score = new_rank

    session.commit()
    session.close()
