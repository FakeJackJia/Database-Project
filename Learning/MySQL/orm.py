from urllib.parse import quote_plus
from sqlalchemy import create_engine, select, Table, or_, and_, func, desc, update, delete
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy.types import CHAR
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy import Column, String, DateTime, Integer, Enum, Boolean, ForeignKey
from enum import IntEnum
from datetime import datetime

engine = create_engine('mysql+pymysql://root:%s@localhost:3306/my_database' % quote_plus('Love=@201314'), echo=True)
Base = declarative_base()

class SexEnum(IntEnum):
    MAN = 1
    WOMEN = 2

class User(Base):
    __tablename__ = "user"
    id = Column('id', type_=Integer, primary_key=True)
    user_name = Column(String(32), nullable=False, unique=True)
    password = Column(String(512), nullable=False)
    real_name = Column(String(16))
    sex = Column(Enum(SexEnum), default=None)
    age = Column(TINYINT(unsigned=True), default=0)
    created_at = Column(DateTime, default=datetime.now())
    is_valid = Column(Boolean, default=True)

class UserAddress(Base):
    __tablename__ = "user_address"
    id = Column(Integer, primary_key=True)
    area = Column(String(256), nullable=False)
    phone_no = Column(CHAR(11))
    remark = Column(String(512))
    is_valid = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id)) # foreign key
    user = relationship('User', backref='addresses')

class UserProfile(Base):
    __tablename__ = "user_profile"
    id = Column(Integer, primary_key=True)
    hobby = Column(String(255))
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship('User', backref='profile', uselist=False)

# create table
#Base.metadata.create_all(bind=engine)

user_obj = User(user_name='天才', password='123456', age=40)
profile = UserProfile(user=user_obj)
# list
user_obj.addresses.append(UserAddress(user=user_obj, area='地址'))

# connection with database
# session = Session(bind=engine)
# session.add(user_obj) # insert one data, if a batch, insert a list
# session.commit() # have to commit
# session.close()

with Session(engine) as session:
    result = session.get(User, 1) # returns an ORM object
    print(result.user_name)

    result = session.get(User, {"id" : 1})
    print(result.user_name)

    result = session.execute(select(User).where(User.id==1)).fetchone() # returns a tuple
    print(result[0].user_name)

    result = session.execute(select(User).where(User.id==1)).scalar_one_or_none()
    print(result.user_name)

    result = session.execute(select(User.id, User.user_name)).mappings() # return a list of dictionary
    for r in result:
        print(r)

    result = session.execute(select(User)).scalars() # returns a list of ORM objects
    for r in result:
        print(r.user_name)

class Student(Base):
    __table__ = Table("school_student_info", Base.metadata, autoload_with=engine)

class Course(Base):
    __table__ = Table("school_course_info", Base.metadata, autoload_with=engine)

class StudentGrade(Base):
    __table__ = Table("school_student_grade", Base.metadata, autoload_with=engine)

with Session(engine) as session:
    sql1 = select(Student).where(Student.age > 12)
    sql2 = select(Student).where(Student.age.between(9, 12)) # include 9 and 12
    sql3 = select(Student).where(Student.age.is_(None))
    sql4 = select(Student).where(Student.age.in_((9, 12)))
    sql5 = select(Student).where(or_(Student.age == 9, Student.age == 12)) # same as sql4
    sql6 = select(Student).where(Student.stu_name.like('李%'))
    sql7 = select(Student).where(Student.stu_name.startswith('李')) # same as sql6
    sql8 = select(Student).where(Student.stu_name.like('李_'))
    sql9 = select(Student).where(Student.stu_name.like('%雪%'))
    sql10 = select(Student).where(Student.stu_name.contains('雪'))
    sql11 = select(Student).where(and_(Student.age.between(9, 12), Student.sex == '女'))
    sql12 = select(Student).where(Student.age.between(9, 12)).where(Student.sex == '女') # same as sql11
    sql13 = select(Student).where(or_(and_(Student.age > 12, Student.sex == '男'), and_(Student.age < 9, Student.sex == '女')))
    sql14 = select(Student).where(and_(Student.stu_name.like('李%'), Student.sex == '女', Student.age.is_not(None)))

    result = session.execute(sql14).scalars()
    for r in result:
        print(r.id, r.stu_name, r.sex, r.age)

    sql15 = select(func.count().label('count')).select_from(Student)
    sql16 = select(func.max(StudentGrade.score).label('max_score'),
                   func.min(StudentGrade.score).label('min_score')).where(StudentGrade.course_id == 1)
    sql17 = select(func.avg(StudentGrade.score).label('avg_score')).where(StudentGrade.course_id == 1)
    sql18 = select(func.sum(StudentGrade.score).label('total_score')).where(StudentGrade.student_id == 5)

    result = session.execute(sql18).mappings().one()
    print(result)

    user_obj = session.get(User, 1)
    print(user_obj.user_name)
    for item in user_obj.addresses:
        print(item.id, item.area)

    add_obj = session.get(UserAddress, 2)
    print(add_obj.id, add_obj.area)
    print(add_obj.user.id, add_obj.user.user_name)

    sql19 = select(Student, Course, StudentGrade).where(Student.id == StudentGrade.student_id) \
            .where(Course.id == StudentGrade.course_id)
    result = session.execute(sql19).mappings().all()

    for item in result:
        print(item.Student.stu_no, item.Student.stu_name, item.Course.course_name, item.StudentGrade.score)

    sql20 = select(Student.address).distinct()

    result = session.execute(sql20).scalars()
    for item in result:
        print(item)

    sql21 = select(Student.class_name, func.count().label('count')).group_by(Student.class_name)
    sql22 = select(Student.class_name, Student.sex, func.count().label('count')).group_by(Student.class_name, Student.sex)
    sql23 = select(StudentGrade.student_id, func.count().label('course_count')).where(StudentGrade.score >= 60) \
        .group_by(StudentGrade.student_id).having(func.count() == 3)
    sql24 = select(Student.stu_name, StudentGrade.score).where(StudentGrade.student_id == Student.id) \
        .where(StudentGrade.course_id == Course.id) \
        .where(Course.course_name == '语文').order_by(StudentGrade.score.desc())
    sql25 = select(Student.stu_name, func.sum(StudentGrade.score).label('total')) \
        .where(StudentGrade.student_id == Student.id).group_by(Student.id) \
        .order_by(desc('total')).limit(10) # top 10
    sql26 = select(Student.stu_name, func.sum(StudentGrade.score).label('total')) \
        .where(StudentGrade.student_id == Student.id).group_by(Student.id) \
        .order_by(desc('total')).offset(10).limit(10) # top 11 ~ 20

    result = session.execute(sql26).mappings()
    for item in result:
        print(item)

    stu_obj = session.get(Student, 2)
    stu_obj.phone_no = '15812133933'
    session.add(stu_obj)
    session.commit()

    sql27 = update(Student).where(Student.stu_name.startswith('李')).values(age=Student.age + 1)\
        .execution_options(synchronize_session="fetch")
    result = session.execute(sql27)
    session.commit()
    print(result.rowcount) # affected rows

    stu_obj = session.get(Student, 51)
    session.delete(stu_obj)
    session.commit()

    sql28 = delete(StudentGrade).where(StudentGrade.score < 60)
    result = session.execute(sql28)
    session.commit()
    print(result.rowcount)