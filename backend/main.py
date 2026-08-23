print("MAIN.PY LOADED")
from fastapi import FastAPI
from db import get_connection
from models import SecurityEvent
from detection import check_brute_force
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/events")
def get_events():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM events
        ORDER BY timestamp DESC
    """)

    events = cursor.fetchall()

    cursor.close()
    conn.close()

    return events

@app.get("/stats")
def get_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM events")
    total_events = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts")
    total_alerts = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM alerts
        WHERE severity = 'HIGH'
    """)
    high_alerts = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "total_events": total_events,
        "total_alerts": total_alerts,
        "high_severity_alerts": high_alerts
    }