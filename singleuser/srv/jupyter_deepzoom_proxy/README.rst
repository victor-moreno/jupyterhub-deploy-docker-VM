jupyter deepzoom proxy

Adds a proxy service to jupyter to view openslide images

config:
- a new browser tab is opened if exists file ~/.jupyter/.new_browser 
- if file ~/.images exists and has a valid folder, it is used to load images. Otherwise, ~/images or ~/ is used

This package uses code from OpenSlide Python

OpenSlide Python is a Python interface to the OpenSlide library.

.. _ OpenSlide: https://openslide.org/


License
=======

This code and OpenSlide Python is released under the terms of the `GNU Lesser General
Public License, version 2.1`_.

.. _`GNU Lesser General Public License, version 2.1`: https://raw.github.com/openslide/openslide-python/master/lgpl-2.1.txt
