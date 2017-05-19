'''
This script is used to clean up the MHL file. It will use the regular expression to find out any duplications.
Since the MHL file is huge, it may took a long time to excute. (5-10 mins)
And there might be very few false positive. For example:

# 10.200.4.1 - 64 - Bragg static IPs
10.200.4.1|-|-|bragg01,bragg-01|-|device|-|runaround,isilon,1ss|Isilon NL400 - 1 Summer Street

The first line is just a comment. It's not duplication. But this script will take it as duplication. I don't wanna fix it
Bite me.
Author: Peter Chen
'''

import re

row = 0

def row_getter():
    global row
    return(row)

def row_setter_0():
    global row
    row = 0

def row_setter():
    global row
    row += 1

file_object = open('./master.host.listing.txt')
try:
    all_the_text = file_object.read()
finally:
    file_object.close()

pattern_ip = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.[1-9]{1,3}')     # I know it's ugly..bite me
all_ip = list(set(pattern_ip.findall(all_the_text)))    # Find all IPs and delete the repetitive ones, convert to list again
print(all_ip) # This is just for mornitoring the process and debugging.
fp_result = open('./MHL_check_result.txt','w')
for ip in all_ip:
    times = 0
    ip = ip.replace(".","\.",3)
    pattern_current_ip = re.compile('(.){0,20}' + str(ip) + '(\D)')
    with open('./master.host.listing.txt') as file_object:
        for line in file_object:
            row_setter()
            if (pattern_current_ip.match(line) != None):
                if times == 0:
                    temp = line
                    times += 1
                    continue
                elif "VLAN" in line:
                    continue
                elif "reserved for" in line:
                    times -= 1
                    continue
                else:
                    print(ip, " Duplicate Found ! ", line)
                    fp_result.write(temp + line + "\n")
                    times += 1
                    continue
        row_setter_0()
        temp = ""
fp_result.close()