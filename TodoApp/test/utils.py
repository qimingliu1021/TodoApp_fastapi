from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
import pytest
from ..models import Todos, Users
from ..routers.auth import bcrypt_context

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
  SQLALCHEMY_DATABASE_URL, 
  connect_args={"check_same_thread": False}, 
  poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db(): 
  db = TestingSessionLocal()
  try: 
    yield db
  finally: 
    db.close()

def override_get_current_user(): 
  return {'qiming_test': 'testing', 'id': 1, 'user_role': 'admin'}


@pytest.fixture
def test_todo(): 
  todo = Todos(
    title = 'learn to code', 
    description = 'Need to learn it everyday', 
    priority = 5, 
    complete = False, 
    owner_id = 1
  )

  db = TestingSessionLocal()
  db.add(todo)
  db.commit()
  yield todo
  with engine.connect() as connection: 
    connection.execute(text("DELETE FROM Todos"))
    connection.commit()


@pytest.fixture
def test_user(): 
  print("running test_user() ......")
  user = Users(
    username="qiming_test", 
    email="test@gmail.com", 
    first_name="Qiming",
    last_name="Liu", 
    hashed_password=bcrypt_context.hash("testpassword"), 
    role="admin", 
    phone_number="111-111-1111"
  )

  print("running Testing SessionLocal() ......")

  db = TestingSessionLocal()
  db.add(user)
  db.commit()
  yield user
  with engine.connect() as connection: 
    connection.execute(text("DELETE FROM users;"))
    connection.commit()


