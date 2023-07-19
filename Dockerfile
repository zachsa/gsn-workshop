# Use Python 3.10 as the base image
FROM python:3.10.6

# Set the working directory in the container
WORKDIR /app

# Copy the script.py and requirements.txt files into the container
COPY script.py requirements.txt /app/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libxml2-dev libxslt1-dev zlib1g-dev \
    libsasl2-dev libldap2-dev

# Install the project dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set the entry point for the container
CMD [ "python", "script.py" ]
