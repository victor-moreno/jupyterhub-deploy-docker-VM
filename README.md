## adapted from: jupyterhub-deploy-docker 
[https://github.com/jupyterhub/jupyterhub-deploy-docker](https://github.com/jupyterhub/jupyterhub-deploy-docker) 

### changes to server

#### docker-compose.yaml
    -p 12000:443
    mount jupyterhub_config.py as volume

#### Dockerfile
    install: 
        dockerspawner 
        oauthenticator
        nativeauthenticator
        jupyterhub-idle-culler 
        PyJWT 

#### jupyterhub_config.py

    MyDockerSpawner: mounts volumes according to user
    MultiOAuthenticator: native, github, google

### client image 

#### jupyterhub_config.py:
    c.JupyterHub.base_url = '/jhub/'
    c.ServerProxy.servers

#### Dockerfile
    from:
        gpu-jupyter  cschranz/gpu-jupyter:v1.4_cuda-11.0_ubuntu-18.04
    install: 
        code server
        rstudio


### build jupyterhub server:
    make build

### build jupyterlab client:
    make image

### start
    docker-compose up -d

### services for jupyter_proxy
    in singleuser/srv:
    - jupyter-rserver_proxy (RStudio)
    - jupyter_codeserver_proxy (Code Server)
    - jupyter_deepzoom_proxy (openslide python)
    - jupyter_tensorboard_proxy (tensorboard)