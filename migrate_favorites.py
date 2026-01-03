#!/usr/bin/env python3
"""
Database migration script to add favorites table.
Run this after updating the code to add favorites functionality.
"""

import sqlite3
from app.config import DATABASE_PATH

def migrate():
    """Add favorites table to existing database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    print("Starting favorites migration...")

    # Create favorite_papers table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite_papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paper_id VARCHAR NOT NULL UNIQUE,
            personal_rank FLOAT DEFAULT 5.0,
            notes TEXT,
            tags TEXT,
            favorited_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✓ Created favorite_papers table")

    conn.commit()
    conn.close()

    print("\nMigration completed successfully!")
    print("\nYou can now:")
    print("  1. Add papers to favorites from the main page")
    print("  2. View all favorites at /favorites")
    print("  3. Add personal rankings and notes to your favorite papers")

if __name__ == '__main__':
    migrate()
