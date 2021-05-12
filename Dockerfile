FROM python:3.8

COPY ./src ./
RUN pip install -r ./requirements.txt

RUN chmod +x ./main.py
ENTRYPOINT ["python", "./main.py"]

#docker build -t connegp-tests .
#docker run connegp-tests --help
#docker run connegp-tests --url http://a25a8a2eda9464b7fb3931bf12de441b-1975690911.ap-southeast-2.elb.amazonaws.com/collections/SA1s/items
