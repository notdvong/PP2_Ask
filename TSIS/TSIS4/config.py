WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
GRAY = (100, 100, 100)

DB_CONFIG = {
    "dbname": "snake_db",
    "user": "postgres",
    "password": "postgres", 
    "host": "localhost",
    "port": "5432"
}


DEFAULT_SETTINGS = {
    "snake_color": [0, 255, 0],
    "grid_overlay": False,
    "sound": True
}