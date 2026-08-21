from db import get_connection

def check_brute_force(ip_address):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT COUNT(*)
    FROM events
    WHERE ip_address = %s
    AND event_type = 'LOGIN_FAILED'
    """

    cursor.execute(query, (ip_address,))
    count = cursor.fetchone()[0]

    print(f"IP: {ip_address}")
    print(f"Failed Count: {count}")

    if count >= 5:
        print("BRUTE FORCE DETECTED")

        alert_query = """
        INSERT INTO alerts
        (ip_address, alert_type, severity, description)
        VALUES (%s, %s, %s, %s)
        """

        values = (
            ip_address,
            "BRUTE_FORCE",
            "HIGH",
            f"Detected {count} failed login attempts from {ip_address}"
        )

        cursor.execute(alert_query, values)
        conn.commit()

        print("ALERT INSERTED")

    cursor.close()
    conn.close()