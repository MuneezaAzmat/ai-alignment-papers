#!/usr/bin/env python3
"""
Database migration script to add new columns and tables for user preferences.
Run this after updating the code to add the new features.
"""

import sqlite3
from app.config import DATABASE_PATH

def migrate():
    """Add new columns and tables to existing database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    print("Starting database migration...")

    # Add new columns to papers table if they don't exist
    try:
        cursor.execute("ALTER TABLE papers ADD COLUMN summary_rating INTEGER")
        print("✓ Added summary_rating column")
    except sqlite3.OperationalError:
        print("- summary_rating column already exists")

    try:
        cursor.execute("ALTER TABLE papers ADD COLUMN user_rank_override FLOAT")
        print("✓ Added user_rank_override column")
    except sqlite3.OperationalError:
        print("- user_rank_override column already exists")

    # Create affiliation_preferences table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS affiliation_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            affiliation_name VARCHAR NOT NULL UNIQUE,
            rank_score FLOAT NOT NULL,
            is_custom BOOLEAN DEFAULT 1,
            created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✓ Created affiliation_preferences table")

    # Create user_feedback table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paper_id VARCHAR NOT NULL,
            feedback_type VARCHAR NOT NULL,
            feedback_value TEXT NOT NULL,
            created_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✓ Created user_feedback table")

    conn.commit()
    conn.close()

    print("\nMigration completed successfully!")
    print("\nYou can now:")
    print("  1. Add custom affiliations at /preferences")
    print("  2. Rate summaries with the star rating system")
    print("  3. Set custom ranks for individual papers")
    print("  4. View learning insights on the preferences page")

if __name__ == '__main__':
    migrate()
