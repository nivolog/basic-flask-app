FROM python:3.8-slim-buster
ADD . /code
WORKDIR /code
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD python3 EasyPlan.py