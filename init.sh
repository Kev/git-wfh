#!/bin/bash

mkdir -p /var/run/sshd

# This doesn't much matter, as there's no password for the user, but do it anyway
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# Create and configure the git user for SSH
# This is the only user in use on the server, it will both be accepting the inbound
# connections and making the requests upstream. It has the proxy script as its
# shell and can't be used for anything else. It's set so that it'll make the initial
# connection upstream as TOFU.
useradd -m -s /git-proxy.py git
mkdir -p ~git/.ssh
echo $MY_PUBLIC_KEY > ~git/.ssh/authorized_keys
echo "Host = $UPSTREAM_HOST
StrictHostKeyChecking = accept-new" > ~git/.ssh/config
chown -R git:git ~git/.ssh
chmod go-rwx ~git/.ssh

mkdir -p /repositories
chown -R git:git /repositories

# Export the envvars somewhere the python script can get at them
echo "UPSTREAM_USER = '$UPSTREAM_USER'
UPSTREAM_HOST = '$UPSTREAM_HOST'
UPSTREAM_PORT = '$UPSTREAM_PORT'" > /proxyenvironment.py
chmod ugo+x /proxyenvironment.py