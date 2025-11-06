FROM python:3.12-slim

ARG DECRYPT_PASSPHRASE
ARG TOKEN
ENV TOKEN=$TOKEN
ARG STAGE
ENV STAGE=$STAGE
ARG TZ
ENV TZ=$TZ

WORKDIR /app
COPY /src /app
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends gnupg tzdata
RUN gpg --quiet --batch --yes --decrypt --passphrase=$DECRYPT_PASSPHRASE \
    --output kasse.py kasse.py.gpg \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD ["python", "main.py"]