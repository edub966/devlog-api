from database import get_connection
from datetime import datetime, timezone, timedelta

def get_weekly_summary():
    conn=get_connection()

    seven_days_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()

    rows = conn.execute("""
        SELECT
            COUNT(*) AS session_count,
            SUM(duration_mins) AS total_mins,
            ROUND(AVG(energy_level), 1) AS avg_energy,
            session_type,
            project
        FROM sessions
        WHERE created_at >= ?
    """, (seven_days_ago,)).fetchall()

    top_project_row = conn.execute("""
       SELECT project, SUM(duration_mins) AS total_mins
       FROM sessions
       WHERE created_at >= ?
       GROUP BY project
       ORDER BY total_mins DESC LIMIT 1
       """, (seven_days_ago,)).fetchone()


    # get most common session type this week
    top_type_row = conn.execute("""
        SELECT session_type, COUNT(*) AS count
        FROM sessions
        WHERE created_at >= ?
        GROUP BY session_type
        ORDER BY count DESC
            LIMIT 1
        """, (seven_days_ago,)).fetchone()

    conn.close()

    if not rows or rows[0]["session_count"] == 0:
        return {"message": "No sessions logged in the last 7 days"}

    row = rows[0]
    return {
        "period": "last 7 days",
        "session_count": row["session_count"],
        "total_mins": row["total_mins"] or 0,
        "avg_energy": row["avg_energy"] or 0,
        "top_project": dict(top_project_row) if top_project_row else None,
        "top_session_type": dict(top_type_row) if top_type_row else None
    }

def get_streak():
    conn = get_connection()

    rows = conn.execute("""
        SELECT DISTINCT DATE(created_at) AS day
        FROM sessions
        ORDER BY day DESC
    """).fetchall()

    conn .close()

    if not rows:
        return {"streak_days": 0, "message": "No sessions logged yet"}

    days = [row["day"] for row in rows]  # list of date strings, newest first
    today = datetime.now(timezone.utc).date()
    streak = 0

    for i, day_str in enumerate(days):
        day = datetime.strptime(day_str, "%Y-%m-%d").date()
        expected = today - timedelta(days=i)  # what day we expect at position i

        if day == expected:
            streak += 1  # this day is part of the consecutive chain
        else:
            break  # gap in the chain — streak is over

    return {
        "streak_days": streak,
        "last_session": days[0] if days else None
    }

def get_peak_hours():
    # Returns average energy level grouped by hour of day
    # Shows you when you code best
    conn = get_connection()

    rows = conn.execute("""
        SELECT
            CAST(strftime('%H', created_at) AS INTEGER) AS hour,
            ROUND(AVG(energy_level), 1)                 AS avg_energy,
            COUNT(*)                                    AS session_count
        FROM sessions
        GROUP BY hour
        ORDER BY avg_energy DESC
    """).fetchall()


    conn.close()

    if not rows:
        return {"message": "Not enough data yet"}

    # format hours
    result = []
    for row in rows:
        hour = row["hour"]
        label = f"{hour % 12 or 12} {'AM' if hour < 12 else 'PM'}"  # convert 24hr to 12hr format
        result.append({
            "hour": label,
            "avg_energy": row["avg_energy"],
            "session_count": row["session_count"]
        })

    return {"peak_hours": result}
