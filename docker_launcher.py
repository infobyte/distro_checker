#!/usr/bin/env python2.7
'''
Faraday Penetration Test IDE
Copyright (C) 2015  Infobyte LLC (http://www.infobytesec.com/)
See the file 'doc/LICENSE' for the license information

'''
import subprocess
import argparse
import json
import time
import sys
import os

from extras.docker.docker_helpers import (check_root, create_volumes, start_container,
                                   connect_to_container, stop_container)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', help='Use bash to connect',
                        action='store_true')
    parser.add_argument('-t', '--tag', help='Docker image tag to run',
                        required=False)
    parser.add_argument('-c', '--cmd', help='Command to run',
                        required=False)    
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    check_root()

    args = parse_args()
    #create_volumes()

    container_id = start_container(args.tag)

    if args.debug:
        cmd = '/bin/bash'
    elif args.cmd:
        cmd = args.cmd

    extra_ssh_flags = ('-X',)

    try:
        connect_to_container(container_id, cmd, extra_ssh_flags)
    finally:
        stop_container(container_id)
