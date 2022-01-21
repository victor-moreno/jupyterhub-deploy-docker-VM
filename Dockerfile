# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

ARG HUB_VERSION
FROM jupyterhub/jupyterhub-onbuild:$HUB_VERSION

# Install dockerspawner & tools
RUN pip3 install --no-cache-dir dockerspawner \
                                jupyterhub-idle-culler \
                                PyJWT \
                                pyyaml
# authenticators
RUN pip3 install    oauthenticator \
                    jupyterhub-nativeauthenticator
# change templates/native-login.html to allow github
RUN sed -i 's+</a></p>+</a></p></div><div style="padding-top: 25px;"><p>Login with <a href="{{ base_url }}github/oauth_login">GitHub</a></p>+' /usr/local/lib/python3.8/dist-packages/nativeauthenticator/templates/native-login.html

