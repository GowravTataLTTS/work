# Use the official Python image as the base
FROM python:3.9

# Set the working directory in the container
WORKDIR .

# Copy the app folder to the working directory
COPY . .

# Install the required dependencies
RUN pip install -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Set the entrypoint command
CMD ["python", "run.py"]