"""
Profile model for Instagram users
"""
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.utils.database import Base

class Profile(Base):
    """Instagram profile model"""
    __tablename__ = "profiles"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic profile info
    username = Column(String, unique=True, index=True, nullable=False)
    followers_count = Column(Integer, default=0)
    
    # Aggregated metrics
    total_videos = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    total_likes = Column(Integer, default=0)
    total_comments = Column(Integer, default=0)
    
    # Average engagement rates
    avg_likes_rate = Column(Float, default=0.0)
    avg_comments_rate = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    videos = relationship("Video", back_populates="profile")
    
    def __repr__(self):
        return f"<Profile(id={self.id}, username='{self.username}', followers={self.followers_count})>"
