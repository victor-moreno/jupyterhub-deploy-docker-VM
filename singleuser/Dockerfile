ARG DOCKER_NOTEBOOK_IMAGE
FROM $DOCKER_NOTEBOOK_IMAGE
ARG JUPYTERIMG_VERSION
#RUN python3 -m pip install --no-cache jupyterhub==$JUPYTERIMG_VERSION

RUN cd /tmp && git clone https://github.com/jupyterhub/jupyterhub && pip install /tmp/jupyterhub && rm -rf /tmp/jupyterhub

USER root
COPY nvtop /usr/local/bin/nvtop
RUN apt-get install -y mc

RUN conda install jupyter-server-proxy -c conda-forge && \
    jupyter labextension install @jupyterlab/server-proxy

# code server
RUN curl -fsSL https://code-server.dev/install.sh | sh

# rstudio
RUN apt-get update && apt-get -y --no-install-recommends install \
    liblzma-dev libbz2-dev libjpeg-dev libgsl-dev default-jdk libglpk-dev \
    libxml2-dev libssl-dev libcurl4-openssl-dev \
    procps psmisc lsb-release libclang-dev libpq5

#ENV RSTUDIO_VERSION=1.4.1106 not working
ENV RSTUDIO_VERSION=1.3.959
RUN cd /tmp && \
    wget https://download2.rstudio.org/server/xenial/amd64/rstudio-server-${RSTUDIO_VERSION}-amd64.deb && \
    dpkg -i rstudio-server-${RSTUDIO_VERSION}-amd64.deb && \
    rm rstudio-server-${RSTUDIO_VERSION}-amd64.deb && \
    echo "USER=jovyan" >> /etc/environment && \
    pip3 install --no-cache jupyter-rsession-proxy

USER jovyan

COPY srv /srv
ENTRYPOINT ["tini", "--", "/srv/docker-entrypoint.sh"]
CMD ["start-singleuser.sh"]
