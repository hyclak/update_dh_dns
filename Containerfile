FROM python:3-slim

COPY update_dh_dns.py ./
CMD ["python3", "./update_dh_dns.py"]
