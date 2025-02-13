# =========================================================================== #
# Author: Omer Kemal                                                          #
# Website: https://www.johndoe.com                                            #
# Social Media:                                                               #
#   - Facebook: https://www.facebook.com/johndoe                              #
#   - Telegram: https://t.me/johndoe                                          #
#   - Twitter: @JohnDoe                                                       #
#   - GitHub: https://github.com/johndoe                                      #
# =========================================================================== #

from sqlalchemy import ForeignKey, String, Integer, Column, Float
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Admin(Base):
    __tablename__ = 'admin'
    ID = Column("id", String, primary_key=True)
    fullname = Column("name", String(20), nullable=False,primary_key=True)
    password = Column("password", String(20), nullable=False)

    def __init__(self, ID, fullname, password):
        self.ID = ID
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        admin_data = f"({self.ID}-{self.fullname}-{self.password})"
        return admin_data


class Subjects(Base):
    __tablename__ = 'subjects'

    ID = Column('id', String, primary_key=True)
    subject = Column('subject',String, nullable=False)
    stauts = Column('stauts',String,nullable=False)

    def __init__(self, ID, subject, stauts):
        self.ID = ID
        self.subject = subject
        self.stauts = stauts

    def __repr__(self):
        subjuct_data = f'({self.ID}-{self.subject}-{self.stauts})'
        return subjuct_data


class Teacher(Base):
    __tablename__ = 'teacher'

    ID = Column("id", String, primary_key=True)
    fname = Column("fname", String(20), nullable=False)
    mname = Column("mname", String(20), nullable=False)
    lname = Column("lname", String(20), nullable=False)
    gender = Column('gender',String(2))
    password = Column("password", String(20), nullable=False)

    def __init__(self, ID, fname, mname, lname, gender, password):
        self.ID = ID
        self.fname = fname
        self.mname = mname
        self.lname = lname
        self.gender = gender
        self.password = password

    def __repr__(self):
        teacher_data = f"({self.ID}-{self.fname}-{self.mname}-{self.lname}-{self.gender}-{self.password})"
        return teacher_data


class Student(Base):

    """docstring for Student"""
    __tablename__ ='student'

    ID = Column("id", String, primary_key=True)
    fname = Column("first_name", String(20), nullable=False)
    mname = Column("middl_name", String(20), nullable=False)
    lname = Column("last_name", String(20), nullable=False)
    gender = Column("gender", String(2),nullable=False)
    grade = Column("grade", Integer)
    section = Column("section", String(20))
    password = Column("password", String(20),nullable=False)

    def __init__(self, ID, fname, mname, lname, gender, password, section, grade):
        self.ID = ID
        self.fname = fname
        self.mname = mname
        self.lname = lname
        self.gender = gender
        self.password = password
        self.section = section
        self.grade = grade

    def __repr__(self):
        student_data = f"({self.ID}-{self.fname}-{self.mname}-{self.lname}-{self.gender}-{self.password}-{self.section}-{self.grade})"
        return student_data


class Parent(Base):
    __tablename__ = 'parent'

    ID = Column("id", String, primary_key=True)
    student_id = Column('student_id',String,ForeignKey('student.id'))
    hous_number = Column('hous_number',Integer,primary_key=True,nullable=False)
    fname = Column('fname',String,nullable=False)
    lname = Column('lname',String,nullable=False)
    phone = Column('phone',Integer,nullable=False)
    email = Column('email',String,nullable=False)


    def __init__(self,ID,hous_number,fname,lname,phone,email):
        self.ID = ID
        self.hous_number = hous_number
        self.fname = fname
        self.lname = lname
        self.phone = phone
        self.email = email
    
    def __repr__(self):

        Parent = f'({self.ID}-{self.student_id}-{self.hous_number}-{self.fname}-{self.lname}-{self.phone}-{self.email})'
        return Parent


class CreatAssessment(Base):

    __tablename__ = 'createassessment'

    ID = Column('id', String, nullable=False, primary_key=True)
    Assessment_of = Column('assessment_of',ForeignKey('teacher.id'))
    Assessment_name = Column('assessment_name',String)
    Mark = Column('mark',Float)

    def __init__(self,ID, Assessment_name, Assessment_of, Mark):
        self.ID = ID
        self.Assessment_of = Assessment_name
        self.Assessment_name = Assessment_name
        self.Mark = Mark

    def __repr__(self):
        assessment_data = f"({self.ID}-{self.Assessment_of}-{self.Assessment_name}-{self.Mark})"
        return assessment_data


class Assessment(Base):

    __tablename__ = 'assessment'

    ID = Column('id',String, primary_key=True, nullable=False)
    student_id = Column('student_id', String,ForeignKey('student.id'), nullable=False)
    teacher_id = Column('teacher_id', String,ForeignKey('teacher.id'), nullable=False)
    subject_id = Column('subject_id', String, ForeignKey('subjects.id'), nullable=False)
    grade = Column('grade',String,nullable=False)
    section = Column('section',String,nullable=False)
    AssessmentName = Column('assessmentName',Float,nullable=False)
    ScoreMark = Column('Score_Mark',String, nullable=False)

    def __init__(self, ID, student_id, teacher_id, subject_id,grade,section, AssessmentName, ScoreMark):
        self.ID = ID
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.subject_id = subject_id
        self.grade = grade
        self.section = section
        self.AssessmentName = AssessmentName
        self.ScoreMark = ScoreMark

    def __repr__(self):
        AssessmentData = f"({self.ID}-{self.student_id}-{self.teacher_id}-{self.subject_id}-{self.grade}-{self.section}-{self.AssessmentName}-{self.ScoreMark})"
        return AssessmentData


class totalAssessment(Base):

    __tablename__ = 'total_assessment'

    ID = Column("id",String,nullable=False,primary_key=True)
    student_id = Column('srtudent_id',String,ForeignKey('student.id'),nullable=False)
    teacher_id = Column('teacher_id',String,ForeignKey('teacher.id'),nullable=False)
    total_mark = Column('total_mark',Float,nullable=False)

    def __init__(self, ID,student_id,teacher_id,total_mark):
        self.ID = ID
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.total_mark = total_mark
    
    def __repr__(self):
        totalassessment = f"({self.ID}-{self.student_id}-{self.teacher_id}-{self.total_mark})"

        return totalassessment


class avrage(Base):

    __tablename__ = 'avrage'

    ID = Column('id',String,primary_key=True,nullable=False)
    student_id = Column('student_id',String,ForeignKey('student.id'),nullable=False)
    Subjects = Column('subject', String, ForeignKey('subjects.id'),nullable=False)
    avrage = Column('avrage',Integer,nullable=False)
    simister = Column('simister',Float,nullable=False)

    def __init__(self,ID,student_id,avrage,simister):
        self.ID = ID
        self.student_id = student_id
        self.avrage = avrage
        self.simister = simister

    def __repr__(self):
        avrage = f'({self.ID}-{self.student_id}-{self.avrage}-{self.simister})'

        return avrage


class rank(Base):

    __tablename__ = 'rank'

    ID = Column('id',String,primary_key=True,nullable=False)
    student_id = Column('student_id',String,ForeignKey('student.id'),nullable=False)
    rank = Column('rank',Integer,nullable=False)
    simister = Column('simister',Float,nullable=False)

    def __init__(self,ID,student_id,rank,simister):
        self.ID = ID
        self.student_id = student_id
        self.rank = rank
        self.simister = simister

    def __repr__(self):
        rank = f'({self.ID}-{self.student_id}-{self.rank}-{self.simister})'

        return rank


class Sections(Base):

    __tablename__ = 'section'

    ID = Column('id',String,primary_key=True)
    section = Column('section',String)
    grade = Column('grade',Integer)


    def __init__(self,ID,section,grade):
        self.ID = ID
        self.section = section
        self.grade = grade


    def __repr__(self):
        section = f'({self.ID}-{self.grade}-{self.section})'
        return section


class thought(Base):
    __tablename__ = 'thought'

    ID = Column('id', String, primary_key=True, nullable=False)
    subject_id = Column('subject_id', String, ForeignKey('subjects.id'), nullable=False)
    teacher_id = Column('teacher_id', String, ForeignKey('teacher.id'), nullable=False)
    grade = Column('grade', String, nullable=False)
    section = Column('section', String, nullable=False)
    access_level = Column('access_level',String, nullable=False)

    def __init__(self, ID, subject_id, teacher_id, grade, section, access_level):
        self.ID = ID
        self.subject_id = subject_id
        self.teacher_id = teacher_id
        self.grade = grade
        self.section = section
        self.access_level = access_level


    def __repr__(self):
        thought_data = f'({self.ID}-{self.subject_id}-{self.teacher_id}-{self.grade}-{self.section}-{self.access_level})'
        return thought_data


class Resource(Base):
    __tablename__ = 'resource'

    ID = Column('id', String, primary_key=True, nullable=False)
    section_id = Column('section_id', String, ForeignKey('section.id'), nullable=False)
    description = Column('description',String,nullable=True)
    file_name = Column('file_name',String,nullable=False)
    path = Column('path',String,nullable=False)
    post_t = Column('post_t',String,ForeignKey('teacher.id'),nullable=False)
    post_a = Column('post_a',String,ForeignKey('admin.id'),nullable=False)
    resource_type = Column('resource_type',String,nullable=False)
    valid = Column('valid',Integer,nullable=False)


    def __init__(self, ID, section_id,description,file_name,path,post_t,post_a,resource_type,valid):
        self.ID = ID
        self.section_id = section_id
        self.description = description
        self.file_name = file_name
        self.path = path
        self.post_t = post_t
        self.post_a = post_a
        self.resource_type = resource_type
        self.valid = valid


    def __repr__(self):
        resource = f'({self.ID}-{self.section_id}-{self.description}-{self.file_name}-{self.path}-{self.post_t}-{self.post_a}-{self.resource_type})'
        return resource

