# Use the official Python image as the base
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the app folder to the working directory
COPY app/ .

# Install the required dependencies
RUN pip install -r requirements.txt

# Set the entrypoint command
CMD ["python", "run.py"]