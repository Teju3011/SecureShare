import os
from typing import Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.core.config import settings


class FileEncryptor:
    def __init__(self, key: bytes = None):
        self._key = key or settings.encryption_key_bytes
        if len(self._key) != 32:
            raise ValueError(f"AES-256 key must be exactly 32 bytes (got {len(self._key)})")
        self._aesgcm = AESGCM(self._key)

    def encrypt(self, data: bytes) -> Tuple[str, bytes]:
        """
        Encrypts plaintext bytes using AES-256-GCM.
        Generates a 12-byte cryptographically secure random nonce.
        Returns:
            (nonce_hex, ciphertext_with_auth_tag)
        """
        nonce = os.urandom(12)  # 96-bit nonce recommended for GCM
        ciphertext = self._aesgcm.encrypt(nonce, data, associated_data=None)
        return nonce.hex(), ciphertext

    def decrypt(self, nonce_hex: str, ciphertext: bytes) -> bytes:
        """
        Decrypts ciphertext with authentication tag verification.
        Raises InvalidTag exception if data has been tampered with.
        """
        nonce = bytes.fromhex(nonce_hex)
        plaintext = self._aesgcm.decrypt(nonce, ciphertext, associated_data=None)
        return plaintext


file_encryptor = FileEncryptor()
