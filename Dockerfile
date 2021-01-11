FROM python:3.7
# add project
ADD ./web /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt .



##run flask
##Developer use
#CMD ["python"]

#Production use
CMD ["python", "app.py"]
