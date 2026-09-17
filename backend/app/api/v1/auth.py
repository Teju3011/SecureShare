from fastapi import APIRouter, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, get_client_ip, get_user_agent
from app.core.rate_limit import rate_limit_check
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, Token, MfaSetupResponse, MfaVerifyRequest
from app.schemas.user import UserResponse
from app.services.user_service import UserService
from app.audit.logger import log_security_event

router = APIRouter(prefix="/auth", tags=["Authentication & MFA"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limit_check("auth_register", max_requests=10, window_seconds=60))]
)
def register(
    req: RegisterRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    ip = get_client_ip(request)
    ua = get_user_agent(request)
    user = UserService.register_user(
        db=db,
        email=req.email,
        full_name=req.full_name,
        password=req.password,
        client_ip=ip,
        user_agent=ua
    )
    return user


@router.post(
    "/login",
    response_model=Token,
    dependencies=[Depends(rate_limit_check("auth_login", max_requests=15, window_seconds=60))]
)
def login(
    req: LoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    ip = get_client_ip(request)
    ua = get_user_agent(request)
    result = UserService.authenticate_user(
        db=db,
        email=req.email,
        password=req.password,
        totp_code=req.totp_code,
        client_ip=ip,
        user_agent=ua
    )
    return result


@router.post("/login-form", response_model=Token, include_in_schema=False)
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None,
    db: Session = Depends(get_db)
):
    """Provides OAuth2 compatibility for Swagger UI."""
    ip = get_client_ip(request)
    ua = get_user_agent(request)
    result = UserService.authenticate_user(
        db=db,
        email=form_data.username,
        password=form_data.password,
        client_ip=ip,
        user_agent=ua
    )
    return result


@router.get("/me", response_model=UserResponse)
def get_current_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/mfa/setup", response_model=MfaSetupResponse)
def setup_mfa(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    setup_data = UserService.setup_mfa(current_user, db)
    return setup_data


@router.post("/mfa/verify")
def verify_mfa(
    req: MfaVerifyRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ip = get_client_ip(request)
    ua = get_user_agent(request)
    success = UserService.verify_and_enable_mfa(
        user=current_user,
        code=req.code,
        db=db,
        client_ip=ip,
        user_agent=ua
    )
    return {"success": success, "message": "MFA has been successfully activated on your account."}


@router.post("/logout")
def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ip = get_client_ip(request)
    ua = get_user_agent(request)
    log_security_event(
        db=db,
        action="USER_LOGOUT",
        resource_type="auth",
        actor_id=current_user.id,
        actor_email=current_user.email,
        ip_address=ip,
        user_agent=ua,
        result="SUCCESS"
    )
    return {"message": "Logged out successfully."}
