FROM python:alpine

# defining the directory
WORKDIR /app
#copy the contents to the working dir
COPY . .

#running all the dependencies
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5000

# command to start the container
CMD ["python","run.py"]