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
RUN pip3 install /tmp/native && rm -rf /tmp/native

# RUN pip3 install jupyterhub-nativeauthenticator
# RUN sed -i 's+</a></p>+</a></p></div><div style="padding-top: 25px;"><p>Login with <a href="{{ base_url }}github/oauth_login">GitHub</a> or <a href="{{ base_url }}google/oauth_login">Google</a></p>+' /usr/local/lib/python3.8/dist-packages/nativeauthenticator/templates/native-login.html

