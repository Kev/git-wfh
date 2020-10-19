#!/bin/bash
tmp/init.sh
tail -F /home/git/proxy.log&
/usr/sbin/sshd -D