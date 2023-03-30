import redis

r = redis.Redis(host='192.168.0.100', port=6379, db=1)
# print(r.hget('whitelist', 'IPs'))
key_list = r.keys()
flows_key_list = []
for key in key_list:
    if '_flows' in str(key):
        if key not in flows_key_list:
            flows_key_list.append(key)
for target_key in flows_key_list:
    print(r.hgetall(target_key))