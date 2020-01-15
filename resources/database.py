import sys, os
sys.path.append("..")
import sqlite3
from sqlite3 import Error
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'database','database.db')

def create_session():
    """
    Creates a new entry in the sessions table
    """
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect(DB_PATH)
        query = '''
            INSERT INTO sessions (last_updated_date)
            VALUES (datetime('now')) '''

        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return cursor.lastrowid

    except Exception as e:
        print(e)
        raise e

    finally:
        if conn:
            conn.close()

def get_sessions_cards(session_id):
    """
    Return the card_id's of all cards associated with the current session
    """
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect(DB_PATH)
        query = '''
            SELECT card_id
            FROM card
            WHERE session_id = ?
        '''
        cursor = conn.cursor()
        cursor.execute(query, session_id)
        rows = cursor.fetchall()
        return rows

    except Exception as e:
        print(e)
        raise e

    finally:
        if conn:
            conn.close()

def create_card(data):
    """
    Creates a new card in the database
    """
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect(DB_PATH)
        query = '''
            INSERT INTO card (session_id, type, name, hp, mana, pwr, card_text, lvl_up_text, tribe, region)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        return cursor.lastrowid

    except Exception as e:
        print(e)
        raise e

    finally:
        if conn:
            conn.close()

def get_card(session_id, card_id):
    """
    Retrieve all card data for a specific
    """
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect(DB_PATH)
        query = '''
            SELECT *
            FROM card
            WHERE session_id = ? and card_id = ?
        '''
        cursor = conn.cursor()
        cursor.execute(query, (session_id, card_id,))
        rows = cursor.fetchall()
        return rows

    except Exception as e:
        print(e)
        raise e

    finally:
        if conn:
            conn.close()
