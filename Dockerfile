FROM ubuntu:22.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y dist-upgrade && DEBIAN_FRONTEND=noninteractive apt-get install -y openssh-server git-core python3 && apt-get clean

ADD init.sh /tmp/init.sh
RUN chmod u+rwx /tmp/init.sh

ADD git-proxy.py /git-proxy.py
RUN chmod ugo+rx /git-proxy.py

ADD start.sh /start.sh
RUN chmod ugo+rx /start.sh

EXPOSE 22

VOLUME ["/repositories"]

CMD /start.sh
