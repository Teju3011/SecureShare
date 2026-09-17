from app.core.config import settings
from app.storage.base import BaseStorageProvider
from app.storage.local_client import LocalStorageProvider

def get_storage_provider() -> BaseStorageProvider:
    if settings.STORAGE_PROVIDER.lower() == "minio":
        try:
            from app.storage.minio_client import MinioStorageProvider
            provider = MinioStorageProvider()
            if provider.client is not None:
                return provider
        except Exception:
            pass
    return LocalStorageProvider()

storage = get_storage_provider()

__all__ = ["BaseStorageProvider", "LocalStorageProvider", "storage", "get_storage_provider"]
