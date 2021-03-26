# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

ARG JUPYTERHUB_VERSION
FROM jupyterhub/jupyterhub-onbuild:$JUPYTERHUB_VERSION

# postgress
RUN apt-get update && apt-get install -y libpq-dev git \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && /usr/bin/python3 -m pip install --upgrade pip \
    && pip3 install --no-cache-dir psycopg2-binary

# # Copy TLS certificate and key
# ENV SSL_CERT /srv/jupyterhub/secrets/jupyterhub.crt
# ENV SSL_KEY /srv/jupyterhub/secrets/jupyterhub.key
# COPY ./secrets/*.crt $SSL_CERT
# COPY ./secrets/*.key $SSL_KEY
# RUN chmod 700 /srv/jupyterhub/secrets && \
#     chmod 600 /srv/jupyterhub/secrets/*

# Install dockerspawner, oauth
RUN pip3 install --no-cache-dir dockerspawner oauthenticator \
    jupyterhub-idle-culler PyJWT 

# RUN cd /tmp && git clone https://github.com/jupyterhub/nativeauthenticator.git && pip3 install /tmp/nativeauthenticator && rm -rf /tmp/nativeauthenticator
COPY native /tmp/native
RUN cd /tmp/native && pip3 install . && cd / && rm -rf /tmp/native

