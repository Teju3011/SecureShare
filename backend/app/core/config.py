from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    PROJECT_NAME: str = "SECURESHARE"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # Security & Tokens
    SECRET_KEY: str = "secureshare-super-secret-jwt-signing-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # AES-256-GCM Encryption Key (64-character hex string representing 32 bytes)
    FILE_ENCRYPTION_KEY_HEX: str = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"

    # Database
    DATABASE_URL: str = "sqlite:///./secureshare.db"

    # Storage
    STORAGE_PROVIDER: str = "local"  # "local" or "minio"
    STORAGE_LOCAL_ROOT: str = "./storage_data"

    # MinIO
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "secureshare_minio_user"
    MINIO_SECRET_KEY: str = "secureshare_minio_secret_password"
    MINIO_CLEAN_BUCKET: str = "secureshare-clean"
    MINIO_QUARANTINE_BUCKET: str = "secureshare-quarantine"
    MINIO_SECURE: bool = False

    # ClamAV
    CLAMAV_HOST: str = "localhost"
    CLAMAV_PORT: int = 3310
    CLAMAV_TIMEOUT_SECONDS: int = 10
    CLAMAV_MODE: str = "smart"  # "live" or "smart"

    # Limits
    MAX_FILE_SIZE_BYTES: int = 50 * 1024 * 1024  # 50 MB

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]

    @property
    def encryption_key_bytes(self) -> bytes:
        try:
            raw = bytes.fromhex(self.FILE_ENCRYPTION_KEY_HEX.strip())
            if len(raw) == 32:
                return raw
        except Exception:
            pass
        # Fallback to deterministic 32-byte sha256 if hex is not formatted
        import hashlib
        return hashlib.sha256(self.FILE_ENCRYPTION_KEY_HEX.encode("utf-8")).digest()


settings = Settings()
