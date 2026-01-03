import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
CHECK_INTERVAL_HOURS = int(os.getenv('CHECK_INTERVAL_HOURS', 24))
DATABASE_PATH = 'papers.db'

# High-impact organizations and research groups for ranking
PROMINENT_AFFILIATIONS = {
    'openai': 10,
    'anthropic': 10,
    'google': 9,
    'deepmind': 9,
    'google deepmind': 9,
    'meta': 8,
    'meta ai': 8,
    'microsoft': 8,
    'microsoft research': 8,
    'stanford': 7,
    'mit': 7,
    'berkeley': 7,
    'uc berkeley': 7,
    'oxford': 7,
    'cambridge': 7,
    'carnegie mellon': 7,
    'cmu': 7,
    'eth zurich': 6,
    'toronto': 6,
    'montreal': 6,
    'mila': 6,
    'redwood research': 8,
    'alignment research center': 8,
    'arc': 7,
    'chai': 7,
    'machine intelligence research institute': 7,
    'miri': 7,
}

# Keywords to identify AI alignment papers
ALIGNMENT_KEYWORDS = [
    'alignment',
    'ai safety',
    'value alignment',
    'reward modeling',
    'rlhf',
    'constitutional ai',
    'ai ethics',
    'interpretability',
    'mechanistic interpretability',
    'adversarial robustness',
    'ai governance',
    'existential risk',
    'x-risk',
    'beneficial ai',
    'corrigibility',
    'scalable oversight',
    'truthfulness',
    'honesty',
    'deception',
    'inner alignment',
    'outer alignment',
    'mesa optimization',
]
