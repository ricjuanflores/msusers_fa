from abc import ABC, abstractmethod
from sqlalchemy.orm import Session


class Seeder(ABC):
    """Base class for all seeders."""
    
    priority: int = 50  # Lower number = runs first
    
    def __init__(self, db: Session):
        self.db = db
    
    @abstractmethod
    def run(self) -> None:
        """Execute the seeder. Must be implemented by subclasses."""
        pass
    
    def commit(self) -> None:
        """Commit changes to the database."""
        self.db.commit()
    
    def rollback(self) -> None:
        """Rollback changes."""
        self.db.rollback()
