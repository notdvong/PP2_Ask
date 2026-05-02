import psycopg2
from config import DB_CONFIG

def get_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def init_db():
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

def save_result(username, score, level):
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM players WHERE username = %s;", (username,))
    result = cursor.fetchone()
    
    if result:
        player_id = result[0]
    else:
        cursor.execute("INSERT INTO players (username) VALUES (%s) RETURNING id;", (username,))
        player_id = cursor.fetchone()[0]
        
    cursor.execute("""
        INSERT INTO game_sessions (player_id, score, level_reached) 
        VALUES (%s, %s, %s);
    """, (player_id, score, level))
    
    conn.commit()
    cursor.close()
    conn.close()

def get_top_10():
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.username, g.score, g.level_reached, DATE(g.played_at)
        FROM game_sessions g
        JOIN players p ON g.player_id = p.id
        ORDER BY g.score DESC
        LIMIT 10;
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_personal_best(username):
    conn = get_connection()
    if not conn: return 0
    cursor = conn.cursor()
    cursor.execute("""
        SELECT MAX(g.score) 
        FROM game_sessions g 
        JOIN players p ON g.player_id = p.id 
        WHERE p.username = %s;
    """, (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result and result[0] else 0