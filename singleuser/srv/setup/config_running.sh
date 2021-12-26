#!/bin/bash

# prevent /usr/local/bin/start.sh deleting NB_USER
sed -i 's/userdel/# userdel/' /usr/local/bin/start.sh
sed -i 's/useradd/# useradd/' /usr/local/bin/start.sh
sed -i "s/jovyan/$NB_USER/g" /etc/passwd
sed -i "s/1000:100/$NB_UID:$NB_GID/" /etc/passwd

[[ -f /tmp/group ]] && cp /tmp/group /etc/group 

export USER=$NB_USER
export HOME=/home/$NB_USER


if [ ! -f ${HOME}/.jupyter/jupyter_notebook_config.py ]; then
    mkdir -p ${HOME}/.jupyter
    cp /srv/jupyter_notebook_config.py ${HOME}/.jupyter/
    chown -R ${NB_UID}:${NB_GID} ${HOME}/.jupyter
fi 
if [ ! -f ${HOME}/.jupyter/services.yaml ]; then
    mkdir -p ${HOME}/.jupyter
    cp /srv/services.yaml ${HOME}/.jupyter/
    chown -R ${NB_UID}:${NB_GID} ${HOME}/.jupyter
    sed -i "s/jovyan/$NB_USER/" ${HOME}/.jupyter/services.yaml
fi 
if [ ! -f ${HOME}/.bashrc ]; then
    cp /srv/.bashrc ${HOME}/.bashrc
    ln -s ${HOME}/.bashrc ${HOME}/.profile
    chown -R ${NB_UID}:${NB_GID} ${HOME}/.bashrc ${HOME}/.profile
fi

# .Rprofile
echo -e "Sys.setenv('RVER'='${RVER}')\n.libPaths( paste0('/library/',Sys.getenv('RVER')));\noptions(repos = c(REPO_NAME = 'https://packagemanager.rstudio.com/all/latest'))" > ${HOME}/.Rprofile
chown -R ${NB_UID}:${NB_GID} ${HOME}/.Rprofile
export R_LIBS_USER=/library/${RVER}

if [ "$JUPYTER_IMAGE_SPEC" == "jupyter-vnc" ] && [ ! -f ${HOME}/Desktop/labelimg.desktop ]; then
    export RESOURCES_LOC=$(python -c "import jupyter_labelimg_proxy as pkg; print(pkg.__path__[0])")/resources
    mkdir -p ${HOME}/Desktop ${HOME}/.icons ${HOME}/.local/share/applications
    cp ${RESOURCES_LOC}/labelimg.desktop ${HOME}/Desktop/
    cp ${RESOURCES_LOC}/labelimg.desktop ${HOME}/.local/share/applications
    ln -s ${RESOURCES_LOC}/labelimg.png ${HOME}/.icons/labelimg.png
    touch ${HOME}/.Xauthority
    chown ${NB_UID}:${NB_GID} -R ${HOME}/.local ${HOME}/.config ${HOME}/.icons ${HOME}/Desktop ${HOME}/.Xauthority
fi



