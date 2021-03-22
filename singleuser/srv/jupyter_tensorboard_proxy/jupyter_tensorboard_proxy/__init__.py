import os
import shutil

def get_logdir():
    board_folder = ''
    filename = os.path.expanduser('~/.board')
    if os.path.isfile(filename):
        with open(filename) as f:
            board_folder = f.readline().rstrip()

    if board_folder == '' or not os.path.isdir(board_folder):
        board_folder = '/home/jovyan/board'
        if not os.path.isdir(board_folder):
            os.mkdir(board_folder)
            
    return board_folder

def get_tensorboard(prog):
    if shutil.which(prog):
        return prog
    raise FileNotFoundError(f'Could not find {prog} in PATH')

def get_icon_path():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'icons', 'tensorboard.svg'
    )

def get_new_browser():
    # if file ~/.jupyter/.new_browser exists, open in new browser
    return os.path.isfile(os.path.expanduser('~/.jupyter/.new_browser'))

def setup_tensorboard():
  def _get_cmd(port):
    cmd = [
            get_tensorboard('tensorboard'), 
            '--port={port}',
            '--host=0.0.0.0',
            '--logdir',
            get_logdir(),
    ]
    return cmd
  
  return {
    'command': _get_cmd,
    'timeout': 20,
    'new_browser_tab': get_new_browser(),
    'launcher_entry': {
      'title': 'Tensorboard',
      'icon_path': get_icon_path(),
    }
  }
