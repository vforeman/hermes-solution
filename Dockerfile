FROM python:2.7

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
# Copying the requirements for installation to take
# advantage of the caching.
COPY hermes/requirements.txt .
RUN pip install -r ./requirements.txt
