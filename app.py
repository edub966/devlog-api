from flask import Flask, request, jsonify
from database import init_db, create_session, get_all_sessions, get_session_by_id, update_session, delete_session
from stats import get_weekly_summary, get_streak, get_peak_hours
app = Flask(__name__)

@app.route("/sessions", methods=["POST"])
def log_session():
    data = request.get_json()

    required = ["project", "session_type", "duration_mins", "energy_level", "mood", "shipped"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing requried field: {field}"}), 400

    new_id = create_session(data)
    return jsonify({"message": "Session logged", "id": new_id}), 201

@app.route("/sessions", methods=["GET"])
def list_sessions():
    filters = {}

    if request.args.get("project"):
        filters["project"] = request.args.get("project")

    if request.args.get("session_type"):
        filters["session_type"] = request.args.get("session_type")

    sessions = get_all_sessions(filters if filters else None)
    return jsonify(sessions), 200

@app.route("/sessions/<int:session_id>", methods=["GET"])
def get_session(session_id):
    session = get_session_by_id(session_id)

    if not session:
        return jsonify({"error": "Session not found"}), 404
    return jsonify(session), 200

@app.route("/sessions/<int:session_id>", methods=["PUT"])
def edit_session(session_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400
    updated = update_session(session_id, data)

    if not updated:
        return jsonify({"error": "Session not found"}), 404
    return jsonify({"message": "Session updated"}), 200

@app.route("/sessions/<int:session_id>", methods=["DELETE"])
def remove_session(session_id):
    deleted = delete_session(session_id)

    if not deleted:
        return jsonify({"error": "Session not found"}), 404

    return jsonify({"message": "Session deleted"}), 200

@app.route("/stats/summary", methods=["GET"])
def weekly_summary():
    return jsonify(get_weekly_summary()), 200


@app.route("/stats/streak", methods=["GET"])
def streak():
    return jsonify(get_streak()), 200


@app.route("/stats/peak-hours", methods=["GET"])
def peak_hours():
    return jsonify(get_peak_hours()), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)