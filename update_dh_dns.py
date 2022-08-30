#!/usr/bin/env python3

import os
import re
import sys
from urllib.request import urlopen

def get_current_ip():
    ip = urlopen('https://api.ipify.org').read().decode('utf8')
    return str(ip)

def update_dreamhost_a_record(key, record, new_ip):
    records = urlopen(f"https://api.dreamhost.com/?key={key}&cmd=dns-list_records").read().decode('utf8')
    # print(records)
    record_match = rf"{re.escape(record)}\s+A\s+(.\d+\.\d+\.\d+\.\d+)\s+"
    if not re.search(record_match, records):
        print("No current record found. Adding Record.")
    else: 
        current_record_ip = re.split(record_match, records)[1]
        if current_record_ip == new_ip:
            print("IP record is already correct, no action taken.")
            return
        else:
            result = urlopen(f"https://api.dreamhost.com/?key={key}&cmd=dns-remove_record&record={record}&type=A&value={current_record_ip}").read().decode('utf8')
            print(f"Removing old IP ({current_record_ip}): {result}")

    # Finally, add Record
    result = urlopen(f"https://api.dreamhost.com/?key={key}&cmd=dns-add_record&record={record}&type=A&value={new_ip}").read().decode('utf8')
    print(f"Adding new IP ({new_ip}): {result}")

def main():
    try:
        apikey = os.environ['DH_API_KEY']
    except:
        print("Please define the DH_API_KEY environment variable with a valid Dreamhost API Key.")
        exit(1)

    try:
        record = os.environ['DH_HOSTNAME']
    except:
        print("Please define the DH_HOSTNAME environment variable with a valid hostname.")
        exit(1)

    external_ip = get_current_ip()
    print(f"Updating IP to {external_ip}")

    update_dreamhost_a_record(apikey, record, external_ip)

if __name__ == '__main__':
    sys.exit(main())