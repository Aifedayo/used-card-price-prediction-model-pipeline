FROM python:3.12

WORKDIR /app

COPY  . /app

RUN apt update -y && apt install awscli -y

RUN pip install -r requirements.txt

CMD [ "python3", "app.py" ]
