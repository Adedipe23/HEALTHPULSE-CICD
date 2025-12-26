from backend.app import app

def test_health_endpoint():
    client = app.test_client()
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"

def test_check_ok_case():
    client = app.test_client()
    payload = {
        "heartRate": 72,
        "systolic": 118,
        "diastolic": 76,
        "temperatureC": 36.8,
        "spo2": 98
    }
    r = client.post("/api/v1/check", json=payload)
    assert r.status_code == 200
    data = r.get_json()
    assert data["overallStatus"] == "OK"

def test_check_critical_case():
    client = app.test_client()
    payload = {
        "heartRate": 140,
        "systolic": 190,
        "diastolic": 130,
        "temperatureC": 40.0,
        "spo2": 85
    }
    r = client.post("/api/v1/check", json=payload)
    assert r.status_code == 200
    data = r.get_json()
    assert data["overallStatus"] == "CRITICAL"
