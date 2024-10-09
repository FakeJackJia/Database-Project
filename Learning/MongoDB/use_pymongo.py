from pymongo import MongoClient, DESCENDING
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
print(client)

for item in client.list_databases():
    print(item)

# access to specific database
db = client.test
print(db)

for collection in db.list_collection_names():
    print(collection)

# CRUD
doc = {
    'username':'丽丽',
    'age':23
}
result = db.users.insert_one(doc)
print(result)

doc1 = {
    'username':'丽丽1',
    'age':24
}
doc2 = {
    'username':'丽丽2',
    'age':25
}
doc_list = [doc1, doc2]
result = db.users.insert_many(doc_list)
print(len(result.inserted_ids))

user_obj = db.users.find_one() # returns a dictionary
print(user_obj)

user_obj = db.users.find_one({'_id':ObjectId('67037c34e6993ce90901fef4')})
print(user_obj)

result = db.students.find({'age':{'$gt':12}}, {'stu_no':1, 'age':1})
for item in result:
    print(item)

result = db.students.find().skip(10).limit(4)
for item in result:
    print(item)

result = db.grades.find({'grade.course_name':'语文'}).sort('grade.score', DESCENDING)
for item in result:
    print(item)

result = db.grades.find({'grade.course_name':'语文'}).sort([('age', DESCENDING), ('grade.score', DESCENDING)])
for item in result:
    print(item)

result = db.students.count_documents({})
print(result)

result = db.grades.aggregate([
    {'$match':{'grade.score':{'$gte':60}}},
    {'$group':{'_id':'$stu_no', 'total':{'$sum':1}}},
    {'$match':{'total':{'$eq':3}}}
])
for item in result:
    print(item)

result = db.users.update_one({}, {'$set':{'age':20}})
print(result.modified_count)

result = db.users.replace_one({'username':'丽丽'}, {'username':'莉莉'})

result = db.users.update_many({'username':'丽丽'}, {'$set': {'age':50}})

result = db.users.find_one_and_update({}, {'$set':{'age':100}}) # returns a dictionary of doc

result = db.users.delete_one({'username':'丽丽'})
print(result.deleted_count)

result = db.users.find_one_and_delete({'username':'丽丽1'})
print(result)

result = db.users.delete_many({'username':'丽丽2'})
print(result.deleted_count)