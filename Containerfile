FROM python:3

COPY update_dh_dns.py ./
CMD ["python3", "./update_dh_dns.py"]
