FROM python:3.10.0

WORKDIR /app

COPY . /app

RUN cd website

RUN pip install -r requirements.txt

CMD ["python", "website/main.py"]