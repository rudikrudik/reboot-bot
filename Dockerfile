ARG MY_VARIABLE

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY /src /app

# Install dependencies (if any)
# Note: You might need to install build dependencies before pip install if packages require compilation
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
#RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends gnupg
RUN gpg --quiet --batch --yes --decrypt --passphrase=${MY_VARIABLE} \
--output ip_list.py ip_list.py.gpg

# Run the application
CMD ["python", "main.py"]