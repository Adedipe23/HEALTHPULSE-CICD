from flask import Flask, request, jsonify
from datetime import datetime, timezone
from collections import deque

app = Flask(__name__)

# Keep last 20 checks in memory (good enough for a CI/CD demo)
HISTORY = deque(maxlen=20)


def classify_vitals(hr, sys_bp, dia_bp, temp_c, spo2):
    """
    Returns:
      overall: "OK" | "WARN" | "CRITICAL"
      notes: list[str]
    """
    notes = []
    severity = 0  # 0=OK, 1=WARN, 2=CRITICAL

    # Heart rate (bpm)
    if hr < 50:
        notes.append("Low heart rate (possible bradycardia).")
        severity = max(severity, 1)
    elif hr > 120:
        notes.append("Very high heart rate (possible tachycardia).")
        severity = max(severity, 2)
    elif hr > 100:
        notes.append("Elevated heart rate.")
        severity = max(severity, 1)

    # Blood pressure (mmHg) - simplified thresholds for demo
    if sys_bp >= 180 or dia_bp >= 120:
        notes.append("Hypertensive crisis range blood pressure.")
        severity = max(severity, 2)
    elif sys_bp >= 130 or dia_bp >= 80:
        notes.append("Elevated blood pressure.")
        severity = max(severity, 1)
    elif sys_bp < 90 or dia_bp < 60:
        notes.append("Low blood pressure.")
        severity = max(severity, 1)

    # Temperature (°C)
    if temp_c < 35.0:
        notes.append("Low temperature (possible hypothermia).")
        severity = max(severity, 2)
    elif temp_c >= 39.5:
        notes.append("High fever.")
        severity = max(severity, 2)
    elif temp_c >= 38.0:
        notes.append("Fever.")
        severity = max(severity, 1)

    # SpO2 (%)
    if spo2 < 90:
        notes.append("Critically low oxygen saturation.")
        severity = max(severity, 2)
    elif spo2 < 95:
        notes.append("Low oxygen saturation.")
        severity = max(severity, 1)

    overall = "OK" if severity == 0 else ("WARN" if severity == 1 else "CRITICAL")
    if not notes:
        notes.append("All vitals within normal demo ranges.")

    return overall, notes


def parse_number(data, key):
    if key not in data:
        raise ValueError(f"Missing field: {key}")
    try:
        return float(data[key])
    except (TypeError, ValueError):
        raise ValueError(f"Invalid number for field: {key}")


@app.get("/api/v1/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/v1/history")
def history():
    return jsonify({"items": list(HISTORY)})


@app.post("/api/v1/check")
def check():
    data = request.get_json(silent=True) or {}
    try:
        hr = parse_number(data, "heartRate")
        sys_bp = parse_number(data, "systolic")
        dia_bp = parse_number(data, "diastolic")
        temp_c = parse_number(data, "temperatureC")
        spo2 = parse_number(data, "spo2")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    overall, notes = classify_vitals(hr, sys_bp, dia_bp, temp_c, spo2)

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input": {
            "heartRate": hr,
            "systolic": sys_bp,
            "diastolic": dia_bp,
            "temperatureC": temp_c,
            "spo2": spo2,
        },
        "overallStatus": overall,
        "notes": notes,
    }

    HISTORY.appendleft(result)
    return jsonify(result)


if __name__ == "__main__":
    # For local debugging outside Docker
    app.run(host="0.0.0.0", port=5000, debug=True)
