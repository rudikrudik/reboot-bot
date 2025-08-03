#!/bin/sh

gpg --quiet --batch --yes --decrypt --passphrase="$LARGE_SECRET_PASSPHRASE" \
--output ip_list.py ip_list.py.gpg