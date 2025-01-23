# FROM python:latest

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# WORKDIR /app

# RUN apt-get update

# RUN pip3 install --upgrade pip

# RUN pip3 install -U pipenv

# COPY . /app/

# RUN pipenv install

# EXPOSE 8000

# ENTRYPOINT ["./entrypoint.sh"]

# Use a specific Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (e.g., for PostgreSQL or other packages)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install virtualenv
RUN pip install --no-cache-dir --upgrade pip virtualenv

COPY . /app/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
