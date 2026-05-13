# DevLog API

A REST API for logging and analyzing developer work sessions. Built with Flask and SQLite — tracks projects, focus time, energy levels, and surfaces patterns like coding streaks and peak productivity hours.

This isn't a tutorial project. It's a tool I actually use to log every session in this portfolio.

---

## Tech Stack

- **Python 3.13** + **Flask** — routing and request handling
- **SQLite** — lightweight database, zero config
- **PyCharm HTTP Client** — request testing and session logging

---

## Project Structure

```
devlog-api/
├── app.py          # routes and request/response handling
├── database.py     # all SQLite logic, CRUD functions
├── stats.py        # aggregation queries (summary, streak, peak hours)
├── log.http        # live session log — real entries from every coding session
└── requirements.txt
```

---

## Endpoints

### Sessions

| Method | Route | Description |
|--------|-------|-------------|
| `POST` | `/sessions` | Log a new coding session |
| `GET` | `/sessions` | Get all sessions (filterable) |
| `GET` | `/sessions/<id>` | Get a single session |
| `PUT` | `/sessions/<id>` | Update a session |
| `DELETE` | `/sessions/<id>` | Delete a session |

### Stats

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/stats/summary` | Weekly totals, avg energy, top project |
| `GET` | `/stats/streak` | Current consecutive day coding streak |
| `GET` | `/stats/peak-hours` | Best hours of day by average energy |

---

## Getting Started

```bash
git clone https://github.com/edub966/devlog-api
cd devlog-api
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
python app.py
```

API runs at `http://127.0.0.1:5000`

---

## Example Requests

**Log a session:**
```http
POST /sessions
Content-Type: application/json

{
  "project": "devlog-api",
  "session_type": "focus",
  "duration_mins": 120,
  "energy_level": 4,
  "mood": "flow",
  "shipped": "built stats endpoints",
  "notes": "streak logic was the trickiest part"
}
```

**Filter sessions by project:**
```http
GET /sessions?project=devlog-api
```

**Filter by session type:**
```http
GET /sessions?session_type=focus
```

**Get weekly summary:**
```http
GET /stats/summary
```
```json
{
  "avg_energy": 4.2,
  "period": "last 7 days",
  "session_count": 8,
  "top_project": { "project": "devlog-api", "total_mins": 420 },
  "top_session_type": { "count": 6, "session_type": "focus" },
  "total_mins": 540
}
```

**Get coding streak:**
```http
GET /stats/streak
```
```json
{
  "last_session": "2026-05-13",
  "streak_days": 3
}
```

**Get peak hours:**
```http
GET /stats/peak-hours
```
```json
{
  "peak_hours": [
    { "avg_energy": 4.8, "hour": "10 PM", "session_count": 5 },
    { "avg_energy": 4.2, "hour": "9 PM", "session_count": 7 }
  ]
}
```

---

## Session Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `project` | string | yes | project name |
| `session_type` | string | yes | `focus` / `debug` / `review` / `learning` / `planning` |
| `duration_mins` | integer | yes | how long you actually coded |
| `energy_level` | integer | yes | 1–5 scale |
| `mood` | string | yes | `flow` / `grinding` / `stuck` / `exploratory` |
| `shipped` | string | yes | one-line description of what you got done |
| `notes` | string | no | optional free text |

---

## Design Decisions

**Why separate `stats.py`?** Aggregation logic is fundamentally different from CRUD — it reads across multiple rows to surface patterns rather than operating on individual records. Keeping it separate makes both files easier to extend.

**Why store `created_at` server-side?** The API sets the timestamp at insert time rather than accepting it from the client. This prevents backdating and keeps the streak and peak-hours logic trustworthy.

**Why parameterized queries everywhere?** All SQL uses `?` placeholders instead of string formatting — standard SQL injection prevention.

---

## Part of a larger roadmap

This API is project #19 of 26 in a summer portfolio build spanning data science, embedded systems, and full stack development. The session data logged here feeds into later projects — including an end-to-end ML pipeline (#8) that will use this data as a training set.