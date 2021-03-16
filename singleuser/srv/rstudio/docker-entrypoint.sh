#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

if [ "$(which "$1")" = "/usr/local/bin/start-singleuser.sh" ]; then
#    usermod --shell /bin/bash jovyan
    if [ ! -f /home/jovyan/.jupyter/jupyter_notebook_config.py ]; then
       mkdir -p /home/jovyan/.jupyter
       cp /srv/jupyter_notebook_config.py /home/jovyan/.jupyter/
       cp /srv/rstudio*.conf /home/jovyan/.jupyter/
       sed -i "s/USER/${USER}/" /home/jovyan/.jupyter/rstudio.conf
       chown -R 1001:100 /home/jovyan/.jupyter
    fi 
    if [ ! -f /home/jovyan/.bashrc ]; then
       cp /srv/.bashrc /home/jovyan/.bashrc
       ln -s /home/jovyan/.bashrc /home/jovyan/.profile
       chown -R 1001:100 /home/jovyan/.bashrc /home/jovyan/.profile
    fi
fi

# Run the command provided
exec "$@"
