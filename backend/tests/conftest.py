import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["ENVIRONMENT"] = "testing"
os.environ["DATABASE_URL"] = "sqlite:///./test_secureshare.db"
os.environ["STORAGE_LOCAL_ROOT"] = "./test_storage_data"
os.environ["CLAMAV_MODE"] = "smart"

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.core.database import Base, get_db
from app.main import app
from app.models.user import User, UserRole
from app.models.audit import AuditLog
from app.security.password import get_password_hash
from app.security.jwt import create_access_token
from app.audit.logger import log_security_event

test_engine = create_engine("sqlite:///./test_secureshare.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()

    # Create admin
    admin = User(
        email="testadmin@example.com",
        full_name="Test Admin",
        hashed_password=get_password_hash("AdminPass123!"),
        role=UserRole.ADMIN,
        is_active=True,
        mfa_enabled=False
    )
    # Create standard user
    user = User(
        email="testuser@example.com",
        full_name="Test Standard User",
        hashed_password=get_password_hash("UserPass123!"),
        role=UserRole.STANDARD_USER,
        is_active=True,
        mfa_enabled=False
    )
    db.add_all([admin, user])
    db.commit()
    db.refresh(admin)
    db.refresh(user)

    # Initial audit log
    log_security_event(
        db=db,
        action="SYSTEM_INIT",
        resource_type="system",
        resource_id="1",
        actor_email="system@example.com",
        result="SUCCESS"
    )

    db.close()

    yield

    Base.metadata.drop_all(bind=test_engine)
    if os.path.exists("./test_secureshare.db"):
        try:
            os.remove("./test_secureshare.db")
        except Exception:
            pass


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def admin_headers():
    db = TestingSessionLocal()
    admin = db.query(User).filter(User.role == UserRole.ADMIN).first()
    token = create_access_token(subject=str(admin.id), role="ADMIN", email=admin.email)
    db.close()
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def user_headers():
    db = TestingSessionLocal()
    user = db.query(User).filter(User.role == UserRole.STANDARD_USER).first()
    token = create_access_token(subject=str(user.id), role="STANDARD_USER", email=user.email)
    db.close()
    return {"Authorization": f"Bearer {token}"}
