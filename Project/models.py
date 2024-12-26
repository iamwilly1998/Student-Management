import enum
from sqlalchemy.ext.hybrid import hybrid_property
from Project.extensions import db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum, Text, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime


#ENUM
class UserRole(enum.Enum):
    HOCSINH = "Học sinh"
    NHANVIEN = "Nhân viên"
    GIAOVIEN = "Giáo viên"
    ADMIN = "Người quản trị"

class LoaiTTLL(enum.Enum):
    EMAIL = "Email"
    DTCANHAN = "Số điện thoại"
class Grade(enum.Enum):
    K10 = 10
    K11 = 11
    K12 = 12
class ScoreType(enum.Enum):
    MINS15 = 0
    MINS45 = 1
    FINAL = 2
#DATABASE ORM
class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key= True, autoincrement= True)
    created_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default= True)

class User(BaseModel, UserMixin):

    family_name = Column(String(50), nullable= False)
    first_name = Column(String(10), nullable=False)
    gender = Column(Boolean)
    address = Column(Text)
    birthdate = Column(String(10))
    username = Column(String(20), nullable= False, unique=True)
    password = Column(String(100), nullable=False)
    image = Column(String(100), default="https://res.cloudinary.com/dzm6ikgbo/image/upload/v1703999894/okrajh0yr69c5fmo3swn.png")
    @hybrid_property
    def name(self):
        return self.family_name+" " +self.first_name
    student = relationship("Student", backref="student_info", lazy=True)
    employee = relationship('Employee', backref="employee_info", lazy= True)
    contacts = relationship('UserContact', backref = "user", lazy=True)

    roles = relationship("UserRoles", backref="user_info", lazy=True)
    admin = relationship("Admin", backref="admin_info", lazy=True)
    teacher = relationship("Teacher", backref="teacher_info", lazy=True)
    changes = relationship("ChangedNotification", backref="user_detail", lazy=True)

class UserContact(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    contactType = Column(Enum(LoaiTTLL))
    contactData = Column(String(30))

class ActorBase(db.Model):
    __abstract__ = True

    started_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)
class Employee(ActorBase):
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True, nullable= False, unique= True)


class UserRoles(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable= False)
    role = Column(Enum(UserRole))

class Admin(ActorBase):
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True,unique=True, nullable=False)

class Teacher(ActorBase):
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True, unique=True, nullable=False)
    vanBang = Column(Text)

    classes = relationship("Class", backref="teacher_detail", lazy=True)
    subjects = relationship("Teachers_Subjects", backref="teacher_detail", lazy=True)
    teaching_plan = relationship("TeachingPlan", backref="teacher_detail", lazy=True)
class Semester(db.Model):
    id = Column(String(3), primary_key=True, nullable=False)
    semester = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    students = relationship("Student", backref="semester", lazy=True)
    scores = relationship("Score", backref="semester", lazy=True)
class Class(BaseModel):
    __table_args__ = (UniqueConstraint('name', 'year'),)
    name = Column(String(5), nullable=False)
    amount = Column(Integer, default=0)
    grade = Column(Enum(Grade), nullable=False)
    year = Column(Integer, nullable=False)
    teacher_id = Column(Integer, ForeignKey(Teacher.user_id))

    students = relationship("Students_Classes", backref="class_detail", lazy=True)
    teaching_plan = relationship("TeachingPlan", backref="class_detail", lazy=True)
class Student(ActorBase):
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True, unique=True, nullable=False)
    grade = Column(Enum(Grade), nullable=False, default=Grade.K10)
    semester_id = Column(String(3), ForeignKey(Semester.id), nullable=False)


    classes = relationship("Students_Classes", backref="student_detail", lazy=True)
    scores = relationship("Score", backref="student_detail", lazy=True)
class Students_Classes(db.Model):
    id = Column(Integer, primary_key=True, nullable=False)
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    student_id = Column(Integer, ForeignKey(Student.user_id), nullable=False)

class Subject(BaseModel):
    name = Column(String(20), nullable=False, unique = True)
    grade = Column(Enum(Grade), nullable=False)
    mins15 = Column(Integer, default=1)
    mins45 = Column(Integer, default=1)
    final = Column(Integer, default=1)
    teachers = relationship("Teachers_Subjects", backref="subject_detail", lazy=True)
    teaching_plan = relationship("TeachingPlan", backref="subject_detail", lazy=True)

class Teachers_Subjects(db.Model):
    __table_args__ = (UniqueConstraint('teacher_id', 'subject_id'),)
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey(Teacher.user_id), nullable=False)
    subject_id = Column(Integer,ForeignKey(Subject.id), nullable=False)


class TeachingPlan(BaseModel):
    teacher_id = Column(Integer,ForeignKey(Teacher.user_id), nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False)
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)

    student_scores = relationship("Score", backref="plan_detail", lazy=True)
class Score(BaseModel):
    plan_id = Column(Integer, ForeignKey(TeachingPlan.id), nullable=False)
    student_id = Column(Integer, ForeignKey(Student.user_id), nullable=False)
    semester_id = Column(String(3), ForeignKey(Semester.id), nullable=False)


    details = relationship("ScoreDetails", backref="info", lazy=True)
class ScoreDetails(BaseModel):
    score_id = Column(Integer, ForeignKey(Score.id), nullable=False)
    score_type = Column(Enum(ScoreType), nullable=False)
    score = Column(Float)

class Principle(BaseModel):
    type = Column(String(20), nullable=False, unique=True)
    data = Column(Float)
    description = Column(Text)

class ChangedNotification(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id))
    user_role = Column(Enum(UserRole), nullable=False)
    content = Column(Text)
