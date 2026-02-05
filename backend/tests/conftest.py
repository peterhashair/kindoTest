from datetime import date, datetime
import uuid
from fastapi.responses import JSONResponse
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database import Base, get_db
from main import app
import os
import json
import sqlite3
# Import schemas for seeding
from modules.parents.parent_schema import Parent
from modules.schools.school_schema import School
from modules.students.student_schema import Student
from modules.trips.trip_schema import Trip

# --- Teach sqlite3 how to handle UUIDs for database queries ---
sqlite3.register_adapter(uuid.UUID, str)

# This is the definitive fix for the StatementError
# --- Monkey-patch for UUID serialization in JSON responses ---
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return super().default(obj)

class CustomJSONResponse(JSONResponse):
    def render(self, content: any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=UUIDEncoder,
        ).encode("utf-8")

app.default_response_class = CustomJSONResponse
# --- End monkey-patch ---



# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture to override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Apply the override
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Create the database tables before any tests run
    Base.metadata.create_all(bind=engine)
    
    # Seed the database with test data
    db = TestingSessionLocal()
    
    # Add a school for tests to use
    test_school = School(name="Test Academy", id=uuid.uuid4())
    db.add(test_school)
    
    test_parent = Parent(name="Test Parent", email="testparent@example.com", id=uuid.uuid4())
    db.add(test_parent)
    
    # add a student associated with the parent and the school
    test_student = Student(name="Test Student", gender="male", dob=date(2010, 1, 1))
    test_student.parents.append(test_parent)
    db.add(test_student)
    
    # add a trip associated with the school
    test_trip = Trip(
        name="Test Trip",
        destination="Test Destination",
        price_in_cents=int(10000),
        description="A trip for testing",
        start_date=date(2030, 1, 1),
        end_date=date(2030, 1, 2),
        school_id=test_school.id,
        published=True
    )
    db.add(test_trip)
    
    db.commit()
    db.close()

    yield
    
    # Teardown: remove the test database file after all tests in the session are done
    if os.path.exists("test.db"):
        os.remove("test.db")


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c


