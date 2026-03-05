from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)    # "doctor" or "admin"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    bmi = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Study(Base):
    __tablename__ = "studies"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    ga_weeks = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    study_id = Column(Integer, ForeignKey("studies.id"))
    plane = Column(String, nullable=True)
    path = Column(String, nullable=False)

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    study_id = Column(Integer, ForeignKey("studies.id"))
    efw_g = Column(Float)
    who_z = Column(Float)
    who_percentile = Column(Float)
    label = Column(String)
    proba_sga = Column(Float)
    proba_lga = Column(Float)
    tta_sd = Column(Float)
    gradcam_paths = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
