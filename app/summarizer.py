import anthropic
from app.config import ANTHROPIC_API_KEY
from app.database import get_session, Paper

SUMMARY_TYPES = {
    'general': {
        'name': 'General Overview',
        'prompt': """Provide a concise summary of this paper focusing on:
1. The main research question or problem
2. Key methodology or approach
3. Main findings or contributions
4. Relevance to AI alignment and safety

Provide a clear, accessible summary in 3-4 paragraphs suitable for researchers and practitioners."""
    },
    'technical': {
        'name': 'Technical Details',
        'prompt': """Provide a detailed technical summary focusing on:
1. Specific algorithms, architectures, or methods used
2. Implementation details and hyperparameters
3. Technical challenges and how they were addressed
4. Experimental setup and evaluation metrics

Include technical depth suitable for researchers implementing similar work."""
    },
    'mathematical': {
        'name': 'Mathematical Analysis',
        'prompt': """Provide a mathematical summary focusing on:
1. Key mathematical formulations and equations
2. Theoretical foundations and proofs
3. Mathematical properties and guarantees
4. Formal analysis and complexity

Emphasize mathematical rigor and formal aspects."""
    },
    'takeaway': {
        'name': 'Key Takeaways',
        'prompt': """Provide a concise summary focusing on:
1. The single most important contribution
2. What makes this work significant
3. Practical implications for AI alignment
4. What readers should remember

Be brief and action-oriented, suitable for quick scanning."""
    },
    'novelty': {
        'name': 'Novel Contributions',
        'prompt': """Analyze what's new in this paper focusing on:
1. How it differs from prior work
2. Novel techniques or approaches introduced
3. Unique insights or perspectives
4. Advances over the state-of-the-art

Emphasize what makes this work original and innovative."""
    },
    'practical': {
        'name': 'Practical Implications',
        'prompt': """Summarize the practical aspects focusing on:
1. Real-world applications and use cases
2. Implementation considerations
3. Limitations and practical constraints
4. How this can be applied in practice

Focus on actionable insights for practitioners."""
    }
}

def generate_summary(title, abstract, authors_list, summary_type='general', use_learning=True):
    """
    Generate a summary of a paper using Claude API.
    Optionally incorporates user feedback to improve summaries.

    Args:
        title: Paper title
        abstract: Paper abstract
        authors_list: List of author names
        summary_type: Type of summary to generate (general, technical, mathematical, etc.)
        use_learning: Whether to use learned preferences from user feedback

    Returns:
        str: Generated summary
    """
    if not ANTHROPIC_API_KEY:
        return "Summary generation unavailable: No API key configured."

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # Get summary type prompt
    type_config = SUMMARY_TYPES.get(summary_type, SUMMARY_TYPES['general'])

    # Base prompt
    prompt = f"""Please provide a summary of this AI alignment research paper.

{type_config['prompt']}

Paper Title: {title}

Authors: {', '.join(authors_list)}

Abstract: {abstract}"""

    # Add learned preferences if enabled
    if use_learning:
        try:
            from app.learning import generate_summary_prompt_enhancements
            enhancements = generate_summary_prompt_enhancements()
            if enhancements:
                prompt += f"\n\n{enhancements}"
        except Exception as e:
            print(f"Could not apply learning enhancements: {e}")

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    except Exception as e:
        print(f"Error generating summary: {e}")
        return f"Error generating summary: {str(e)}"

def summarize_papers(paper_ids=None, limit=10):
    """
    Generate summaries for papers that don't have them yet.

    Args:
        paper_ids: Optional list of specific paper IDs to summarize
        limit: Maximum number of papers to summarize (if paper_ids not provided)

    Returns:
        int: Number of papers summarized
    """
    session = get_session()

    if paper_ids:
        papers = session.query(Paper).filter(Paper.id.in_(paper_ids)).all()
    else:
        # Get papers without summaries, prioritize by rank
        papers = session.query(Paper).filter(Paper.summary.is_(None)).order_by(Paper.rank_score.desc()).limit(limit).all()

    summarized_count = 0

    for paper in papers:
        if paper.summary:
            continue

        print(f"Generating summary for: {paper.title[:60]}...")

        import json
        authors_list = json.loads(paper.authors)

        summary = generate_summary(paper.title, paper.abstract, authors_list)

        paper.summary = summary
        summarized_count += 1

        print(f"  Summary generated ({len(summary)} chars)")

    session.commit()
    session.close()

    print(f"Generated {summarized_count} summaries.")
    return summarized_count
