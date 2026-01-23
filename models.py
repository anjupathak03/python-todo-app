"""
Todo data model
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Todo:
    """Todo item model"""
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    completed: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create Todo from dictionary"""
        return cls(
            id=data.get("id"),
            title=data.get("title", ""),
            description=data.get("description", ""),
            completed=data.get("completed", False),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
