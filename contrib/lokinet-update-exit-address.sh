#!/bin/bash
dig @127.3.2.1 +short -t cname localhost.loki > /data/lokinet-addr.txt
chmod 444 /data/lokinet-addr.txt
