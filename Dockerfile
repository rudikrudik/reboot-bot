FROM python:3.12-slim

ARG DECRYPT_PASSPHRASE
ARG TOKEN
ENV TOKEN=$TOKEN

RUN echo "Value of TOKEN: $TOKEN"

WORKDIR /app
COPY /src /app
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends gnupg
RUN gpg --quiet --batch --yes --decrypt --passphrase=$DECRYPT_PASSPHRASE \
--output /app/kasse.py /app/kasse.py.gpg

CMD ["python", "main.py"]