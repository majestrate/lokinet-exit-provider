#!/bin/bash
if_name=lokitun0
if_addr=$(ip addr show $if_name | grep inet\  | sed 's/inet //' | cut -d' ' -f5)
iptables -t p2p-blocklist --flush
for range in $(wget --quiet https://raw.githubusercontent.com/Naunter/BT_BlockLists/master/bt_blocklists.gz -O - | zcat | parse-blocklist.py ) ; do
    iptables -t p2p-bloclist -A FORWARD -j REJECT -d $range -s $if_addr
done
