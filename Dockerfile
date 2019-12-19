FROM python:3.6.9-slim-stretch

COPY . /usr/local/bin/

CMD ["bammatcher_reporter.py"]