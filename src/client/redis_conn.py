import json
import time
import yaml
import redis

r = redis.Redis(host='192.168.0.100', port=6379, db=1)
# print(r.hget('whitelist', 'IPs'))
key_list = r.keys()
flows_key_list = []
rules = []
yaml_path = "/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/cache/rules_append.yaml"


def parse_rule(content_json):
    saddr = content_json['saddr']
    daddr = content_json['daddr']
    sport = content_json['sport']
    dport = content_json['dport']
    proto = content_json['proto']
    return [saddr, daddr, sport, dport, proto]


while True:
    with open(yaml_path, 'r', encoding="utf-8") as f:
        values = yaml.load(f, Loader=yaml.FullLoader)
        CC_list = values['CC_list']
        DDoS_list = values['DDoS_list']
        nmap_list = values['nmap_list']
        msf_list = values['msf_list']
        if CC_list is None:
            CC_list = []
        if DDoS_list is None:
            DDoS_list = []
        if nmap_list is None:
            nmap_list = []
        if msf_list is None:
            msf_list = []
    for key in key_list:
        if '_flows' in str(key):
            if key not in flows_key_list:
                for item in r.hgetall(key):
                    firewall_content = ''
                    str_item = str(item, 'utf-8')
                    # print(r.hget(key, str_item))
                    # print(json.loads(str_item))
                    # print('=='*10+'\n')
                    # content_json = str(r.hget(key, str_item), 'utf-8')
                    content_json = json.loads(str(r.hget(key, str_item), 'utf-8'))
                    # print(content_json)
                    if content_json['label'] == 'malicious':
                        parsed_rule_params = parse_rule(content_json)
                        if content_json['module_labels'] == 'C&C':
                            match_params = [parsed_rule_params[4], parsed_rule_params[0],
                                            parsed_rule_params[1], parsed_rule_params[3]]
                            if match_params not in CC_list:
                                firewall_content = "sudo iptables -A INPUT -p %s --s %s --d %s --dport %s -j DROP" \
                                                   % (
                                                       match_params[0], match_params[1], match_params[2],
                                                       match_params[3])
                                CC_list.append(match_params)
                        elif content_json['module_labels'] == 'DDoS':
                            match_params = [parsed_rule_params[4], parsed_rule_params[0],
                                            parsed_rule_params[1], parsed_rule_params[2]]
                            if match_params not in DDoS_list:
                                firewall_content = "sudo iptables -A INPUT -p %s --s %s --d %s --sport %s -j DROP" \
                                                   % ( match_params[0], match_params[1], match_params[2],
                                                       match_params[3])
                                DDoS_list.append(match_params)
                        elif content_json['module_labels'] == 'msf':
                            match_params = [parsed_rule_params[4], parsed_rule_params[0],
                                            parsed_rule_params[1], parsed_rule_params[3]]
                            if match_params not in msf_list:
                                firewall_content = "sudo iptables -A INPUT -p %s --s %s --d %s --dport %s -j DROP" \
                                                   % ( match_params[0], match_params[1], match_params[2],
                                                       match_params[3])
                                msf_list.append(match_params)
                        elif content_json['module_labels'] == 'nmap':
                            match_params = [parsed_rule_params[4], parsed_rule_params[0],
                                            parsed_rule_params[1], parsed_rule_params[2]]
                            if match_params not in nmap_list:
                                firewall_content = "sudo iptables -A INPUT -p %s --s %s --d %s --sport %s -j DROP" \
                                                   % ( match_params[0], match_params[1], match_params[2],
                                                       match_params[3])
                                nmap_list.append(match_params)
                        if firewall_content != '':
                            rules.append(firewall_content)
                flows_key_list.append(key)
                print(rules)
    new_data = {
        'CC_list': CC_list,
        'DDoS_list': DDoS_list,
        'nmap_list': nmap_list,
        'msf_list': msf_list,
    }
    f = open(yaml_path, "w")
    yaml.dump(new_data, f)
    f.close()
    time.sleep(600)
# for target_key in flows_key_list:
#     print(r.hgetall(target_key))
