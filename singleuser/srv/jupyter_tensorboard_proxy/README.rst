jupyter tensorboard proxy

Adds a proxy service to jupyterlab to open tensorboard

config:
- A new browser tab is opened if exists file ~/.jupyter/.new_browser 
- if file ~/.board exists and has a valid folder, it is used as --logdir. Otherwise, ~/board is created and used
