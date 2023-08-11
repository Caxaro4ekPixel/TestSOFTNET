FROM python:3.10
LABEL authors="Zavadski"
WORKDIR /home/TestZavadski
RUN apt-get update && apt-get install -y python3 python3-pip python3-dev build-essential
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN flask db init
RUN flask db migrate
RUN flask db upgrade
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
ENTRYPOINT ["top", "-b"]