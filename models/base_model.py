"""
Description: Abstract base model for all database tables using SQLAlchemy.
Author: Bryan Vela
Created: 2026-01-29 - File creation and implemented CRUD ops.
"""
from datetime import datetime, timezone
from utils.db import db


class BaseModel(db.Model):
    """
    Abstract base model for all database tables.
    
    Provides common fields and CRUD operations for all models.
    """
    __abstract__ = True
    
    # Common fields
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    
    def to_dict(self):
        """
        Convert model instance to dictionary.
        
        Returns:
            dict: Base dictionary with common fields
        """
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def create(cls, data):
        """
        Create and save a new instance.
        
        Args:
            data (dict): Dictionary of fields to set
            
        Returns:
            BaseModel: The created instance
            
        Raises:
            ValueError: If validation fails
        """
        try:
            instance = cls(**data)
            db.session.add(instance)
            db.session.commit()
            return instance
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to create {cls.__name__}: {str(e)}")
    
    @classmethod
    def get_by_id(cls, id):
        """
        Retrieve an instance by its primary key.
        
        Args:
            id (int): Primary key
            
        Returns:
            BaseModel or None: The found instance or None
        """
        return cls.query.get(id)
    
    @classmethod
    def get_all(cls, limit=100, offset=0):
        """
        Retrieve all instances with pagination.
        
        Args:
            limit (int): Maximum number of records to return
            offset (int): Number of records to skip
            
        Returns:
            list: List of instances
        """
        return cls.query.limit(limit).offset(offset).all()
    
    @classmethod
    def count(cls):
        """
        Count total records.
        
        Returns:
            int: Total number of records
        """
        return cls.query.count()
    
    def update(self, data):
        """
        Update instance fields and save.
        
        Args:
            data (dict): Dictionary of fields to update
            
        Returns:
            BaseModel: Updated instance
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return self
    
    def delete(self):
        """
        Delete the instance from the database.
        
        Returns:
            bool: True if successful
        """
        db.session.delete(self)
        db.session.commit()
        return True
    
    def save(self):
        """
        Save the current instance.
        
        Returns:
            BaseModel: The saved instance
        """
        db.session.add(self)
        db.session.commit()
        return self