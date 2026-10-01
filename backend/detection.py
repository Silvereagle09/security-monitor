from db import get_connection

def alert_exists(ip_address, alert_type):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM alerts
        WHERE ip_address = %s
        AND alert_type = %s
    """, (ip_address, alert_type))

    exists = cursor.fetchone()[0] > 0

    cursor.close()
    conn.close()

    return exists

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

    check_query = """
    SELECT COUNT(*)
    FROM alerts
    WHERE ip_address = %s
    AND alert_type = 'BRUTE_FORCE'
    """

    cursor.execute(check_query, (ip_address,))
    existing_alerts = cursor.fetchone()[0]

    print(f"IP: {ip_address}")
    print(f"Failed Count: {count}")
    print(f"Existing Alerts: {existing_alerts}")


    if count >= 5 and existing_alerts == 0:
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
    
def check_password_spraying(ip_address):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT username)
        FROM events
        WHERE ip_address = %s
        AND event_type = 'LOGIN_FAILED'
    """, (ip_address,))

    user_count = cursor.fetchone()[0]

    if user_count >= 3 and not alert_exists(ip_address, "PASSWORD_SPRAYING"):

        cursor.execute("""
            INSERT INTO alerts
            (ip_address, alert_type, severity)
            VALUES (%s, %s, %s)
        """, (
            ip_address,
            "PASSWORD_SPRAYING",
            "HIGH"
        ))

        conn.commit()

    cursor.close()
    conn.close()
    
def check_suspicious_ip_activity(ip_address):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT event_type)
        FROM events
        WHERE ip_address = %s
    """, (ip_address,))

    event_count = cursor.fetchone()[0]

    if (
        event_count >= 4
        and not alert_exists(
            ip_address,
            "SUSPICIOUS_IP_ACTIVITY"
        )
    ):

        cursor.execute("""
            INSERT INTO alerts
            (ip_address, alert_type, severity)
            VALUES (%s, %s, %s)
        """, (
            ip_address,
            "SUSPICIOUS_IP_ACTIVITY",
            "HIGH"
        ))

        conn.commit()

    cursor.close()
    conn.close()
    
    
def check_port_scan(ip_address):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT port)
        FROM events
        WHERE ip_address = %s
        AND event_type = 'PORT_ACCESS'
        AND port IS NOT NULL
    """, (ip_address,))

    port_count = cursor.fetchone()[0]

    print(f"IP: {ip_address}")
    print(f"Different Ports: {port_count}")

    if port_count >= 5 and not alert_exists(ip_address, "PORT_SCAN"):

        print("PORT SCAN DETECTED")

        cursor.execute("""
            INSERT INTO alerts
            (ip_address, alert_type, severity, description)
            VALUES (%s, %s, %s, %s)
        """, (
            ip_address,
            "PORT_SCAN",
            "HIGH",
            f"Detected access to {port_count} different ports from {ip_address}"
        ))

        conn.commit()

        print("PORT SCAN ALERT INSERTED")

    cursor.close()
    conn.close()


def run_all_detections(ip_address, username, event_type):
    check_brute_force(ip_address)
    check_password_spraying(ip_address)
    check_suspicious_ip_activity(ip_address)
    check_port_scan(ip_address)
    check_suspicious_login(ip_address, username, event_type)
    
def check_suspicious_login(ip_address, username, event_type):
    if event_type != "LOGIN_SUCCESS":
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM events
        WHERE username = %s
        AND ip_address = %s
        AND event_type = 'LOGIN_SUCCESS'
    """, (username, ip_address))

    login_count = cursor.fetchone()[0]

    print(f"User: {username}")
    print(f"IP: {ip_address}")
    print(f"Login Count: {login_count}")

    # Current login is already included in the count.
    # Therefore, count == 1 means this is the first login
    # from this IP for this user.
    if login_count == 1:

        print("SUSPICIOUS LOGIN DETECTED")

        if not alert_exists(ip_address, "SUSPICIOUS_LOGIN"):

            cursor.execute("""
                INSERT INTO alerts
                (ip_address, username, alert_type, severity, description)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                ip_address,
                username,
                "SUSPICIOUS_LOGIN",
                "HIGH",
                f"User {username} logged in successfully from a new IP address {ip_address}"
            ))

            conn.commit()

            print("SUSPICIOUS LOGIN ALERT INSERTED")

    cursor.close()
    conn.close()