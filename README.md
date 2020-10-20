# Git WFH - a Work From Home Proxy for Git

When working from home it is convenient to have fast local access
to Git repositories - both to avoid the potentially slow download
of very large repositories multiple times and to cope in the case
of connectivity failures. This image is intended to be run on a
developer's local network (or local machine, for single-machine
setups) and to proxy all read access to the workplace Git servers
so that large downloads will be faster and operation can continue
when connectivity to the workplace server is unavailable.

This does *not* attempt to do anything clever with write access
to the server (or, indeed, anything non-clever) - it is a
read-only proxy. This makes use of Git's ability to configure
different URIs for fetching from and pushing to a remote such that
you can fetch from the proxy, and push directly to the workplace
server.

## Building the Image

`docker build -t git-wfh .`

## Running the Proxy

To use the `docker-compose.yaml` file copy `environment.sample` to `environment`, edit to configure for your deployment, and then
`docker-compose up -d`. You should, of course, read what it's doing
to understand it before running it.

## Configuring Git

Ensure that your ssh config allows agent forwarding to the proxy, e.g. in `~/.ssh/config`
```
Host proxy.mynetwork
  ForwardAgent yes
```
Then configure your local git so that when it tries to fetch from the workplace
remote it'll fetch from the proxy, and when pushing it'll still push to the workplace, e.g.
```
git config --global url.ssh://git@proxy.mynetwork:9022/.insteadOf ssh://git@workplace:22/
git config --global url.ssh://git@workplace:22/.pushInsteadOf ssh://git@workplace:22/
```

## Problems

If your process gets destroyed in the middle of a checkout and you end up with a broken repository, just delete the relevant half-baked repository manually and let it recover on next fetch.

## Alternatives

Other Git mirroring solutions exist, although the ones I found didn't do quite what I wanted. One might also consider https://github.com/opensafely/git-server-proxy  or https://github.com/guillon/git-mirror.