import os
import shutil
from pathlib import Path
from app.storage.base import BaseStorageProvider
from app.core.config import settings


class LocalStorageProvider(BaseStorageProvider):
    def __init__(self, root_dir: str = None):
        self.root = Path(root_dir or settings.STORAGE_LOCAL_ROOT).resolve()
        self.clean_dir = self.root / "clean"
        self.quarantine_dir = self.root / "quarantine"

        self.clean_dir.mkdir(parents=True, exist_ok=True)
        self.quarantine_dir.mkdir(parents=True, exist_ok=True)

    def _get_target_dir(self, is_quarantined: bool) -> Path:
        return self.quarantine_dir if is_quarantined else self.clean_dir

    def _sanitize_path(self, filename: str, is_quarantined: bool) -> Path:
        # Strip path traversal characters
        safe_name = Path(filename).name
        target_dir = self._get_target_dir(is_quarantined)
        resolved_path = (target_dir / safe_name).resolve()
        if not str(resolved_path).startswith(str(target_dir)):
            raise ValueError(f"Security exception: Path traversal attempt detected for {filename}")
        return resolved_path

    def save_file(self, filename: str, data: bytes, is_quarantined: bool = False) -> str:
        safe_name = Path(filename).name
        file_path = self._sanitize_path(safe_name, is_quarantined)
        with open(file_path, "wb") as f:
            f.write(data)
        zone = "quarantine" if is_quarantined else "clean"
        return f"{zone}/{safe_name}"

    def get_file(self, storage_path: str, is_quarantined: bool = False) -> bytes:
        filename = Path(storage_path).name
        file_path = self._sanitize_path(filename, is_quarantined)
        if not file_path.exists():
            raise FileNotFoundError(f"File {storage_path} not found in storage.")
        with open(file_path, "rb") as f:
            return f.read()

    def delete_file(self, storage_path: str, is_quarantined: bool = False) -> bool:
        try:
            filename = Path(storage_path).name
            file_path = self._sanitize_path(filename, is_quarantined)
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception:
            return False

    def move_to_clean(self, storage_path: str) -> str:
        filename = Path(storage_path).name
        src = self._sanitize_path(filename, is_quarantined=True)
        dst = self._sanitize_path(filename, is_quarantined=False)
        if not src.exists():
            raise FileNotFoundError(f"Quarantined file {src} not found.")
        shutil.move(str(src), str(dst))
        return f"clean/{filename}"
