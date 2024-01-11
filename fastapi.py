from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, Integer, String, create_engine, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from databases import Database
from pydantic import BaseModel
import sqlalchemy
from typing import Union
from pydantic import validator
from sqlalchemy.exc import IntegrityError

DATABASE_URL = "mysql+mysqlconnector://root@localhost/mydb"

database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Model
class Parent(Base):
    __tablename__ = "parent"

    id_parent = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, index=True)
    username = Column(String, index=True)
    password = Column(String)
    koordinat_lattitude = Column(Float)
    koordinat_longtitude = Column(Float)

class Tracker(Base):
    __tablename__ = "tracker"
    id_tracker = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama_anak = Column(String, index=True)
    lokasi = Column(String)
    koordinat_lattitude = Column(Float)
    koordinat_longtitude = Column(Float)


# Controller
# ==================Parent (ortu)==================
class ParentCreate(BaseModel):
    
    email: str
    username: str
    password: str
    koordinat_lattitude: float
    koordinat_longtitude: float

class ParentUpdate(BaseModel):
    id_parent: int
    # email: str
    # username: str
    # password: str
    koordinat_lattitude: float
    koordinat_longtitude: float

class ParentResponse(BaseModel):
    id_parent: int
    email: str
    username: str
    koordinat_lattitude: float
    koordinat_longtitude: float
    
class ParentUpdateResponse(BaseModel):
    id_parent: int
    koordinat_lattitude: float
    koordinat_longtitude: float
    
#==================Tracker (anak)==================
class TrackerCreate(BaseModel):
    
    id_tracker: str
    nama_anak: str
    lokasi: str
    koordinat_lattitude: float
    koordinat_longtitude: float

class TrackerUpdate(BaseModel):
    id_tracker: str
    # nama_anak: str
    # lokasi: str
    koordinat_lattitude: float
    koordinat_longtitude: float

class TrackerResponse(BaseModel):
    id_tracker: str
    nama_anak: str
    lokasi: str
    koordinat_lattitude: float
    koordinat_longtitude: float
    
class TrackerUpdateResponse(BaseModel):
    id_tracker: str
    koordinat_lattitude: float
    koordinat_longtitude: float

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes (Ortu)
@app.post("/parents/create", response_model=ParentResponse)
async def create_parent(parent: ParentCreate, db: Session = Depends(get_db)):
    try:
        db_parent = Parent(**parent.dict())
        db.add(db_parent)
        db.commit()
        db.refresh(db_parent)
        return ParentResponse(
            id_parent=db_parent.id_parent,
            email=db_parent.email,
            username=db_parent.username,
            koordinat_lattitude=db_parent.koordinat_lattitude,
            koordinat_longtitude=db_parent.koordinat_longtitude
        )
    except IntegrityError as e:
        # Handle duplicate email error
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e.orig))

@app.get("/parents", response_model=list[ParentResponse])
async def read_parents(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    parents = db.query(Parent).offset(skip).limit(limit).all()
    return [{"id_parent": parent.id_parent, "email": parent.email, "username": parent.username, "koordinat_lattitude": parent.koordinat_lattitude, "koordinat_longtitude": parent.koordinat_longtitude} for parent in parents]

@app.put("/parents/update", response_model=ParentUpdateResponse)
async def update_parent(parent: ParentUpdate, db: Session = Depends(get_db)):
    parent_id = parent.id_parent

    # Retrieve the existing record from the database
    db_parent = db.query(Parent).filter(Parent.id_parent == parent_id).first()

    if db_parent:
        try:
            # Update the fields with the new values
            db_parent.koordinat_lattitude = parent.koordinat_lattitude
            db_parent.koordinat_longtitude = parent.koordinat_longtitude

            db.commit()
            db.refresh(db_parent)

            # Return the updated values
            return ParentUpdateResponse(
                id_parent=db_parent.id_parent,
                koordinat_lattitude=db_parent.koordinat_lattitude,
                koordinat_longtitude=db_parent.koordinat_longtitude
            )
        except IntegrityError as e:
            # Handle duplicate email error or other integrity errors
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e.orig))
    else:
        # If the record with the given ID is not found
        raise HTTPException(status_code=404, detail="Record not found")
    

@app.put("/parents/update", response_model=ParentUpdateResponse)
async def update_parent(parent: ParentUpdate, db: Session = Depends(get_db)):
    parent_id = parent.id_parent

    # Retrieve the existing record from the database
    db_parent = db.query(Parent).filter(Parent.id_parent == parent_id).first()

    if db_parent:
        try:
            # Update the fields with the new values
            db_parent.koordinat_lattitude = parent.koordinat_lattitude
            db_parent.koordinat_longtitude = parent.koordinat_longtitude

            db.commit()
            db.refresh(db_parent)

            # Return the updated values
            return ParentUpdateResponse(
                id_parent=db_parent.id_parent,
                koordinat_lattitude=db_parent.koordinat_lattitude,
                koordinat_longtitude=db_parent.koordinat_longtitude
            )
        except IntegrityError as e:
            # Handle duplicate email error or other integrity errors
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e.orig))
    else:
        # If the record with the given ID is not found
        raise HTTPException(status_code=404, detail="Record not found")

# ==================Tracker==================
    
@app.get("/tracker", response_model=list[TrackerResponse])
async def read_tracker(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    trackers = db.query(Tracker).offset(skip).limit(limit).all()
    return [{"id_tracker": tracker.id_tracker, "nama_anak": tracker.nama_anak, "lokasi": tracker.lokasi, "koordinat_lattitude": tracker.koordinat_lattitude, "koordinat_longtitude": tracker.koordinat_longtitude} for tracker in trackers]

# Routes (anak)
@app.put("/tracker/update", response_model=TrackerUpdateResponse)
async def update_tracker(tracker: TrackerUpdate, db: Session = Depends(get_db)):
    tracker_id = tracker.id_tracker

    # Retrieve the existing record from the database
    db_tracker = db.query(Tracker).filter(Tracker.id_tracker == tracker_id).first()

    if db_tracker:
        try:
            # Update the fields with the new values
            db_tracker.koordinat_lattitude = tracker.koordinat_lattitude
            db_tracker.koordinat_longtitude = tracker.koordinat_longtitude

            db.commit()
            db.refresh(db_tracker)

            # Return the updated values
            return TrackerUpdateResponse(
                id_tracker=db_tracker.id_tracker,
                koordinat_lattitude=db_tracker.koordinat_lattitude,
                koordinat_longtitude=db_tracker.koordinat_longtitude
            )
        except IntegrityError as e:
            # Handle duplicate email error or other integrity errors
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e.orig))
    else:
        # If the record with the given ID is not found
        raise HTTPException(status_code=404, detail="Record not found")