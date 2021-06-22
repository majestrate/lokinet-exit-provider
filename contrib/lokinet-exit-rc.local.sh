#!/bin/bash

# flush iptables
iptables -t nat --flush
ip6tables -t nat --flush

# find default route's interface name
exit_if=$(ip route | grep ^default | cut -d' ' -f5)

# add ipv4 forward rule
iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o $exit_if -j MASQUERADE
# add ipv6 forward rule
ip6tables -t nat -A POSTROUTING -s fd00::ffff:a00:1/120 -o $exit_if -j MASQUERADE

# drop outbound ports
for port in 22 25 ; do
        iptables -A INPUT -p tcp --dport $port -j REJECT
        iptables -A OUTPUT -p tcp --dport $port -j REJECT
        iptables -A FORWARD -p tcp --dport $port -j REJECT
done

# increase nat conntrack size
sysctl net.netfilter.nf_conntrack_max=331072

# put a file down with our lokinet address in it
dig @127.3.2.1 +short -t cname localhost.loki > /data/lokinet-addr.txt
chmod 444 /data/lokinet-addr.txt
