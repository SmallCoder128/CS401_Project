 FROM python:3.11

 RUN mkdir /app
 WORKDIR /app
 COPY requirements.txt /app/requirements.txt
 RUN pip install -r /app/requirements.txt
 COPY . /app

 EXPOSE 5000

 ENTRYPOINT ["python"]

 CMD ["api_front.py"]   