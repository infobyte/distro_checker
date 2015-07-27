#!/usr/bin/env python2.7
'''
Faraday Penetration Test IDE
Copyright (C) 2015  Infobyte LLC (http://www.infobytesec.com/)
See the file 'doc/LICENSE' for the license information

'''
import subprocess
import argparse
import re
import uuid


distros = ['debian:7.3', 'ubuntu:14.10']


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cmd', help='Command to run')
    parser.add_argument('-i', '--images', help='list of images')
    parser.add_argument('-d', '--dockerfile', help='Command to run in the docker generation', default='extras/docker/Dockerfile.base')
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = parse_args()
    f = open(args.dockerfile)
    baseDocker = f.read()
    f.close()

    if args.cmd:
        if args.images:
            with open(args.images) as f:
                distros = f.read().splitlines()

        print "Distros: " + str(distros)
        for d in distros:
            print "Start build docker: " + d
            newDocker = re.sub("BUILDDISTRO", d, baseDocker)
            file_ = open('docker.tmp', 'w')
            file_.write(newDocker)
            file_.close()
            dockName = str(uuid.uuid4())[:13] + "_" + d

            print "docker build -f docker.tmp -t " + str(dockName) + "."

            try:
                subprocess.call('docker build -f docker.tmp -t %s .' % dockName, shell=True)
                
                try:
                    print "Run build docker: " + d + ", id: "  + str(dockName)
                    print('./docker_launcher.py -d -t %s' % dockName)
                    print ('./docker_launcher.py -c \'%s\' -t %s' % (args.cmd , dockName))
                    subprocess.call('./docker_launcher.py -c "%s" -t %s' % (args.cmd , dockName), shell=True)

                except subprocess.CalledProcessError, cpe:
                    print('Running faraday fail: "%s"' % cpe)

            except subprocess.CalledProcessError, cpe:
                print('build images error stop: "%s"' % cpe)
                sys.exit(1) 
    else:
        print "Usage -h",

