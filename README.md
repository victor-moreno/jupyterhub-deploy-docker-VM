## adapted from: jupyterhub-deploy-docker 
[https://github.com/jupyterhub/jupyterhub-deploy-docker](https://github.com/jupyterhub/jupyterhub-deploy-docker) 

### changes to server

#### docker-compose.yaml
    mount jupyterhub_config.py as volume

#### Dockerfile
    install: 
        dockerspawner 
        jupyterhub-idle-culler 
        PyJWT
        pyyaml
        oauthenticator
        nativeauthenticator (modified template to allow github/google )

#### jupyterhub_config.py
    customize user images as defined in config.yaml (sample in singleuser/srv/setup)
    MyDockerSpawner: mounts volumes according to user config
    MultiOAuthenticator: native, github, google
    c.JupyterHub.base_url = '/jhub/'

#### configurable proxy
    runs as a separated docker sharing the network. This way shutting down the hub doesn't close clients
    see ./proxy

### build jupyterhub server:
    make build

### client images
    diverse images in singleuser/Dockerfile-xxx

### services for jupyter_proxy
    in singleuser/srv:
    - jupyter-rserver_proxy (RStudio)
    - jupyter_codeserver_proxy (Code Server)
    - jupyter_deepzoom_proxy (openslide python)
    - jupyter_tensorboard_proxy (tensorboard)
    - jupyter_openrefine_proxy (openrefine)
    - jupyter-logout (logout/comntrol/resources)
    - jupyter_labelimg_proxy (labelimg)

### build jupyterlab clients:
    make image?

### start
    docker-compose up -d
