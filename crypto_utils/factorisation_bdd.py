import sqlite3
import os
import json
import time

def initialize_local_db():
    """Initialise la base de données locale de factorisation"""
    db_file = os.path.join(os.path.dirname(__file__), 'factorization_cache.db')
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Création de la table si elle n'existe pas
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS factorizations (
                                                                 number TEXT PRIMARY KEY,
                                                                 factors TEXT,
                                                                 method TEXT,
                                                                 timestamp REAL
                   )
                   ''')

    conn.commit()
    conn.close()
    return db_file

def check_local_db(number):
    """Vérifie si le nombre est déjà factorisé dans la base locale"""
    db_file = os.path.join(os.path.dirname(__file__), 'factorization_cache.db')
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT factors, method, timestamp FROM factorizations WHERE number = ?", (str(number),))
    result = cursor.fetchone()
    conn.close()

    if result:
        factors_json, method, timestamp = result
        return {
            'success': True,
            'number': number,
            'factors': json.loads(factors_json),
            'source': f'Cache local ({method})',
            'cached': True,
            'original_timestamp': timestamp
        }
    return None

def save_to_local_db(result):
    """Sauvegarde le résultat de factorisation dans la base locale"""
    if not result.get('success') or 'factors' not in result:
        return

    db_file = os.path.join(os.path.dirname(__file__), 'factorization_cache.db')
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    factors_json = json.dumps(result['factors'])
    method = result.get('source', 'unknown')

    cursor.execute(
        "INSERT OR REPLACE INTO factorizations (number, factors, method, timestamp) VALUES (?, ?, ?, ?)",
        (str(result['number']), factors_json, method, time.time())
    )

    conn.commit()
    conn.close()