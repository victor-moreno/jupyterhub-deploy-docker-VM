import os
import shutil
import pathlib

def get_codeserver(prog):
    if shutil.which(prog):
        return prog
    raise FileNotFoundError(f'Could not find {prog} in PATH')

def get_icon_path():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'icons', 'codeserver.svg'
    )

def setup_codeserver():
  def _get_cmd(port):
    cmd = [
            get_codeserver('code-server'), 
            '--auth=none', 
            '--disable-telemetry', 
            '--bind-addr=127.0.0.1:{port}'
    ]
    return cmd
  
  return {
    'command': _get_cmd,
    'timeout': 20,
    'launcher_entry': {
      'title': 'Code Server',
      'icon_path': get_icon_path()
    }
  }
