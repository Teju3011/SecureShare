from abc import ABC, abstractmethod


class BaseStorageProvider(ABC):
    @abstractmethod
    def save_file(self, filename: str, data: bytes, is_quarantined: bool = False) -> str:
        """Saves encrypted file data to storage. Returns relative storage key/path."""
        pass

    @abstractmethod
    def get_file(self, storage_path: str, is_quarantined: bool = False) -> bytes:
        """Retrieves raw encrypted file data from storage."""
        pass

    @abstractmethod
    def delete_file(self, storage_path: str, is_quarantined: bool = False) -> bool:
        """Permanently deletes a file from storage."""
        pass

    @abstractmethod
    def move_to_clean(self, storage_path: str) -> str:
        """Moves a quarantined file into the clean storage zone upon admin release."""
        pass
