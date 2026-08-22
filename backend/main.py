print("MAIN.PY LOADED")
from fastapi import FastAPI
from db import get_connection
from models import SecurityEvent
from detection import check_brute_force

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Security Monitor API Running"}

@app.get("/test-db")
def test_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT DATABASE();")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return {
            "status": "success",
            "database": result[0]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
        
@app.post("/events")
def create_event(event: SecurityEvent):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO events
    (timestamp, event_type, username, ip_address)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        event.timestamp,
        event.event_type,
        event.username,
        event.ip_address
    )

    cursor.execute(query, values)
    conn.commit()
    print("Calling detection...")
    check_brute_force(event.ip_address)

    cursor.close()
    conn.close()

    return {
        "message": "Event stored successfully"
    }
    
@app.get("/alerts")
def get_alerts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM alerts
        ORDER BY created_at DESC
    """)

    alerts = cursor.fetchall()

    cursor.close()
    conn.close()

    return alerts