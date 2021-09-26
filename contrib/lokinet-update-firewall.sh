#!/bin/bash
# find default route's interface name
exit_if=$(ip route | grep ^default | cut -d' ' -f5)

# get lokinet's address
if_name=lokitun0
if_range=$(ip addr show $if_name | grep inet\  | sed 's/inet //' | cut -d' ' -f5)

iptables -t nat --flush
iptables -t nat -A POSTROUTING -s $if_range -o $exit_if -j MASQUERADE

# drop outbound ports
for port in 22 25 ; do
        iptables -A FORWARD -p tcp --dport $port -j REJECT --reject-with tcp-reset -s $if_range
done

# drop blacklisted ranges
for range in $(wget --quiet https://raw.githubusercontent.com/Naunter/BT_BlockLists/master/bt_blocklists.gz -O - | zcat | parse-blocklist.py ) ; do
    iptables -t nat -A FORWARD -j REJECT -d $range -s $if_range
done
