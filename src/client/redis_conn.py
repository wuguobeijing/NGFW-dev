import json
import time

import redis

r = redis.Redis(host='192.168.0.100', port=6379, db=1)
# print(r.hget('whitelist', 'IPs'))
key_list = r.keys()
flows_key_list = []
while True:
    for key in key_list:
        if '_flows' in str(key):
            if key not in flows_key_list:
                for item in r.hgetall(key):
                    str_item = str(item, 'utf-8')
                    print(r.hget(key, str_item))
                    # print(json.loads(str_item))
                    print('=='*10+'\n')
                flows_key_list.append(key)

    time.sleep(600)
# for target_key in flows_key_list:
#     print(r.hgetall(target_key))
