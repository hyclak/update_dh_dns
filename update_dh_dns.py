#!/usr/bin/env python3
""" Update DreamHost DNS Entry from Environment Variables """

import os
import re
import sys
from datetime import datetime
from urllib.request import urlopen

APIURL = "https://api.dreamhost.com"

def get_current_ip():
    """ Get external IP address from api.ipify.org """
    with urlopen('https://api.ipify.org') as result:
        current_ip = result.read().decode('utf8')
        return str(current_ip)

def update_dreamhost_a_record(key, record, new_ip):
    """ Update A record via DreamHost DNS API """
    records_url = f"{APIURL}/?key={key}&cmd=dns-list_records"
    with urlopen(records_url) as result:
        records = result.read().decode('utf8')
        record_match = rf"{re.escape(record)}\s+A\s+(.\d+\.\d+\.\d+\.\d+)\s+"
        if not re.search(record_match, records):
            print("No current record found. Adding Record.")
        else:
            current_record_ip = re.split(record_match, records)[1]
            if current_record_ip == new_ip:
                print("IP record is already correct, no action taken.")
                return

            # Remove existing record
            remove_url = f"{APIURL}/?key={key}&cmd=dns-remove_record&record={record}&type=A&value={current_record_ip}" # pylint: disable=C0301
            with urlopen(remove_url) as result:
                print(f"Removing old IP ({current_record_ip}): {result.read().decode('utf8')}")

        # Finally, add Record
        add_url = f"{APIURL}/?key={key}&cmd=dns-add_record&record={record}&type=A&value={new_ip}"
        with urlopen(add_url) as result:
            print(f"Adding new IP ({new_ip}): {result.read().decode('utf8')}")

def main():
    """ Initiate Update """
    try:
        apikey = os.environ['DH_API_KEY']
    except KeyError():
        print("Please define the DH_API_KEY environment variable with a valid Dreamhost API Key.")
        sys.exit(1)

    try:
        record = os.environ['DH_HOSTNAME']
    except KeyError():
        print("Please define the DH_HOSTNAME environment variable with a valid hostname.")
        sys.exit(1)

    print(f"Validating IP at {datetime.now.strftime('%m/%d/%Y %H:%M:%S')}")

    external_ip = get_current_ip()
    print(f"Updating IP to {external_ip}")

    update_dreamhost_a_record(apikey, record, external_ip)

if __name__ == '__main__':
    sys.exit(main())
