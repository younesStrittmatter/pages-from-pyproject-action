FROM python:3.9-slim

COPY entrypoint.sh /entrypoint.sh
COPY pages_from_pyproject.py /pages_from_pyproject.py

RUN pip install toml 
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]