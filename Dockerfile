FROM python:3.10.10-bullseye

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . ./k8s
WORKDIR /k8s
EXPOSE 5000
CMD [ "python3", "app.py"]
