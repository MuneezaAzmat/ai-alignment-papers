import json
from app.database import get_session, Paper, UserFeedback
from sqlalchemy import func

def get_feedback_insights():
    """
    Analyze user feedback to extract insights for improving summaries.

    Returns:
        dict: Insights about user preferences
    """
    session = get_session()

    # Get summary ratings
    rated_papers = session.query(Paper).filter(Paper.summary_rating.isnot(None)).all()

    # Get rank adjustments
    rank_feedback = session.query(UserFeedback).filter_by(feedback_type='rank_adjustment').all()

    session.close()

    insights = {
        'summary_ratings': {
            'count': len(rated_papers),
            'average': sum(p.summary_rating for p in rated_papers) / len(rated_papers) if rated_papers else 0,
            'high_rated': [p for p in rated_papers if p.summary_rating >= 4],
            'low_rated': [p for p in rated_papers if p.summary_rating <= 2]
        },
        'rank_adjustments': {
            'count': len(rank_feedback),
            'papers_boosted': [],
            'papers_lowered': []
        }
    }

    # Analyze rank adjustments
    for feedback in rank_feedback:
        try:
            data = json.loads(feedback.feedback_value)
            old_rank = data.get('old_rank', 0)
            new_rank = data.get('new_rank')

            if new_rank is not None and new_rank > old_rank:
                insights['rank_adjustments']['papers_boosted'].append(feedback.paper_id)
            elif new_rank is not None and new_rank < old_rank:
                insights['rank_adjustments']['papers_lowered'].append(feedback.paper_id)
        except:
            continue

    return insights

def generate_summary_prompt_enhancements():
    """
    Generate prompt enhancements based on user feedback.

    Returns:
        str: Additional instructions for the summarization prompt
    """
    insights = get_feedback_insights()

    enhancements = []

    # Analyze high-rated vs low-rated summaries
    if insights['summary_ratings']['high_rated']:
        enhancements.append(
            "Based on user feedback, they prefer summaries that are clear, concise, and directly address "
            "the paper's relevance to AI alignment and safety."
        )

    if insights['summary_ratings']['low_rated']:
        enhancements.append(
            "Avoid being too technical or abstract. Users prefer summaries with practical implications "
            "and real-world relevance to AI safety."
        )

    # Add preferences based on rank adjustments
    if len(insights['rank_adjustments']['papers_boosted']) > 0:
        enhancements.append(
            "The user has shown interest in papers that directly tackle concrete AI safety challenges. "
            "Emphasize practical applications and novel approaches."
        )

    return "\n\n".join(enhancements) if enhancements else ""

def get_personalized_ranking_insights():
    """
    Get insights about user's ranking preferences.

    Returns:
        dict: Information about which affiliations/topics the user values
    """
    session = get_session()

    # Get papers with user rank overrides
    overridden_papers = session.query(Paper).filter(Paper.user_rank_override.isnot(None)).all()

    # Analyze patterns
    boosted_affiliations = []
    lowered_affiliations = []

    for paper in overridden_papers:
        if paper.user_rank_override > paper.rank_score:
            # User boosted this paper
            if paper.affiliations:
                try:
                    affs = json.loads(paper.affiliations)
                    boosted_affiliations.extend(affs)
                except:
                    pass
        elif paper.user_rank_override < paper.rank_score:
            # User lowered this paper
            if paper.affiliations:
                try:
                    affs = json.loads(paper.affiliations)
                    lowered_affiliations.extend(affs)
                except:
                    pass

    session.close()

    return {
        'boosted_affiliations': list(set(boosted_affiliations)),
        'lowered_affiliations': list(set(lowered_affiliations)),
        'total_overrides': len(overridden_papers)
    }

def get_learning_report():
    """
    Generate a comprehensive report about what the system has learned from user feedback.

    Returns:
        dict: Complete learning report
    """
    feedback_insights = get_feedback_insights()
    ranking_insights = get_personalized_ranking_insights()
    prompt_enhancements = generate_summary_prompt_enhancements()

    report = {
        'feedback_summary': {
            'total_ratings': feedback_insights['summary_ratings']['count'],
            'average_rating': round(feedback_insights['summary_ratings']['average'], 2),
            'total_rank_adjustments': feedback_insights['rank_adjustments']['count']
        },
        'ranking_preferences': ranking_insights,
        'summary_preferences': {
            'high_rated_count': len(feedback_insights['summary_ratings']['high_rated']),
            'low_rated_count': len(feedback_insights['summary_ratings']['low_rated']),
            'prompt_enhancements': prompt_enhancements
        }
    }

    return report
