from sqlalchemy import (
    Column, BigInteger, String, ForeignKey, Date
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Teacher(Base):
    __tablename__ = 'teachers'

    teacher_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    courses = relationship('Course', back_populates='teacher', cascade="all, delete-orphan")

class Course(Base):
    __tablename__ = 'courses'

    course_id = Column(BigInteger, primary_key=True, autoincrement=True)
    course_name = Column(String(100), nullable=False)
    teacher_id = Column(BigInteger, ForeignKey('teachers.teacher_id', ondelete='CASCADE'), nullable=False)
    teacher = relationship('Teacher', back_populates='courses')
    student_courses = relationship('StudentCourse', back_populates='course')

class Student(Base):
    __tablename__ = 'students'

    student_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    option_student_id = Column(String(50))
    student_courses = relationship('StudentCourse', back_populates='student')

class StudentCourse(Base):
    __tablename__ = 'student_courses'
    
    student_id = Column(BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), primary_key=True)
    course_id = Column(BigInteger, ForeignKey('courses.course_id', ondelete='CASCADE'), primary_key=True)
    enrollment_date = Column(Date, nullable=False)
    student = relationship('Student', back_populates='student_courses')
    course = relationship('Course', back_populates='student_courses')