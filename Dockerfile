FROM python:3.12-slim

ARG DECRYPT_PASSPHRASE
ARG TOKEN
ENV TOKEN=$TOKEN

# Set working directory
WORKDIR /app

# Copy application files
COPY /src /app

# Install dependencies (if any)
# Note: You might need to install build dependencies before pip install if packages require compilation
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
#RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends gnupg
RUN gpg --quiet --batch --yes --decrypt --passphrase=$DECRYPT_PASSPHRASE \
--output /app/ip_list.py /app/ip_list.py.gpg

# Run the application
CMD ["python", "main.py"]