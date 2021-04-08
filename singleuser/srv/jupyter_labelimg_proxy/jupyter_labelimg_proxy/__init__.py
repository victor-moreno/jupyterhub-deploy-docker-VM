import os
import yaml
import shlex
import tempfile

# load config
with open(os.path.expanduser('~/.jupyter/services.yaml'), 'r') as cfgfile:
    cfg = yaml.load(cfgfile, Loader=yaml.FullLoader)

def get_key(key, app='labelimg', cfg=cfg):
    for a in cfg:
        for k, v in a.items():
            if k == app:
                return v.get(key)

def get_images_dir():
    images_dir = get_key('images_dir')
    if images_dir == None:
        images_dir =  os.path.expanduser('~/images')
    if not os.path.isdir(images_dir):
        os.makedirs(images_dir, exist_ok=True)
        if not os.path.isdir(images_dir):
            raise Exception(f'Could not create {images_dir}')
    return images_dir            

def get_icon_path():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'resources', 'labelimg.svg'
    )

def setup_labelimg():
    NOVNC_PATH = os.getenv('NOVNC_PATH', '/opt/noVNC')
    sockets_dir = tempfile.mkdtemp()
    sockets_path = os.path.join(sockets_dir, 'vnc-socket')
    xstartup_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'xstartup')

    vnc_command = ' '.join((shlex.quote(p) for p in [
        'vncserver',
        '-verbose',
        '-xstartup', xstartup_path,
        '-geometry', '1680x1050',
        '-SecurityTypes', 'None',
        '-rfbunixpath', sockets_path,
        '-fg',
        ':1',
    ]))
    return {
        'command': [
            'websockify', '-v',
            '--web', NOVNC_PATH,
            '--heartbeat', '30',
            '5901',
            '--unix-target', sockets_path,
            '--',
            '/bin/sh', '-c',
            f'cd {os.getcwd()} && {vnc_command}'
        ],
        'port': 5901,
        'timeout': 30,
        'mappath': {'{base_url}/labeling/': '/'},
        'new_browser_window': True,
        'launcher_entry': {
            'title': 'labelImg',
            'icon_path': get_icon_path()
        }
    }

