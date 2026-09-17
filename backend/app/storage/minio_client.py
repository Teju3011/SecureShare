import io
from pathlib import Path
from app.storage.base import BaseStorageProvider
from app.core.config import settings


class MinioStorageProvider(BaseStorageProvider):
    def __init__(self):
        try:
            from minio import Minio
            self.client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_SECURE
            )
            self._ensure_buckets()
        except Exception as e:
            # If MinIO is unreachable during initialization, will fall back or log
            self.client = None

    def _ensure_buckets(self):
        if not self.client:
            return
        for bucket in [settings.MINIO_CLEAN_BUCKET, settings.MINIO_QUARANTINE_BUCKET]:
            try:
                if not self.client.bucket_exists(bucket):
                    self.client.make_bucket(bucket)
            except Exception:
                pass

    def save_file(self, filename: str, data: bytes, is_quarantined: bool = False) -> str:
        safe_name = Path(filename).name
        bucket = settings.MINIO_QUARANTINE_BUCKET if is_quarantined else settings.MINIO_CLEAN_BUCKET
        if not self.client:
            raise RuntimeError("MinIO client is not connected.")
        self.client.put_object(
            bucket_name=bucket,
            object_name=safe_name,
            data=io.BytesIO(data),
            length=len(data)
        )
        zone = "quarantine" if is_quarantined else "clean"
        return f"{zone}/{safe_name}"

    def get_file(self, storage_path: str, is_quarantined: bool = False) -> bytes:
        safe_name = Path(storage_path).name
        bucket = settings.MINIO_QUARANTINE_BUCKET if is_quarantined else settings.MINIO_CLEAN_BUCKET
        if not self.client:
            raise RuntimeError("MinIO client is not connected.")
        response = self.client.get_object(bucket, safe_name)
        try:
            return response.read()
        finally:
            response.close()
            response.release_conn()

    def delete_file(self, storage_path: str, is_quarantined: bool = False) -> bool:
        safe_name = Path(storage_path).name
        bucket = settings.MINIO_QUARANTINE_BUCKET if is_quarantined else settings.MINIO_CLEAN_BUCKET
        if not self.client:
            return False
        try:
            self.client.remove_object(bucket, safe_name)
            return True
        except Exception:
            return False

    def move_to_clean(self, storage_path: str) -> str:
        safe_name = Path(storage_path).name
        if not self.client:
            raise RuntimeError("MinIO client is not connected.")
        # Copy from quarantine bucket to clean bucket
        from minio.commonconfig import CopySource
        copy_source = CopySource(settings.MINIO_QUARANTINE_BUCKET, safe_name)
        self.client.copy_object(settings.MINIO_CLEAN_BUCKET, safe_name, copy_source)
        self.client.remove_object(settings.MINIO_QUARANTINE_BUCKET, safe_name)
        return f"clean/{safe_name}"
