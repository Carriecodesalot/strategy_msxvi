import psycopg2
import random
import time
from datetime import datetime

# Database connection details
DB_NAME = "telemetry_db"
DB_USER = "your_user"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"

# Connect to PostgreSQL
def connect_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

# Create table if it doesn’t exist
def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS telemetry (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            can_id INT,
            signal_name TEXT,
            value FLOAT
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Generate sample data
def generate_data():
    can_ids = [100, 200, 300, 400]
    signals = ["speed", "rpm", "temperature", "voltage"]
    
    return {
        "timestamp": datetime.utcnow(),
        "can_id": random.choice(can_ids),
        "signal_name": random.choice(signals),
        "value": round(random.uniform(0, 100), 2)
    }

# Upload data to PostgreSQL
def upload_data():
    conn = connect_db()
    cur = conn.cursor()
    
    for _ in range(10):  # Upload 10 samples
        data = generate_data()
        cur.execute(
            "INSERT INTO telemetry (timestamp, can_id, signal_name, value) VALUES (%s, %s, %s, %s)",
            (data["timestamp"], data["can_id"], data["signal_name"], data["value"])
        )
        conn.commit()
        print(f"Uploaded: {data}")
        time.sleep(3)  # Simulating a 3-second interval
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_table()
    upload_data()

