"""
Migration script to add paper_highlights table
Run this once to update the database schema
"""

from sqlalchemy import create_engine, text
from app.config import DATABASE_PATH

engine = create_engine(f'sqlite:///{DATABASE_PATH}')

# Create the table if it doesn't exist
with engine.connect() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS paper_highlights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paper_id VARCHAR NOT NULL,
        highlight_text TEXT NOT NULL,
        page_number INTEGER NOT NULL,
        position_data TEXT,
        color VARCHAR DEFAULT 'yellow',
        note TEXT,
        created_date DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """))
    conn.commit()

print("Migration complete: paper_highlights table created")
