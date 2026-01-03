from sqlalchemy import create_engine, Column, String, Integer, Text, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.config import DATABASE_PATH

Base = declarative_base()

class Paper(Base):
    __tablename__ = 'papers'

    id = Column(String, primary_key=True)  # arXiv ID
    title = Column(String, nullable=False)
    authors = Column(Text, nullable=False)  # JSON string of authors
    affiliations = Column(Text)  # JSON string of affiliations
    abstract = Column(Text, nullable=False)
    summary = Column(Text)
    published_date = Column(DateTime, nullable=False)
    fetched_date = Column(DateTime, default=datetime.utcnow)
    arxiv_url = Column(String)
    pdf_url = Column(String)
    rank_score = Column(Float, default=0.0)  # Ranking score based on affiliations
    summary_rating = Column(Integer)  # User rating of summary (1-5 stars)
    user_rank_override = Column(Float)  # Optional manual rank override

    def __repr__(self):
        return f"<Paper(id='{self.id}', title='{self.title[:50]}...')>"

class AffiliationPreference(Base):
    __tablename__ = 'affiliation_preferences'

    id = Column(Integer, primary_key=True, autoincrement=True)
    affiliation_name = Column(String, nullable=False, unique=True)
    rank_score = Column(Float, nullable=False)
    is_custom = Column(Boolean, default=True)  # User-added vs. default
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<AffiliationPreference(name='{self.affiliation_name}', score={self.rank_score})>"

class UserFeedback(Base):
    __tablename__ = 'user_feedback'

    id = Column(Integer, primary_key=True, autoincrement=True)
    paper_id = Column(String, nullable=False)
    feedback_type = Column(String, nullable=False)  # 'summary_rating', 'rank_adjustment'
    feedback_value = Column(Text, nullable=False)  # JSON data
    created_date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<UserFeedback(paper_id='{self.paper_id}', type='{self.feedback_type}')>"

class FavoritePaper(Base):
    __tablename__ = 'favorite_papers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    paper_id = Column(String, nullable=False, unique=True)  # arXiv ID
    personal_rank = Column(Float, default=5.0)  # User's personal ranking (0-10)
    notes = Column(Text)  # Personal notes about the paper
    tags = Column(Text)  # JSON list of custom tags
    favorited_date = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<FavoritePaper(paper_id='{self.paper_id}', rank={self.personal_rank})>"

class PaperHighlight(Base):
    __tablename__ = 'paper_highlights'

    id = Column(Integer, primary_key=True, autoincrement=True)
    paper_id = Column(String, nullable=False)  # arXiv ID
    highlight_text = Column(Text, nullable=False)  # The highlighted text content
    page_number = Column(Integer, nullable=False)  # PDF page number
    position_data = Column(Text)  # JSON with coordinates and selection data
    color = Column(String, default='yellow')  # Highlight color
    note = Column(Text)  # Optional user note for this highlight
    created_date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PaperHighlight(paper_id='{self.paper_id}', page={self.page_number})>"

engine = create_engine(f'sqlite:///{DATABASE_PATH}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()
