FROM python:3.7.5

WORKDIR /code

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD . .

CMD ["python", "main.py"]
