import sqlite3
import logging
from typing import Optional

def init_db(db_path: str = 'gamingai.db') -> None:
    """Initialize the database with required tables."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_input_text (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text_type TEXT,
            text TEXT,
            UNIQUE(text_type)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            key_name TEXT PRIMARY KEY,
            key_value TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            question_session_id TEXT,
            asked_on DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def reset_db(db_path: str = 'gamingai.db') -> None:
    """Reset the database by dropping all tables."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Drop existing tables
    cursor.execute("DROP TABLE IF EXISTS system_input_text")
    cursor.execute("DROP TABLE IF EXISTS api_keys")
    cursor.execute("DROP TABLE IF EXISTS user_questions")
    
    conn.commit()
    conn.close()

def main(reset: bool = False, db_path: Optional[str] = None) -> None:
    """
    Main function to populate the database.
    
    Args:
        reset (bool): If True, reset the database before initialization
        db_path (str, optional): Path to the database file
    """
    if db_path is None:
        db_path = 'gamingai.db'
    
    try:
        if reset:
            logging.info("Resetting database...")
            reset_db(db_path)
        
        logging.info("Initializing database...")
        init_db(db_path)
        
        logging.info("Database population completed successfully.")
    except Exception as e:
        logging.error(f"Error during database population: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
