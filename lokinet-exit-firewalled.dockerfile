# set up firewalled exit

FROM registry.oxen.rocks/lokinet-exit:latest

RUN /bin/bash -c 'pip3 install iblocklist2ipset'

COPY contrib/parse-blocklist.py /usr/local/bin/parse-blocklist.py
RUN /bin/bash -c 'chmod 700 /usr/local/bin/parse-blocklist.py'

COPY contrib/lokinet-update-firewall.sh /usr/local/bin/lokinet-update-firewall.sh
RUN /bin/bash -c 'chmod 700 /usr/local/bin/lokinet-update-firewall.sh'

COPY contrib/lokinet-firewall.crontab /etc/cron.d/lokinet-firewall
RUN /bin/bash -c 'chmod 644 /etc/cron.d/lokinet-firewall'

RUN /bin/bash -c 'echo /usr/local/bin/lokinet-update-firewall.sh >> /etc/rc.local'