import psycopg2
import config

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def setup_database():
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            create_table_query = """
                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(100) NOT NULL,
                    phone VARCHAR(20) NOT NULL UNIQUE
                )
            """
            cur.execute(create_table_query)
            conn.commit()
            cur.close()
            print("Database setup complete. Table 'contacts' is ready.")
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()