FROM python:3.9-slim

COPY entrypoint.sh /entrypoint.sh
COPY build_code_reference.py /build_code_reference.py

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]