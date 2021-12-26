# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

ARG JUPYTERHUB_VERSION
FROM jupyterhub/jupyterhub-onbuild:$JUPYTERHUB_VERSION

# Install dockerspawner, oauth
RUN pip3 install --no-cache-dir dockerspawner oauthenticator \
    jupyterhub-idle-culler PyJWT pyyaml

# RUN cd /tmp && git clone https://github.com/jupyterhub/nativeauthenticator.git && pip3 install /tmp/nativeauthenticator && rm -rf /tmp/nativeauthenticator
# templates/native-login.html modified to allow github/google oauth
COPY native /tmp/native
RUN cd /tmp/native && pip3 install . --use-feature=in-tree-build && cd / && rm -rf /tmp/native

