###
## Faraday Penetration Test IDE
## Copyright (C) 2015  Infobyte LLC (http://www.infobytesec.com/)
## See the file 'doc/LICENSE' for the license information
###
#
# Ubuntu Dockerfile
#
# https://github.com/dockerfile/ubuntu
#

# Pull base image.
FROM BUILDDISTRO

# Set environment variables.
ENV HOME /root
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV TERM linux

# Install.
RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update

#RUN \
#  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
#  apt-get update && \
#  apt-get -y upgrade

RUN \
  apt-get install -y build-essential && \
  apt-get install -y software-properties-common && \
  apt-get install -y byobu curl git htop man unzip vim wget && \
  apt-get install -y python-pip python-dev && \
  apt-get install -y openssh-server && \
  rm -rf /var/lib/apt/lists/*

#RUN pip install couchdbkit==0.6.5 mockito==0.5.1 whoosh==2.5.5 argparse==1.1 IPy==0.75 restkit==4.2.2 requests==1.2.3 tornado==3.2 flask==0.10.1 colorama==0.3.2 

# Add files.
ADD root/.bashrc /root/.bashrc
ADD root/.gitconfig /root/.gitconfig
ADD root/.scripts /root/.scripts


# Define working directory.
WORKDIR /root

RUN mkdir -p /var/run/sshd

RUN echo 'root:testing' | chpasswd

RUN mkdir -p /root/.ssh/
RUN echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDjXxcHjyVkwHT+dSYwS3vxhQxZAit6uZAFhuzA/dQ2vFu6jmPk1ewMGIYVO5D7xV3fo7/RXeCARzqHl6drw18gaxDoBG3ERI6LxVspIQYjDt5Vsqd1Lv++Jzyp/wkXDdAdioLTJyOerw7SOmznxqDj1QMPCQni4yhrE+pYH4XKxNx5SwxZTPgQWnQS7dasY23bv55OPgztI6KJzZidMEzzJVKBXHy1Ru/jjhmWBghiXYU5RBDLDYyT8gAoWedYgzVDmMZelLR6Y6ggNLOtMGiGYfPWDUz9Z6iDAUsOQBtCJy8Sj8RwSQNpmOgSzBanqnhed14hLwdYhnKWcPNMry71 faraday@faraday-docker.org' >> /root/.ssh/authorized_keys

RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

ADD . /root/build
WORKDIR /root/build
#RUN ./run.sh

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]


# docker build -t testing4 .
# sudo docker run -i -t -p 22  testing4
# cat extras/docker/Dockerfile.base | sed -e 's/FARADAYDISTRO/debian:14.04/'
# docker build -t faraday - < cat extras/docker/Dockerfile.base | sed -e 's/FARADAYDISTRO/debian:14.04/'
# cat extras/docker/Dockerfile.base | sed -e 's/FARADAYDISTRO/13.10/' > docker
# docker build -t faraday2 - < /tmp/docker
