import json
import socket

import requests

import config

def ip_to_loki(ip):
    """
    convert a ip address in string representation to a .loki address
    """
    return socket.gethostbyaddr(ip)[0]

def get_lokinet_ip():
    """
    return the ip address of the lokinet interface
    """
    return socket.getaddrinfo("localhost.loki", 0)[0][-1][0]

def resolve_local_address():
    """
    get our .loki address
    """
    return ip_to_loki(get_lokinet_ip())

def obtain_exit():
    """ 
    obtain an exit node and return its .loki address
    """
    return resolve_local_address()


# atomic units per human readable unit
_multiplier = 1000000000

def get_charge_amount():
    """
    get the base amount to charge for a pay address
    """
    return human_to_atomic(config.EXIT_FEE)

def human_to_atomic(amount):
    """ take a human readable amount and convert it to atomic units """
    return int(amount * _multiplier)

def atomic_to_human(amount)
    """
    convert an atomic amount to a readable human unit
    """
    return float(amount) /  float(_multiplier)

def rpc(method, args):
    """
    do an rpc request to the wallet
    """
    j = dict()
    try:
        resp = requests.post(config.wallet_url(), data=json.dumps({'jsonrpc': '2.0', 'id': 0, 'method': method, 'params' : dict(args)}), headers={'Content-Type': 'application/json'})
        j = resp.json()
    except Exception as ex:
        log.warn("rpc error: {}".format(ex))
    return 'result' in j and j['result'] or None

def obtain_sub_address():
    """
    obtain a new subaddress from the wallet
    """
    result = rpc('create_address', {'account_index': config.ACCOUNT_INDEX})
    if result and 'address' in result and 'address_index' in result:
        return result['address'], result['address_index']

def find_tx_for(index):
    """
    yield all tx for an account with this subaddress index
    """
    result = rpc("get_transfers", {'in':True, 'account_index': config.ACCOUNT_INDEX, 'subaddr_indices' :[int(index)]})
    if result and 'in' in result:
        for item in result['in']:
            yield item
