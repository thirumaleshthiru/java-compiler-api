# Use an official Python runtime as a parent image
FROM python:3.8

# Install JDK and GCC
RUN apt-get update && \
    apt-get install -y default-jdk gcc

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080
EXPOSE 8080

# Run Gunicorn with 4 worker processes
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "app:app"]
