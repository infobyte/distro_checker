#!/bin/bash
###
## Faraday Penetration Test IDE
## Copyright (C) 2015  Infobyte LLC (http://www.infobytesec.com/)
## See the file 'doc/LICENSE' for the license information
###

# Delete all containers
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
#docker rm $(docker ps -a -q)
# Delete all images
#docker rmi $(docker images -q)
