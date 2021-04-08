#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

if [ "$(which "$1")" = "/usr/local/bin/start-singleuser.sh" ]; then
#    usermod --shell /bin/bash jovyan
    if [ ! -f /home/jovyan/.jupyter/jupyter_notebook_config.py ]; then
       mkdir -p /home/jovyan/.jupyter
       cp /srv/jupyter_notebook_config.py /home/jovyan/.jupyter/
       chown -R 1001:100 /home/jovyan/.jupyter
    fi 
    if [ ! -f /home/jovyan/.jupyter/services.yaml ]; then
       mkdir -p /home/jovyan/.jupyter
       cp /srv/services.yaml /home/jovyan/.jupyter/
       chown -R 1001:100 /home/jovyan/.jupyter
    fi 
    if [ ! -f /home/jovyan/.bashrc ]; then
       cp /srv/.bashrc /home/jovyan/.bashrc
       ln -s /home/jovyan/.bashrc /home/jovyan/.profile
       chown -R 1001:100 /home/jovyan/.bashrc /home/jovyan/.profile
    fi
    if [ ! -f /home/jovyan/.Rprofile ]; then
       echo ".libPaths(paste0(R.home(), '/library'))" >> /home/jovyan/.Rprofile
       chown -R 1001:100 /home/jovyan/.Rprofile
    fi
    if [ "$JUPYTER_IMAGE_SPEC" == "jupyter-vnc" ] && [ ! -f ${HOME}/Desktop/labelimg.desktop ]; then
      export RESOURCES_LOC=$(python -c "import jupyter_labelimg_proxy as pkg; print(pkg.__path__[0])")/resources
      mkdir -p ${HOME}/Desktop ${HOME}/.icons ${HOME}/.local/share/applications
      cp ${RESOURCES_LOC}/labelimg.desktop ${HOME}/Desktop/
      cp ${RESOURCES_LOC}/labelimg.desktop ${HOME}/.local/share/applications
      ln -s ${RESOURCES_LOC}/labelimg.png ${HOME}/.icons/labelimg.png
      touch ${HOME}/.Xauthority
      chown 1001:100 -R ${HOME}/.local ${HOME}/.config ${HOME}/.icons ${HOME}/Desktop ${HOME}/.Xauthority
    fi
fi

# Run the command provided
exec "$@"
