from src.app import activities


def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert set(response.json()) == set(activities)


def test_signup_adds_participant(client):
    email = "new.student@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert email in client.get("/activities").json()["Chess Club"]["participants"]


def test_signup_rejects_duplicate_email(client):
    email = "michael@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 400
    assert activities["Chess Club"]["participants"].count(email) == 1


def test_signup_unknown_activity_returns_404(client):
    response = client.post("/activities/Nope/signup", params={"email": "x@mergington.edu"})

    assert response.status_code == 404


def test_unregister_removes_participant(client):
    email = "michael@mergington.edu"

    response = client.delete("/activities/Chess Club/unregister", params={"email": email})

    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_missing_participant_returns_404(client):
    response = client.delete(
        "/activities/Chess Club/unregister", params={"email": "nobody@mergington.edu"}
    )

    assert response.status_code == 404


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete("/activities/Nope/unregister", params={"email": "x@mergington.edu"})

    assert response.status_code == 404
