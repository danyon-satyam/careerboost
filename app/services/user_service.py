from sqlalchemy.orm import Session
from typing import Optional

from app.models.user import User
from app.core.security import hash_password
from app.core.exceptions import NotFoundError, ConflictError


class UserService:
    """Handles all DB operations for Users."""

    def create_user(
        self,
        db: Session,
        email: str,
        password: str,
        full_name: str
    ) -> User:
        """Create a new user. Raises ConflictError if email exists."""
        existing = self.get_by_email(db, email)
        if existing:
            raise ConflictError("Email already registered")

        user = User(
            email=email.lower().strip(),
            password_hash=hash_password(password),
            full_name=full_name.strip(),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_by_email(
        self,
        db: Session,
        email: str
    ) -> Optional[User]:
        """Fetch user by email. Returns None if not found."""
        return db.query(User).filter(
            User.email == email.lower().strip()
        ).first()

    def get_by_id(
        self,
        db: Session,
        user_id: int
    ) -> User:
        """Fetch user by ID. Raises NotFoundError if not found."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundError("User not found")
        return user

    def update_user(
        self,
        db: Session,
        user_id: int,
        update_data: dict
    ) -> User:
        """Update user fields. Only updates provided fields."""
        user = self.get_by_id(db, user_id)

        for field, value in update_data.items():
            if value is not None:
                setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user

    def delete_user(
        self,
        db: Session,
        user_id: int
    ) -> bool:
        """Soft delete — sets is_active to False."""
        user = self.get_by_id(db, user_id)
        user.is_active = False
        db.commit()
        return True


# Singleton instance — import this everywhere
user_service = UserService()
