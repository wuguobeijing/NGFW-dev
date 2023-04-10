import json
import subprocess
import time
from tkinter import messagebox

import yaml
import redis

host = '192.168.0.100'
r = redis.Redis(host=host, port=6379, db=1)
# print(r.hget('whitelist', 'IPs'))
key_list = r.keys()
flows_key_list = []
rules_params_yaml_path = "/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/cache/rules_append.yaml"
rules_list_yaml_path = "/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/cache/rules_list.yaml"


def parse_rule(content_json):
    saddr = content_json['saddr']
    daddr = content_json['daddr']
    sport = content_json['sport']
    dport = content_json['dport']
    proto = content_json['proto']
    return [saddr, daddr, sport, dport, proto]


def ssh_query_ip_tables(selected_device, rules_content):
    ssh_content = "ssh %s \'%s\'" % (selected_device, rules_content)
    p = subprocess.Popen(ssh_content, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = p.communicate()
    if err is not None:
        messagebox.showwarning("insert rules failed!", "try again later")
    else:
        if out is not None:
            print(out)


while True:
    with open(rules_params_yaml_path, 'r', encoding="utf-8") as f:
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
    with open(rules_list_yaml_path, 'r', encoding="utf-8") as f:
        rule_list = yaml.load(f, Loader=yaml.FullLoader)
        rules = rule_list['iptables_rules']
        if rules is None:
            rules = []
    for key in key_list:
        if '_flows' in str(key):
            if key not in flows_key_list:
                for item in r.hgetall(key):
                    firewall_content = ''
                    str_item = str(item, 'utf-8')
                    content_json = json.loads(str(r.hget(key, str_item), 'utf-8'))
                    if content_json['label'] == 'malicious':
                        parsed_rule_params = parse_rule(content_json)
                        if content_json['module_labels'] == 'C&C':
                            match_params = [parsed_rule_params[4], parsed_rule_params[0],
                                            parsed_rule_params[1], parsed_rule_params[3]]
                            if match_params not in CC_list:
                                firewall_content = "sudo iptables -A INPUT -p %s -s %s -d %s --dport %s -m comment " \
                                                   "--comment \"CC\" -j DROP" \
                                                   % (match_params[0], match_params[1], match_params[2],
                                                      match_params[3])
                                CC_list.append(match_params)
                        elif content_json['module_labels'] == 'DDoS':
                            match_params = [parsed_rule_params[4], parsed_rule_params[0],
                                            parsed_rule_params[2], parsed_rule_params[1]]
                            if match_params not in DDoS_list:
                                firewall_content = "sudo iptables -A INPUT -p %s -s %s --sport %s -d %s -m comment " \
                                                   "--comment \"DDoS\" -j DROP" \
                                                   % (match_params[0], match_params[1], match_params[2],
                                                      match_params[3])
                                DDoS_list.append(match_params)
                        elif content_json['module_labels'] == 'msf':
                            match_params = [parsed_rule_params[4], parsed_rule_params[0],
                                            parsed_rule_params[1], parsed_rule_params[3]]
                            if match_params not in msf_list:
                                firewall_content = "sudo iptables -A INPUT -p %s -s %s -d %s --dport %s -m comment " \
                                                   "--comment \"msf\" -j DROP" \
                                                   % (match_params[0], match_params[1], match_params[2],
                                                      match_params[3])
                                msf_list.append(match_params)
                        elif content_json['module_labels'] == 'nmap':
                            match_params = [parsed_rule_params[4], parsed_rule_params[0],
                                            parsed_rule_params[2], parsed_rule_params[1]]
                            if match_params not in nmap_list:
                                firewall_content = "sudo iptables -A INPUT -p %s -s %s --sport %s -d %s -m comment " \
                                                   "--comment \"nmap\" -j DROP" \
                                                   % (match_params[0], match_params[1], match_params[2],
                                                      match_params[3])
                                nmap_list.append(match_params)
                        if firewall_content != '':
                            rules.append(firewall_content)
                            ssh_query_ip_tables(host, firewall_content)
                flows_key_list.append(key)
    new_data = {
        'CC_list': CC_list,
        'DDoS_list': DDoS_list,
        'nmap_list': nmap_list,
        'msf_list': msf_list,
    }
    all_rules = {
        'iptables_rules': rules
    }
    print(rules)
    # note rules params
    f = open(rules_params_yaml_path, "w")
    yaml.dump(new_data, f)
    f.close()
    # note iptables rules
    f = open(rules_list_yaml_path, "w")
    yaml.dump(all_rules, f)
    f.close()
    time.sleep(600)
