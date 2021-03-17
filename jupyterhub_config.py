# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os


# pre-spawn settings

NB_UID = 1001
NB_GID = 100

# Whitlelist users and admins
# google: remove @gmail.com
#
# remove to avoid conflicts creating new users
#
import ast
with open('/srv/jupyterhub/user_list.txt') as f: 
    team_map = ast.literal_eval(f.read())

c.Authenticator.allowed_users = list(team_map.keys())

c.Authenticator.admin_users = admin = set()
for u, team in team_map.items():
    if 'admin' in team:
        admin.add(u)

#c.Authenticator.username_map = {'victor.r.moreno@gmail.com': 'victor.r.moreno'}
# c.JupyterHub.redirect_to_server = False

# Spawn single-user servers as Docker containers

from dockerspawner import DockerSpawner
class MyDockerSpawner(DockerSpawner):
    def start(self):
        self.team_map = team_map
        home_dir = os.environ.get('HOME_DIR')
        data_dir = os.environ.get('DATA_DIR')
        work_dir = os.environ.get('IMAGES_WORK_DIR')
        img_dir = os.environ.get('IMAGES_DIR')
        notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR')

        username = self.user.name.split('@')[0]

        if username in self.team_map:
            teams = self.team_map[username]
        else:
            teams = ''

        self.volumes[f"{home_dir}/{username}"] = {
            'bind': notebook_dir,
            'mode': 'rw',
        }
        if 'projects' in teams:
            self.volumes[data_dir] = {
                'bind': notebook_dir+'/projects',
                'mode': 'rw',
            }
        if 'images' in teams:
            self.volumes[img_dir] = {
                'bind': notebook_dir+'/images',
                'mode': 'ro',
            }
            self.volumes[work_dir] = {
                'bind': notebook_dir+'/work',
                'mode': 'rw',
            }
        return super().start()


c.JupyterHub.spawner_class = MyDockerSpawner
# c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

c.DockerSpawner.environment = {
'NB_USER':'jovyan',
'NB_UID': NB_UID,
'NB_GID': NB_GID,
'NB_UMASK':'002',
'GRANT_SUDO':'yes',
'CHOWN_HOME':'yes',
'JUPYTER_ENABLE_LAB':'yes'
}

'''
# hook to run before spawning user image
def pre_spawn_hook(spawner):
    username = spawner.user.name
    # images

c.Spawner.pre_spawn_hook = pre_spawn_hook
'''


c.DockerSpawner.extra_create_kwargs = {
'user': 'root',
'hostname': 'hub',
}

# nvidia
c.DockerSpawner.extra_host_config = {
'runtime': 'nvidia',
}
# 'device_requests': [docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]], ), ], }

# Spawn containers from this image
c.DockerSpawner.image = os.environ['DOCKER_NOTEBOOK_IMAGE']

## c.DockerSpawner.allowed_images = Union({}) form to select image to run

c.DockerSpawner.default_url = '/lab'

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

# volume_driver is no longer a keyword argument to create_container()
# c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'local' })
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True

# For debugging arguments passed to spawned containers
#c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.base_url = '/jhub/'
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8080

# TLS config: requires generating certificates
c.JupyterHub.port = 443
c.JupyterHub.ssl_key = os.environ['SSL_KEY']
c.JupyterHub.ssl_cert = os.environ['SSL_CERT']

# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')

c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
    'jupyterhub_cookie_secret')

c.JupyterHub.db_url = 'postgresql://postgres:{password}@{host}/{db}'.format(
    host=os.environ['POSTGRES_HOST'],
    password=os.environ['POSTGRES_PASSWORD'],
    db=os.environ['POSTGRES_DB'],
)

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

## enable authentication state
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

