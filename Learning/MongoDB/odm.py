from mongoengine import connect, Document, EmbeddedDocument, Q
from enum import Enum
from mongoengine.fields import StringField, IntField, EnumField, ListField, EmbeddedDocumentField

# connect to database
connect(db='test')

class SexChoices(Enum):
    MEN = '男'
    WOMEN = '女'

class CourseGrade(EmbeddedDocument):
    course_name = StringField(max_length=64, required=True)
    teacher = StringField(max_length=16)
    score = IntField(min_value=0, required=True)

class Student(Document):
    stu_no = IntField(required=True, unique=True)
    stu_name = StringField(required=True, max_length=16)
    sex = EnumField(enum=SexChoices)
    class_name = StringField(max_length=10)
    address = StringField(max_length=255)
    phone_no = StringField(max_length=11)
    age = IntField(min_value=0, max_value=100)
    # document in document
    grades = ListField(EmbeddedDocumentField(CourseGrade))

    meta = {
        # specify collection
        'collection':'students'
    }


result = Student.objects.first()
print(result.stu_no)

result = Student.objects.get(stu_no=1001)
print(result.stu_name)

result = Student.objects(age__gt=12)
for item in result:
    print(item.stu_no, item.age)

result = Student.objects.filter(stu_name__startswith='李')
for item in result:
    print(item.stu_name, item.age)

result = Student.objects.filter(Q(stu_name__startswith='李') & Q(age=12))
for item in result:
    print(item.stu_name, item.age)

result = Student.objects.filter(Q(sex=SexChoices.MEN, age__gt=12) | Q(age__lt=9, sex=SexChoices.WOMEN))
result = result.order_by('-age') # - : DESC, default + : ASC
result = result.skip(1).limit(2)
for item in result:
    print(item.stu_name, item.age)
print(result.count())

grade1 = CourseGrade(course_name='语文', score=100)
grades = [grade1]
stu_obj = Student(stu_no=2002, stu_name='王三小')
stu_obj.grades = grades
stu_obj.validate() # check whether it satisfies the requirement
stu_obj.save() # insert this document

result = Student.objects.filter(stu_no=2001)
result = result.update_one(stu_name='王二', phone_no='11111111111')
result = result.update_one(unset__phone_no=True) # remove phone_no
result = result.update_one(inc__stu_no=2)
print(result)

result = Student.objects.filter(stu_no=2002).delete()
print(result)
