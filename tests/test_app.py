import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test"""
    original_activities = {
        "Basketball": {
            "description": "Team sport focusing on shooting, dribbling, and defensive skills",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Individual and doubles tennis training and matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["sarah@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater productions, acting techniques, and stage performance",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["alex@mergington.edu", "jessica@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, sculpture, and various visual arts",
            "schedule": "Mondays and Fridays, 3:30 PM - 4:45 PM",
            "max_participants": 18,
            "participants": ["maya@mergington.edu"]
        },
        "Debate Team": {
            "description": "Competitive debate, research skills, and public speaking",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["david@mergington.edu", "rachel@mergington.edu"]
        },
        "Math Olympiad": {
            "description": "Advanced problem-solving and mathematical competition preparation",
            "schedule": "Tuesdays, 4:00 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["kevin@mergington.edu"]
        },
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
    
    yield
    
    # Reset to original state
    activities.clear()
    activities.update(original_activities)


class TestRootEndpoint:
    def test_root_redirects_to_index(self, client):
        """Test that root redirects to /static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestActivitiesEndpoint:
    def test_get_all_activities(self, client):
        """Test retrieving all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9
        assert "Basketball" in data
        assert "Tennis Club" in data
        assert data["Basketball"]["description"] == "Team sport focusing on shooting, dribbling, and defensive skills"
        assert data["Basketball"]["participants"] == ["james@mergington.edu"]

    def test_activities_have_required_fields(self, client):
        """Test that activities have all required fields"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


class TestSignupEndpoint:
    def test_signup_new_participant(self, client):
        """Test signing up a new participant"""
        response = client.post(
            "/activities/Basketball/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]
        assert "newstudent@mergington.edu" in data["message"]
        
        # Verify participant was added
        activities_response = client.get("/activities")
        assert "newstudent@mergington.edu" in activities_response.json()["Basketball"]["participants"]

    def test_signup_existing_participant(self, client):
        """Test that signup fails for already registered participant"""
        response = client.post(
            "/activities/Basketball/signup?email=james@mergington.edu"
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_nonexistent_activity(self, client):
        """Test that signup fails for non-existent activity"""
        response = client.post(
            "/activities/Nonexistent/signup?email=student@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_multiple_participants(self, client):
        """Test signing up multiple participants to same activity"""
        response1 = client.post(
            "/activities/Tennis Club/signup?email=student1@mergington.edu"
        )
        assert response1.status_code == 200
        
        response2 = client.post(
            "/activities/Tennis Club/signup?email=student2@mergington.edu"
        )
        assert response2.status_code == 200
        
        # Verify both were added
        activities_response = client.get("/activities")
        participants = activities_response.json()["Tennis Club"]["participants"]
        assert "student1@mergington.edu" in participants
        assert "student2@mergington.edu" in participants
        assert len(participants) == 3  # original + 2 new


class TestUnregisterEndpoint:
    def test_unregister_existing_participant(self, client):
        """Test unregistering an existing participant"""
        response = client.delete(
            "/activities/Basketball/unregister?email=james@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "Unregistered" in data["message"]
        assert "james@mergington.edu" in data["message"]
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        assert "james@mergington.edu" not in activities_response.json()["Basketball"]["participants"]

    def test_unregister_nonexistent_participant(self, client):
        """Test that unregister fails for non-existent participant"""
        response = client.delete(
            "/activities/Basketball/unregister?email=nonexistent@mergington.edu"
        )
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"]

    def test_unregister_from_nonexistent_activity(self, client):
        """Test that unregister fails for non-existent activity"""
        response = client.delete(
            "/activities/Nonexistent/unregister?email=student@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_multiple_times(self, client):
        """Test that unregister fails when called twice"""
        # First unregister
        response1 = client.delete(
            "/activities/Drama Club/unregister?email=alex@mergington.edu"
        )
        assert response1.status_code == 200
        
        # Second unregister should fail
        response2 = client.delete(
            "/activities/Drama Club/unregister?email=alex@mergington.edu"
        )
        assert response2.status_code == 400
        assert "not signed up" in response2.json()["detail"]


class TestSignupAndUnregisterFlow:
    def test_signup_then_unregister(self, client):
        """Test signing up and then unregistering"""
        email = "testflow@mergington.edu"
        activity = "Math Olympiad"
        
        # Sign up
        signup_response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        assert signup_response.status_code == 200
        
        # Verify signed up
        get_response = client.get("/activities")
        assert email in get_response.json()[activity]["participants"]
        
        # Unregister
        unregister_response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        assert unregister_response.status_code == 200
        
        # Verify unregistered
        final_response = client.get("/activities")
        assert email not in final_response.json()[activity]["participants"]
