from flask import Blueprint, render_template, jsonify, request
from app.database import get_session, Paper, AffiliationPreference, UserFeedback
from app.fetcher import fetch_recent_papers
from app.summarizer import summarize_papers
from app.ranker import rank_papers, recalculate_paper_ranks, get_user_preferences
from app.learning import get_learning_report
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Main page showing ranked papers."""
    session = get_session()

    # Get filter parameters
    min_rank = request.args.get('min_rank', 0, type=float)
    days_back = request.args.get('days', 30, type=int)

    # Query papers
    query = session.query(Paper)

    if min_rank > 0:
        query = query.filter(Paper.rank_score >= min_rank)

    papers = query.all()

    # Rank papers
    ranked_papers = rank_papers(papers)

    # Prepare paper data for template
    papers_data = []
    for paper in ranked_papers:
        authors_list = json.loads(paper.authors)
        affiliations_list = json.loads(paper.affiliations) if paper.affiliations else []

        papers_data.append({
            'id': paper.id,
            'title': paper.title,
            'authors': authors_list,
            'affiliations': affiliations_list,
            'abstract': paper.abstract,
            'summary': paper.summary,
            'published_date': paper.published_date,
            'arxiv_url': paper.arxiv_url,
            'pdf_url': paper.pdf_url,
            'rank_score': paper.rank_score,
            'user_rank_override': paper.user_rank_override,
            'summary_rating': paper.summary_rating
        })

    session.close()

    return render_template('index.html', papers=papers_data, min_rank=min_rank)

@main.route('/api/fetch', methods=['POST'])
def fetch_papers():
    """API endpoint to fetch new papers."""
    days_back = request.json.get('days_back', 7)
    max_results = request.json.get('max_results', 100)

    new_papers = fetch_recent_papers(days_back=days_back, max_results=max_results)

    return jsonify({
        'success': True,
        'new_papers': new_papers,
        'message': f'Fetched {new_papers} new papers'
    })

@main.route('/api/summarize', methods=['POST'])
def generate_summaries():
    """API endpoint to generate summaries for papers."""
    paper_ids = request.json.get('paper_ids', None)
    limit = request.json.get('limit', 10)

    summarized = summarize_papers(paper_ids=paper_ids, limit=limit)

    return jsonify({
        'success': True,
        'summarized': summarized,
        'message': f'Generated {summarized} summaries'
    })

@main.route('/api/stats')
def get_stats():
    """Get statistics about papers in database."""
    session = get_session()

    total_papers = session.query(Paper).count()
    papers_with_summaries = session.query(Paper).filter(Paper.summary.isnot(None)).count()
    high_rank_papers = session.query(Paper).filter(Paper.rank_score >= 7).count()

    session.close()

    return jsonify({
        'total_papers': total_papers,
        'papers_with_summaries': papers_with_summaries,
        'papers_without_summaries': total_papers - papers_with_summaries,
        'high_rank_papers': high_rank_papers
    })

@main.route('/preferences')
def preferences_page():
    """Preferences management page."""
    return render_template('preferences.html')

@main.route('/api/preferences', methods=['GET'])
def get_preferences():
    """Get all affiliation preferences."""
    prefs = get_user_preferences()
    session = get_session()

    # Get custom preferences with metadata
    custom_prefs = session.query(AffiliationPreference).all()
    session.close()

    result = []
    for name, score in prefs.items():
        # Check if it's a custom preference
        is_custom = any(p.affiliation_name.lower() == name for p in custom_prefs)
        result.append({
            'name': name,
            'score': score,
            'is_custom': is_custom
        })

    # Sort by score descending
    result.sort(key=lambda x: x['score'], reverse=True)

    return jsonify({'preferences': result})

@main.route('/api/preferences', methods=['POST'])
def add_or_update_preference():
    """Add or update an affiliation preference."""
    data = request.json
    affiliation_name = data.get('affiliation_name', '').strip()
    rank_score = data.get('rank_score', 5.0)

    if not affiliation_name:
        return jsonify({'success': False, 'message': 'Affiliation name is required'}), 400

    session = get_session()

    # Check if preference exists
    pref = session.query(AffiliationPreference).filter_by(
        affiliation_name=affiliation_name.lower()
    ).first()

    if pref:
        # Update existing
        pref.rank_score = rank_score
        message = f'Updated {affiliation_name} to score {rank_score}'
    else:
        # Create new
        pref = AffiliationPreference(
            affiliation_name=affiliation_name.lower(),
            rank_score=rank_score,
            is_custom=True
        )
        session.add(pref)
        message = f'Added {affiliation_name} with score {rank_score}'

    session.commit()
    session.close()

    # Recalculate all paper ranks
    recalculate_paper_ranks()

    return jsonify({'success': True, 'message': message})

@main.route('/api/preferences/<string:affiliation_name>', methods=['DELETE'])
def delete_preference(affiliation_name):
    """Delete a custom affiliation preference."""
    session = get_session()

    pref = session.query(AffiliationPreference).filter_by(
        affiliation_name=affiliation_name.lower()
    ).first()

    if not pref:
        session.close()
        return jsonify({'success': False, 'message': 'Preference not found'}), 404

    session.delete(pref)
    session.commit()
    session.close()

    # Recalculate all paper ranks
    recalculate_paper_ranks()

    return jsonify({'success': True, 'message': f'Deleted {affiliation_name}'})

@main.route('/api/paper/<string:paper_id>/rate-summary', methods=['POST'])
def rate_summary(paper_id):
    """Rate a paper's summary."""
    data = request.json
    rating = data.get('rating', 0)

    if rating < 1 or rating > 5:
        return jsonify({'success': False, 'message': 'Rating must be between 1 and 5'}), 400

    session = get_session()

    paper = session.query(Paper).filter_by(id=paper_id).first()
    if not paper:
        session.close()
        return jsonify({'success': False, 'message': 'Paper not found'}), 404

    paper.summary_rating = rating

    # Log feedback
    feedback = UserFeedback(
        paper_id=paper_id,
        feedback_type='summary_rating',
        feedback_value=json.dumps({'rating': rating})
    )
    session.add(feedback)

    session.commit()
    session.close()

    return jsonify({'success': True, 'message': f'Rated summary {rating} stars'})

@main.route('/api/paper/<string:paper_id>/rank', methods=['POST'])
def set_paper_rank(paper_id):
    """Set a manual rank override for a paper."""
    data = request.json
    rank = data.get('rank', None)

    session = get_session()

    paper = session.query(Paper).filter_by(id=paper_id).first()
    if not paper:
        session.close()
        return jsonify({'success': False, 'message': 'Paper not found'}), 404

    if rank is None:
        # Clear override
        paper.user_rank_override = None
        message = 'Cleared manual rank override'
    else:
        paper.user_rank_override = float(rank)
        message = f'Set manual rank to {rank}'

    # Log feedback
    feedback = UserFeedback(
        paper_id=paper_id,
        feedback_type='rank_adjustment',
        feedback_value=json.dumps({'old_rank': paper.rank_score, 'new_rank': rank})
    )
    session.add(feedback)

    session.commit()
    session.close()

    return jsonify({'success': True, 'message': message})

@main.route('/api/learning-report')
def learning_report():
    """Get a report of what the system has learned from user feedback."""
    try:
        report = get_learning_report()
        return jsonify({'success': True, 'report': report})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
