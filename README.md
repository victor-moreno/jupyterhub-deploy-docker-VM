# adapted from jupyterhub-deploy-docker 
[https://github.com/jupyterhub/jupyterhub-deploy-docker](https://github.com/jupyterhub/jupyterhub-deploy-docker) 

### changes to server

jupyterhub_config.py:

docker-compose.yaml:
-p 12000:443

### .env


### client image 
jupyterhub_config.py:

c.JupyterHub.base_url = '/jhub/'



### build jupyterhub server:
make build

### build jupyterlab client:
make image

# start
docker-compose up -d

