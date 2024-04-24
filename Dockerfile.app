FROM python:3.8-slim

#LABEL version="1.0"

RUN apk add --no-cache mariadb-dev build-base
WORKDIR /events

COPY requirements.txt requirements.txt
RUN pip install --no

#RUN pip install -r requirements.txt

COPY . .

# EXPOSE 8080/tcp

# VOLUME /events

CMD ["python", "app.py"]