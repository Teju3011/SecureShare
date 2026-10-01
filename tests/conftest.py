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

# Add backend directory to sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(root_dir, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.core.database import Base, get_db
from app.main import app
from app.models.user import User, UserRole
from app.models.file import File, FileStatus
from app.models.folder import Folder
from app.models.permission import Permission
from app.models.audit import AuditLog
from app.security.password import get_password_hash
from app.security.jwt import create_access_token
from app.audit.logger import log_security_event
from app.core.rate_limit import limiter

test_engine = create_engine("sqlite:///./test_secureshare.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_limiter_each_test():
    limiter.reset()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()

    admin = User(
        email="testadmin@example.com",
        full_name="Test Admin",
        hashed_password=get_password_hash("AdminPass123!"),
        role=UserRole.ADMIN,
        is_active=True,
        mfa_enabled=False
    )
    user_std = User(
        email="testuser@example.com",
        full_name="Test Standard User",
        hashed_password=get_password_hash("UserPass123!"),
        role=UserRole.STANDARD_USER,
        is_active=True,
        mfa_enabled=False
    )
    user_a = User(
        email="usera@example.com",
        full_name="User Alpha",
        hashed_password=get_password_hash("UserPass123!"),
        role=UserRole.USER,
        is_active=True,
        mfa_enabled=False
    )
    user_b = User(
        email="userb@example.com",
        full_name="User Bravo",
        hashed_password=get_password_hash("UserPass123!"),
        role=UserRole.USER,
        is_active=True,
        mfa_enabled=False
    )
    auditor = User(
        email="auditor@example.com",
        full_name="Auditor Compliance",
        hashed_password=get_password_hash("AuditorPass123!"),
        role=UserRole.SECURITY_AUDITOR,
        is_active=True,
        mfa_enabled=False
    )

    db.add_all([admin, user_std, user_a, user_b, auditor])
    db.commit()
    db.refresh(admin)
    db.refresh(user_std)
    db.refresh(user_a)
    db.refresh(user_b)
    db.refresh(auditor)

    log_security_event(
        db=db,
        action="TEST_INIT",
        resource_type="system",
        resource_id="1",
        actor_email="system@test.local",
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
    u = db.query(User).filter(User.role == UserRole.ADMIN).first()
    token = create_access_token(subject=str(u.id), role="ADMIN", email=u.email)
    db.close()
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def user_headers():
    db = TestingSessionLocal()
    u = db.query(User).filter(User.email == "testuser@example.com").first()
    token = create_access_token(subject=str(u.id), role="STANDARD_USER", email=u.email)
    db.close()
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def user_a_headers():
    db = TestingSessionLocal()
    u = db.query(User).filter(User.email == "usera@example.com").first()
    token = create_access_token(subject=str(u.id), role="USER", email=u.email)
    db.close()
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def user_b_headers():
    db = TestingSessionLocal()
    u = db.query(User).filter(User.email == "userb@example.com").first()
    token = create_access_token(subject=str(u.id), role="USER", email=u.email)
    db.close()
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auditor_headers():
    db = TestingSessionLocal()
    u = db.query(User).filter(User.role == UserRole.SECURITY_AUDITOR).first()
    token = create_access_token(subject=str(u.id), role="SECURITY_AUDITOR", email=u.email)
    db.close()
    return {"Authorization": f"Bearer {token}"}
