from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from blueprints.users.models import Credentials, User


class CredentialsRepository:
    """Repository for User and Credentials models with Read/Write Separation."""

    def __init__(self, write_db_session: Session, read_db_session: Session):
        """
        Initializes the repository with separate read and write sessions.
        
        :param write_db_session: Session used for write operations
        :param read_db_session: Session used for read operations
        """
        self.write_db_session = write_db_session
        self.read_db_session = read_db_session
    
    def get_all_credentials(self) -> List[Credentials]:
        """Fetch all credentials (Read-Only)."""
        return self.read_db_session.query(Credentials).all()

    def get_credentials_by_id(self, user_id: int) -> Optional[Credentials]:
        """Fetch a user by ID (Read-Only)."""
        return self.read_db_session.query(Credentials).filter(Credentials.id == user_id).first()
    
    def get_credentials_by_email(self,email:str) -> Optional[Credentials]:
        return self.read_db_session.query(Credentials).filter(Credentials.email == email).first()
    

    def create_credentials(self, email:str, password:str) -> int:
        """Create new credentials (Write Operation)."""
        credentials = Credentials(email = email, password = password)
        self.write_db_session.add(credentials)
        self.write_db_session.flush()
        return credentials.id

    def delete_credentials(self, user_id: int) -> Optional[User]:
        """Delete a user by ID (Write Operation)."""
        user = self.get_credentials_by_id(user_id)
        if user:
            self.write_db_session.delete(user)
        return user
    
    def soft_delete_credentials(self, user_id: int) -> Optional[User]:
        """Soft delete a user by ID (Write Operation)."""
        user = self.get_credentials_by_id(user_id)
        if user:
            user.deleted_at = datetime.now()
        return user

    def update_credentials(self, cred_id: int, **kwargs) -> Optional[User]:
        """Update user fields (Write Operation)."""
        cred = self.get_credentials_by_id(cred_id)
        if cred:
            for key, value in kwargs.items():
                setattr(cred, key, value)
            return cred
        self.write_db_session.commit()
        self.write_db_session.refresh(cred)
        return None
