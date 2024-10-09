import redis, json

pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    db=1,
    max_connections=20
)
connection = redis.Redis(connection_pool=pool)

# string
connection.set('user1', 'Amy')
user1 = connection.get('user1').decode() # decode binary result
print(user1) #result will be none if key does not exist

# removed after 10s
connection.set('user2', 'Tom', ex=10)
d = {'user3':'Bob', 'user4':'Kai'}
connection.mset(d) # set several keys
print(connection.mget(['user1', 'user2', 'user4']))

connection.incr('age')
print(connection.get('age'))
print(connection.delete('user1'))

def register(username, password, nickname):
    key = f'user:{username}'
    user_info = {
        'username':username,
        'password':password,
        'nickname':nickname
    }

    value = json.dumps(user_info)
    connection.set(key, value)

register('lili', 12144, '丽丽')
values = json.loads(connection.get('user:lili'))
print(values['username'])

# list
t = ['Amy', 'Bob']
connection.lpush('user_list', *t)
connection.rpush('user_list', 'Jack')
print(connection.lrange('user_list', 0, -1))
result = connection.lpop('user_list')
print(connection.llen('user_list'))

# hash
connection.hset('stu:0001', 'name', 'Lily')
print(connection.hexists('stu:0001', 'name'))
print(connection.hsetnx('stu:0002', 'name', 'Jack'))
user_info = {
    'username':'Bob',
    'password':123456,
    'age':100
}
connection.hset('stu:0003', mapping=user_info)
print(connection.hkeys('stu:0003'))
connection.hdel('stu:0003', 'age')
print(connection.hlen('stu:0003'))
connection.delete('stu:0004')
print(connection.hmget('stu:0003', 'password', 'username'))

# set
connection.sadd('zoo1', 'dog', 'cat')
print(connection.smembers('zoo1'))
connection.srem('zoo1', 'dog')
connection.sadd('zoo2', 'cat', 'monkey')
print(connection.sunion('zoo1', 'zoo2'))
print(connection.sinter('zoo1', 'zoo2'))


# zset (ordered set)
grade = {'Jack':100, 'Tom':90, 'Jason':0}
connection.zadd('grade', grade)
print(connection.zcard('grade'))
print(connection.zcount('grade', 80, 100))
connection.zrem('grade', 'Jack')
print(connection.zscore('grade', 'Jason'))
print(connection.zrange('grade', 0, -1))

connection.close() # put it back to connection pool