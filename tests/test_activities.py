def test_get_activities_returns_expected_keys(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # basic sanity check for a few known activities
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_new_participant(client):
    activity = "Soccer Team"
    email = "testuser@example.com"
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    # verify in-memory state updated
    from src.app import activities
    assert email in activities[activity]["participants"]


def test_unregistered_participant_removed(client):
    activity = "Chess Club"
    email = "michael@mergington.edu"
    # precondition
    from src.app import activities
    assert any(p.strip().lower() == email for p in activities[activity]["participants"])

    resp = client.delete(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert all(p.strip().lower() != email for p in activities[activity]["participants"])


def test_activity_not_found_returns_404(client):
    resp = client.post("/activities/NoSuchActivity/signup?email=a@b.com")
    assert resp.status_code == 404
    resp = client.delete("/activities/NoSuchActivity/signup?email=a@b.com")
    assert resp.status_code == 404


def test_duplicate_signup_allowed_current_behavior(client):
    activity = "Art Club"
    email = "dup@example.com"
    # two signups of the same email are currently allowed
    r1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert r1.status_code == 200
    r2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert r2.status_code == 200
    from src.app import activities
    matches = [p for p in activities[activity]["participants"] if p == email]
    assert len(matches) >= 2
