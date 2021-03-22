jupyter deepzoom proxy

Adds a proxy service to jupyter to view openslide images

config file:
    ~/.jupyter/services.yaml
    
    - deepzoom:
        images_dir: /home/jovyan/images  # this is the default. Folder will be created if no exists
        new_browser: True  # open as new tab in browser


This package uses code from OpenSlide Python

OpenSlide Python is a Python interface to the OpenSlide library.

.. _ OpenSlide: https://openslide.org/


License
=======

This code and OpenSlide Python is released under the terms of the `GNU Lesser General
Public License, version 2.1`_.

.. _`GNU Lesser General Public License, version 2.1`: https://raw.github.com/openslide/openslide-python/master/lgpl-2.1.txt
