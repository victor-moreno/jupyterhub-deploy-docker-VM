#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

if [ "$(which "$1")" = "/usr/local/bin/start-singleuser.sh" ]; then

   [[ -f /tmp/config_running.sh ]] && . /tmp/config_running.sh

fi

# Run the command provided
exec "$@"