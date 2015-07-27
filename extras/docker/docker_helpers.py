#!/usr/bin/env python2.7
'''
Faraday Penetration Test IDE
Copyright (C) 2015  Infobyte LLC (http://www.infobytesec.com/)
See the file 'doc/LICENSE' for the license information

'''
import subprocess
import json
import time
import sys
import os

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

DOCKER_RUN = 'docker run -d -t '


def start_container(tag):
    """
    Start a new faraday container so we can connect using SSH and run faraday
    :return: The container id we just started
    """

    if tag is not None:
        docker_run = DOCKER_RUN + '%s' % tag
    else:
        docker_run = DOCKER_RUN

    try:
        container_id = subprocess.check_output(docker_run, shell=True)
    except subprocess.CalledProcessError, cpe:
        print('faraday container failed to start: "%s"' % cpe)
        sys.exit(1)
    else:
        # Let the container start the ssh daemon
        time.sleep(1)
        return container_id.strip()


def stop_container(container_id):
    """
    Stop a running faraday container
    """
    try:
        subprocess.check_output('docker stop %s' % container_id, shell=True)
    except subprocess.CalledProcessError, cpe:
        print('faraday container failed to stop: "%s"' % cpe)
        sys.exit(1)


def create_volumes():
    """
    Create the directories if they don't exist
    """
    faraday_home = os.path.expanduser('~/.faraday')
    faraday_shared = os.path.expanduser('~/faraday-shared')

    if not os.path.exists(faraday_home):
        os.mkdir(faraday_home)

    if not os.path.exists(faraday_shared):
        os.mkdir(faraday_shared)


def connect_to_container(container_id, cmd, extra_ssh_flags=()):
    """
    Connect to a running container, start one if not running.
    """
    try:
        cont_data = subprocess.check_output('docker inspect %s' % container_id, shell=True)
    except subprocess.CalledProcessError:
        print('Failed to inspect container with id %s' % container_id)
        sys.exit(1)

    try:
        ip_address = json.loads(cont_data)[0]['NetworkSettings']['IPAddress']
    except:
        print('Invalid JSON output from inspect command')
        sys.exit(1)

    ssh_key = os.path.join(ROOT_PATH, 'faraday-docker.prv')

    # Create the SSH connection command
    ssh_cmd = ['ssh', '-i', ssh_key, '-t', '-t', '-oStrictHostKeyChecking=no',
               '-o UserKnownHostsFile=/dev/null',
               '-o LogLevel=quiet']

    # Add the extra ssh flags
    for extra_ssh_flag in extra_ssh_flags:
        ssh_cmd.append(extra_ssh_flag)

    ssh_cmd.append('root@' + ip_address)
    ssh_cmd.append(cmd)

    print ssh_cmd    

    subprocess.call(ssh_cmd)


def check_root():
    # if not root...kick out
    if not os.geteuid() == 0:
        sys.exit('Only root can run this script')
