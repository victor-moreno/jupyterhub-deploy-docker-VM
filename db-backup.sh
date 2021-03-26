#!/bin/bash
docker run --rm \
    --volumes-from jupyterhub-db \
    -v /mnt/mimas/remote/jhub/bck:/backup ubuntu:18.04 \
    bash -c "cd /var/lib/postgresql/data && tar czvf /backup/db-bck-$(date +%Y%m%d-%H%M).tar.gz ."

