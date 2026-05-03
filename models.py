from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base


class StudySession(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    duration_minutes = Column(Integer)
    notes = Column(String, nullable=True)

    # ✅ MUST allow real dates OR NULL
    date = Column(Date, nullable=True)
    
class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    daily_goal_minutes = Column(Integer, default=60)


