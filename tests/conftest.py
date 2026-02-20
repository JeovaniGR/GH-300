import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test"""
    from src.app import activities
    
    # Store original state
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
