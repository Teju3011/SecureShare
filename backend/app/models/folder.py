from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Folder(Base):
    __tablename__ = "folders"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_folder_id = Column(Integer, ForeignKey("folders.id", ondelete="CASCADE"), nullable=True, index=True)
    folder_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    owner = relationship("User", backref="folders")
    files = relationship("File", back_populates="folder")
    subfolders = relationship("Folder", backref="parent", remote_side=[id])
