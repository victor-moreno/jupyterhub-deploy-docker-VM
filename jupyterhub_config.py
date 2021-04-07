# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

# pre-spawn settings

NB_UID = 1001
NB_GID = 100

CUDA = 'cuda' in os.environ['HOSTNODE']  

c = get_config()  

# read users/teams & images
import os, yaml
with open('/srv/jupyterhub/config.yaml', 'r') as cfgfile:
    cfg = yaml.load(cfgfile, Loader=yaml.FullLoader)

team_map = cfg['users']

# Whitlelist users and admins       # google: remove @gmail.com
c.Authenticator.allowed_users = list(team_map.keys())
c.Authenticator.admin_users = admin = set()
for u, team in team_map.items():
    if 'admin' in team:
        admin.add(u)

# Spawn single-user servers as Docker containers    
# CustomDockerSpawner

# form to select image
def get_options_form(spawner):
    username = spawner.user.name  #  .split('@')[0]
    teams = cfg['users'][username]
    images = cfg['images']

    # list of image letters for user
    img = {k:v for k,v in images.items() if k in teams }
    images = [] # unique list
    for t,i in img.items():
        for k in i:
            if k not in images:
                images.append(k)
    if not CUDA:
        images = [i for i in images if i  != 'G']

    # dict of image label:build
    available_images = cfg['available_images']
    allowed_images = [v for k,v in available_images.items() if k in images]
    images=[]
    for i in allowed_images:
        images = images | i.items()
    
    allowed_images = dict(images)

    # prepare form
    if len(allowed_images) > 1:
        option_t = '<option value="{image}" {selected}>{label}</option>'
        options = [
            option_t.format(
                image=image, label=label, selected='selected' if image == spawner.image else ''
            )
            for label, image in allowed_images.items()
        ]
        return """
        <br><br>
        <label for="image">Select an image for {username}:</label>
        <select class="form-control" name="image" required autofocus>
        {options}
        </select>
        """.format(options=options, username=username)
    else:
        spawner.image = [v for k,v in allowed_images.items()][0]

c.DockerSpawner.options_form = get_options_form

def set_sudo(spawner):
    username = spawner.user.name
    teams = cfg['users'][username]
    if 'sudo' in teams:
        return 'yes'
    else:
        return 'no'

c.DockerSpawner.environment = {
'NB_USER':'jovyan',
'NB_UID': NB_UID,
'NB_GID': NB_GID,
'NB_UMASK':'002',
'CHOWN_HOME':'yes',
'GRANT_SUDO': set_sudo, 
}

    

from dockerspawner import DockerSpawner
class CustomDockerSpawner(DockerSpawner):
    
    # mount volumes by team
    def start(self):
        home_dir = os.environ.get('HOME_DIR')
        notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR')

        username = self.user.name

        self.volumes[f"{home_dir}/{username.split('@')[0]}"] = {
            'bind': notebook_dir,
            'mode': 'rw',
        }

        teams = cfg['users'][username]
        mounts = cfg['mounts']

        mounts = {k:v for k,v in mounts.items() if k in teams }

        for k,v in mounts.items():
            for h,d in v.items():
                self.volumes[h] = { 'bind': d[0], 'mode': d[1] }
           

        return super().start()
    

# c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.JupyterHub.spawner_class = CustomDockerSpawner

# 'user': 'root',

c.DockerSpawner.extra_create_kwargs = {
'user': 'root',
'hostname': 'hub',
}

# nvidia
if CUDA:
    c.DockerSpawner.extra_host_config = {
    'runtime': 'nvidia',
    }

# 'device_requests': [docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]], ), ], }


# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd })

# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config.update({ 'network_mode': network_name })

# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
#notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'

notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
#c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

# external proxy
c.JupyterHub.cleanup_servers = False
# tells the hub to not stop servers when the hub restarts (this is useful even if you don’t run the proxy separately).

c.ConfigurableHTTPProxy.should_start = False
# tells the hub that the proxy should not be started (because you start it yourself).
c.ConfigurableHTTPProxy.auth_token = os.environ.get('CONFIGPROXY_AUTH_TOKEN')
# token for authenticating communication with the proxy.
c.ConfigurableHTTPProxy.api_url = 'http://jupyterproxy:8001' #'http://192.168.1.254:8001'
# the URL which the hub uses to connect to the proxy’s API.

# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.base_url = '/jhub/'
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8080

# don't need because we are behind an https reverse proxy
# # TLS config: requires generating certificates
# c.JupyterHub.port = 443
# c.JupyterHub.ssl_key = os.environ['SSL_KEY']
# c.JupyterHub.ssl_cert = os.environ['SSL_CERT']

# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')

c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
    'jupyterhub_cookie_secret')

c.JupyterHub.db_url = 'postgresql://postgres:{password}@{host}/{db}'.format(
    host=os.environ['POSTGRES_HOST'],
    password=os.environ['POSTGRES_PASSWORD'],
    db=os.environ['POSTGRES_DB'],
)

# reset database
# c.JupyterHub.reset_db = False

# Authenticate users

'''
# GitHub
c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'
c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

# Native
# admin users in c.Authenticator.admin_users are automatically authorized when signup
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'
'''

##### multioauth
# https://github.com/jupyterhub/oauthenticator/issues/136

from traitlets import List
from jupyterhub.auth import Authenticator

def url_path_join(*parts):
    return '/'.join([p.strip().strip('/') for p in parts])

class MultiOAuthenticator(Authenticator):
    authenticators = List(help="The subauthenticators to use", config=True)

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self._authenticators = []
        for authenticator_klass, url_scope, configs in self.authenticators:
            c = self.trait_values()
            c.update(configs)
            self._authenticators.append({"instance": authenticator_klass(**c), "url_scope": url_scope})

    def get_custom_html(self, base_url):
        html = []
        for authenticator in self._authenticators:
            login_service = authenticator["instance"].login_service
            if login_service == 'User/Pass':
                url = url_path_join(authenticator["url_scope"], "login")
            else:
                url = url_path_join(authenticator["url_scope"], "oauth_login")

            # html.append(
            #     f"""
            #     <div class="service-login">
            #       <a role="button" class='btn btn-jupyter btn-lg' href='{url}'>
            #         Sign in with {login_service}
            #       </a>
            #     </div>
            #     """
            # )
        return "\n".join(html)

    def get_handlers(self, app):
        routes = []
        for _authenticator in self._authenticators:
            for path, handler in _authenticator["instance"].get_handlers(app):

                class SubHandler(handler):
                    authenticator = _authenticator["instance"]

                routes.append((f'{_authenticator["url_scope"]}{path}', SubHandler))
        return routes

c.JupyterHub.authenticator_class = MultiOAuthenticator

from oauthenticator.github import GitHubOAuthenticator
from oauthenticator.google import GoogleOAuthenticator
from nativeauthenticator import NativeAuthenticator
#from oauthenticator.azuread  import AzureAdOAuthenticator

if CUDA:
    c.MultiOAuthenticator.authenticators = [
        (GitHubOAuthenticator, '/github', {
            'client_id': os.environ['GITHUB_CLIENT_ID'],
            'client_secret': os.environ['GITHUB_CLIENT_SECRET'],
            'oauth_callback_url': os.environ['GITHUB_CALLBACK_URL']
        }),
        (GoogleOAuthenticator, '/google', {
            'client_id': os.environ['GOOGLE_CLIENT_ID'],
            'client_secret': os.environ['GOOGLE_CLIENT_SECRET'],
            'oauth_callback_url': os.environ['GOOGLE_CALLBACK_URL'],
            'login_service': 'Google'
        }),
        (NativeAuthenticator, '/', {
            'login_service': 'User/Pass'
        }),
    #    (AzureAdOAuthenticator, '/microsoft', {
    #        'client_id': os.environ['AZURE_CLIENT_ID'],
    #        'client_secret': os.environ['AZURE_CLIENT_SECRET'],
    #        'oauth_callback_url': os.environ['AZURE_CALLBACK_URL'],
    #        'tenant_id': os.environ['AZURE_TENANT_ID'],
    #        'login_service': 'Microsoft'
    #    })
    ]
else:
    c.MultiOAuthenticator.authenticators = [
        (GitHubOAuthenticator, '/github', {
            'client_id': os.environ['DGITHUB_CLIENT_ID'],
            'client_secret': os.environ['DGITHUB_CLIENT_SECRET'],
            'oauth_callback_url': os.environ['DGITHUB_CALLBACK_URL']
        }),
        (GoogleOAuthenticator, '/google', {
            'client_id': os.environ['DGOOGLE_CLIENT_ID'],
            'client_secret': os.environ['DGOOGLE_CLIENT_SECRET'],
            'oauth_callback_url': os.environ['DGOOGLE_CALLBACK_URL'],
            'login_service': 'Google'
        }),
        (NativeAuthenticator, '/', {
            'login_service': 'User/Pass'
        }),
    ]
        
import nativeauthenticator
c.JupyterHub.template_paths = [f"{os.path.dirname(nativeauthenticator.__file__)}/templates/"]
#  ["/usr/local/lib/python3.8/dist-packages/nativeauthenticator/templates/"]

# google
# https://oauthenticator.readthedocs.io/en/latest/api/gen/oauthenticator.google.html
c.GoogleOAuthenticator.hosted_domain = ['gmail.com','morenoaguado.net']
c.GoogleOAuthenticator.login_service = 'Google'
c.GoogleOAuthenticator.delete_invalid_users = True
# c.GoogleOAuthenticator.allowed_users = {'victor.r.moreno@gmail.com'}
# c.GoogleOAuthenticator.allowed_google_groups = {'uic'}

c.NativeAuthenticator.check_common_password = True
c.NativeAuthenticator.minimum_password_length = 8
c.NativeAuthenticator.allowed_failed_logins = 3

# end OAuth

## enable authentication state0
c.MultiOAuthenticator.enable_auth_state = True
import warnings
if 'JUPYTERHUB_CRYPT_KEY' not in os.environ:
    warnings.warn(
        "Need JUPYTERHUB_CRYPT_KEY env for persistent auth_state.\n"
        "    export JUPYTERHUB_CRYPT_KEY=$(openssl rand -hex 32)"
    )
    c.CryptKeeper.keys = [ os.urandom(32) ]

pass

# remove idle notebooks after inactive time
# https://github.com/jupyterhub/jupyterhub-idle-culler
import sys
c.JupyterHub.services = [
    {
        'name': 'idle-culler',
        'admin': True,
        'command': [sys.executable, '-m', 'jupyterhub_idle_culler', '--timeout=3600'],
    }
]

# max simultaneous users
c.JupyterHub.concurrent_spawn_limit = 10

# user limits
# c.Spawner.cpu_limit = 2 # cores
# c.Spawner.mem_limit = 8G 

