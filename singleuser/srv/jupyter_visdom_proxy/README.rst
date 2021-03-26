jupyter visdom proxy

Adds a proxy service to jupyterlab to open visdom
    https://github.com/fossasia/visdom

config file:
    ~/.jupyter/services.yaml
    
    - visdom:
        logdir: /home/jovyan/board  # this is the default. Folder will be created if no exists
        new_browser: True  # open as new tab in browser

