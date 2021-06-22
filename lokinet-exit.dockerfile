FROM debian:stable AS lokinet-exit

# set up packages
RUN /bin/bash -c 'echo "man-db man-db/auto-update boolean false" | debconf-set-selections'
RUN /bin/bash -c 'apt-get -o=Dpkg::Use-Pty=0 -q update && apt-get -o=Dpkg::Use-Pty=0 -q dist-upgrade -y && apt-get -o=Dpkg::Use-Pty=0 -q install -y --no-install-recommends ca-certificates curl iptables dnsutils lsb-release'
RUN /bin/bash -c 'curl -so /etc/apt/trusted.gpg.d/lokinet.gpg https://deb.oxen.io/pub.gpg'
RUN /bin/bash -c 'echo "deb https://deb.oxen.io $(lsb_release -sc) main" > /etc/apt/sources.list.d/lokinet.list'
RUN /bin/bash -c 'apt-get -o=Dpkg::Use-Pty=0 -q update && apt-get -o=Dpkg::Use-Pty=0 -q dist-upgrade -y && apt-get -o=Dpkg::Use-Pty=0 -q install -y --no-install-recommends lokinet'

# make config dir for lokinet
RUN /bin/bash -c 'mkdir -p /var/lib/lokinet/conf.d'
# set up private data dir for lokinet
RUN /bin/bash -c 'mkdir /data && chown _lokinet:_loki /data'

# set up configs for lokinet
COPY contrib/lokinet-exit.ini /var/lib/lokinet/conf.d/exit.ini
# set up system configs
COPY contrib/lokinet-exit-sysctl.conf /etc/sysctl.d/00-lokinet-exit.conf
COPY contrib/lokinet-exit-rc.local.sh /etc/rc.local
