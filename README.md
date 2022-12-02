# Description

Container executes the `update_dh_dns.py` script to update the requested A record via the DreamHost DNS API with external IP retrieved from [ipify.com](https://api.ipify.com)

Due to how DreamHost's DNS API works, the following steps are taken:

1. If the A record already exists and is correct, nothing is done.
2. If the A record already exists and is incorrect, the current A record is removed and the new recored is created.
3. If the A record does not already exist, the new record is created.

## Prerequisites

1. Create an [API Key](https://help.dreamhost.com/hc/en-us/articles/4407354972692) with permissions to the dns-* functions. 

## Runtime

1. `DH_API_KEY` Environment Variable containing the API Key.
2. `DH_HOSTNAME` Environment Variable containing the hostname that should be updated.

