import redis  # 导入redis 模块

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
print(r.get('name'))  # 取出键 name 对应的值
print(type(r.get('name')))  # 查看类型
