#!/usr/bin/env python3

# Copyright 2020 Kevin Smith

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import subprocess
import sys
import os
import proxyenvironment

def debug(line):
    with open('/home/git/proxy.log', 'a+') as f:
        f.write(line + "\n")

def exec(command, check):
    try:
        result = subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        debug(str(e))
        if check:
            raise e

def update_cache(repository, dest_path):
    debug("Updating cache for %s" % repository)
    if not os.path.exists(dest_path):
        repository_parts = repository.split(os.sep)[1:] # 1: because the first is empty
        remote = "ssh://%s@%s:%s%s" % (proxyenvironment.UPSTREAM_USER, proxyenvironment.UPSTREAM_HOST, proxyenvironment.UPSTREAM_PORT, repository)
        os.makedirs(dest_path)
        command = ['git', 'clone', '--mirror', remote, dest_path]
        debug("Cloning repository with %s" % command)
        exec(command, True)
        prereceive_path = "%s/hooks/pre-receive" % dest_path
        debug("Installing write-blocking hook to %s" % prereceive_path)
        with open(prereceive_path, 'w+') as f:
            f.writelines(['#!/bin/bash\n', 'echo "You cannot push to the git-wfh proxy"\n', 'exit 1\n'])
        exec(['chmod', 'ugo+rx', prereceive_path], True)
        # TODO: Install hooks to prevent pushes
    else:
        os.chdir(dest_path)
        command = ['git', 'fetch', '--prune']
        debug("Updating cache with %s" % command)
        exec(command, False)

debug("Proxy called with:")
debug(" ".join(sys.argv))
# Remove the first argument (script name)
shell_args = sys.argv[1:]
# The final argument is the git-shell command and (in quotes) repository
repository = shell_args[-1].split()[-1][1:-1]
if repository[0] != os.sep:
    # This happens if it's a ~path
    repository = os.sep + repository
dest_path = '/repositories' + repository
update_cache(repository, dest_path)
# Now mangle the final part to map it to our cache path
final_parts = shell_args[-1].split()
final_parts[-1] = "'%s'" % dest_path
shell_args[-1] = " ".join(final_parts)
command = ['/usr/bin/git-shell'] + shell_args
debug("Passing command upstream with %s" % command)
exec(command, True)