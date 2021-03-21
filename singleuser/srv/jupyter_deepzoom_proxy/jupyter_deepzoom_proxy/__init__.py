import os

def get_image_folder():
    image_folder = os.environ.get('IMAGE_FOLDER')
    if not image_folder:
        home_images = os.path.isdir('/home/jovyan/images')
        if os.path.isdir(home_images):
            image_folder = '/home/jovyan/images'
        else:
            image_folder = '/home/jovyan'

    return image_folder

def get_icon_path():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'icons', 'deepzoom.svg'
    )

def get_deepzoom_path():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'deepzoom_multiserver'
    )

def setup_deepzoom():
    def _get_cmd(port):
        cmd = [
                get_deepzoom_path(), 
                '--base={base_url}deepzoom', 
                '--listen=127.0.0.1', 
                '--port={port}',
                get_image_folder()
              ]
        return cmd
    return {
          'command': _get_cmd,
          'timeout': 20,
          'launcher_entry': {
              'title': 'Deepzoom openslide',
              'icon_path': get_icon_path()
          }
    }