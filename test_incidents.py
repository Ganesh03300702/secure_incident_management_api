def test_create_incident(client, headers):
    payload = {
        "title": "API outage",
        "description": "Production API is unavailable",
        "priority": "high",
        "reporter": "Ganesh",
    }
    response = client.post("/api/v1/incidents", json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json()["priority"] == "high"

def test_invalid_incident_rejected(client, headers):
    payload = {"title": "x", "description": "bad", "priority": "wrong", "reporter": "A"}
    response = client.post("/api/v1/incidents", json=payload, headers=headers)
    assert response.status_code == 422

def test_get_missing_incident(client, headers):
    response = client.get("/api/v1/incidents/999999", headers=headers)
    assert response.status_code == 404

def test_update_incident(client, headers):
    created = client.post("/api/v1/incidents", json={
        "title": "Database issue",
        "description": "Database response time increased",
        "priority": "medium",
        "reporter": "Tester"
    }, headers=headers)
    incident_id = created.json()["id"]
    response = client.put(
        f"/api/v1/incidents/{incident_id}",
        json={"status": "in_progress", "priority": "high"},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"

def test_delete_missing_incident(client, headers):
    response = client.delete("/api/v1/incidents/999999", headers=headers)
    assert response.status_code == 404
