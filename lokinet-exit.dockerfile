FROM debian:stable AS lokinet-exit
ENV container docker
# set up packages
RUN /bin/bash -c 'echo "man-db man-db/auto-update boolean false" | debconf-set-selections'
RUN /bin/bash -c 'apt-get -o=Dpkg::Use-Pty=0 -q update && apt-get -o=Dpkg::Use-Pty=0 -q dist-upgrade -y && apt-get -o=Dpkg::Use-Pty=0 -q install -y --no-install-recommends ca-certificates curl iptables dnsutils lsb-release systemd systemd-sysv cron conntrack iproute2'
RUN /bin/bash -c 'curl -so /etc/apt/trusted.gpg.d/lokinet.gpg https://deb.oxen.io/pub.gpg'
RUN /bin/bash -c 'echo "deb https://deb.oxen.io $(lsb_release -sc) main" > /etc/apt/sources.list.d/lokinet.list'
RUN /bin/bash -c 'apt-get -o=Dpkg::Use-Pty=0 -q update && apt-get -o=Dpkg::Use-Pty=0 -q dist-upgrade -y && apt-get -o=Dpkg::Use-Pty=0 -q install -y --no-install-recommends lokinet'

# make config dir for lokinet
RUN /bin/bash -c 'mkdir -p /var/lib/lokinet/conf.d'
# set up private data dir for lokinet
RUN /bin/bash -c 'mkdir /data && chown _lokinet:_loki /data'

# set up configs for lokinet
COPY contrib/lokinet-exit.ini /var/lib/lokinet/conf.d/exit.ini
COPY contrib/lokinet-exit.resolv.conf /etc/resolv.conf
RUN /bin/bash -c 'chmod 644 /etc/resolv.conf'

# set up system configs
COPY contrib/lokinet-exit-sysctl.conf /etc/sysctl.d/00-lokinet-exit.conf
COPY contrib/lokinet-exit-rc.local.sh /etc/rc.local
RUN /bin/bash -c 'chmod 700 /etc/rc.local'
# setup cron jobs
COPY contrib/lokinet-kill-scans.sh /usr/local/bin/lokinet-kill-scans.sh
RUN /bin/bash -c 'chmod 700 /usr/local/bin/lokinet-kill-scans.sh'
COPY contrib/lokinet-update-exit-address.sh /usr/local/bin/lokinet-update-exit-address.sh
RUN /bin/bash -c 'chmod 700 /usr/local/bin/lokinet-update-exit-address.sh'
COPY contrib/lokinet-exit.crontab /etc/cron.d/lokinet-exit
RUN /bin/bash -c 'chmod 644 /etc/cron.d/lokinet-exit'


VOLUME [ "/sys/fs/cgroup/systemd" ]
VOLUME [ "/sys/fs/cgroup/" ]
STOPSIGNAL SIGRTMIN+3
ENTRYPOINT ["/sbin/init", "verbose", "systemd.unified_cgroup_hierarchy=false"]
