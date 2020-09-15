FROM python:3.6-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /web
COPY . /web/
RUN apt update \
&& apt install gcc libsasl2-dev python-dev libldap2-dev libssl-dev -y \
&& apt clean
RUN pip install --upgrade pip
RUN pip install psycopg2-binary
RUN pip install pyOpenSSL
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "web/manage.py", "runserver", "0.0.0.0:8000"]
