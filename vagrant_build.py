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
import os


distros = [
           {'name' :'debian/jessie64',
            'url':'https://atlas.hashicorp.com/debian/jessie64',
            'provider':'virtualbox'},
           {'name' :'debian/wheezy64',
            'url':'https://atlas.hashicorp.com/debian/wheezy64',
            'provider':'virtualbox'},            
          ]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cmd', help='Command to run')
    # parser.add_argument('-i', '--images', help='list of images')
    parser.add_argument('-v', '--vagrantfile', help='Vagrantbase file', default='extras/Vagrantfile.base')
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = parse_args()
    f = open(args.vagrantfile)
    baseVagrant = f.read()
    f.close()

    if args.cmd:
        # if args.images:
        #     with open(args.images) as f:
        #         distros = f.read().splitlines()

        print "Distros: " + str(distros)
        for d in distros:
            try:
                print "Download Vagrant: " + d['name']
                subprocess.call('vagrant box add %s %s' % (d['name'],d['url']), shell=True)
                print "Start Vagrant: " + d['name']
                newVagrant = re.sub("BUILDDISTRO", d['name'], baseVagrant)
                file_ = open('Vagrantfile', 'w')
                file_.write(newVagrant)
                file_.close()
                subprocess.call('vagrant up --provider %s' % d['provider'], shell=True)
                subprocess.call('vagrant ssh -c \'%s\'' % args.cmd, shell=True)

                #subprocess.call('vagrant destroy -f', shell=True)

            except subprocess.CalledProcessError, cpe:
                print('build images error stop: "%s"' % cpe)
                sys.exit(1) 
    else:
        print "Usage -h",

