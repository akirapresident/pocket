"""
Profile router for API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.utils.database import get_db
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate, Profile as ProfileSchema, ProfileList

router = APIRouter()

@router.get("/", response_model=ProfileList)
async def get_profiles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all profiles with pagination"""
    profiles = db.query(Profile).offset(skip).limit(limit).all()
    total = db.query(Profile).count()
    
    return ProfileList(
        profiles=profiles,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@router.get("/{profile_id}", response_model=ProfileSchema)
async def get_profile(profile_id: int, db: Session = Depends(get_db)):
    """Get profile by ID"""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.get("/username/{username}", response_model=ProfileSchema)
async def get_profile_by_username(username: str, db: Session = Depends(get_db)):
    """Get profile by username"""
    profile = db.query(Profile).filter(Profile.username == username).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/", response_model=ProfileSchema)
async def create_profile(
    profile_data: ProfileCreate,
    db: Session = Depends(get_db)
):
    """Create new profile"""
    # Check if profile already exists
    existing_profile = db.query(Profile).filter(Profile.username == profile_data.username).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists")
    
    db_profile = Profile(**profile_data.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    
    return db_profile

@router.put("/{profile_id}", response_model=ProfileSchema)
async def update_profile(
    profile_id: int,
    profile_update: ProfileUpdate,
    db: Session = Depends(get_db)
):
    """Update profile data"""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    update_data = profile_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
    
    db.commit()
    db.refresh(profile)
    return profile

@router.delete("/{profile_id}")
async def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    """Delete profile"""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    db.delete(profile)
    db.commit()
    return {"message": "Profile deleted successfully"}
