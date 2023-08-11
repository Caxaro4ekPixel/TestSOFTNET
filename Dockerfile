FROM ubuntu:latest
LABEL authors="Zavadski"
COPY . /home/TestZavadski
WORKDIR /home/TestZavadski
RUN apt-get update && apt-get install -y python3 python3-pip python3-dev build-essential
RUN git clone https://github.com/Caxaro4ekPixel/TestSOFTNET.git
RUN pip3 install -r requirements.txt
RUN flask db init
RUN flask db migrate
RUN flask db upgrade
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
ENTRYPOINT ["top", "-b"]