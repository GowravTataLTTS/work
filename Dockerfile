FROM python:3.6.1-alpine

# defining the directory
WORKDIR /work
#copy the contents to the working dir
COPY . /work

#running all the dependencies
RUN pip install --upgrade pip

RUN pip install -r requirements.txt


ENTRYPOINT ["python"]
# command to start the container
CMD ["run.py"]