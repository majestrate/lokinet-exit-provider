#!/usr/bin/env python3

from flask import Flask, render_template, request, session
import requests

from binascii import hexlify
import hashlib
import logging
import json
import os
import struct

import config
import logic
import k8api


logic.create_tables()

log = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = config.API_KEY

def rpc(method, args):
    """
    do an rpc request to the wallet
    """
    j = dict()
    try:
        log.info("rpc: {} {}".format(method, args))
        resp = requests.post(config.wallet_url(), data=json.dumps({'jsonrpc': '2.0', 'id': 0, 'method': method, 'params' : dict(args)}), headers={'Content-Type': 'application/json'})
        j = resp.json()
        log.info("rpc result: {}".format(j))
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

# atomic units per human readable unit
multiplier = 1000000000

def get_charge_amount(address):
    """
    get the amount to charge for a loki pay address
    """
    return 100 * multiplier


@app.route("/")
def exit_auth():
    pay_address = session.get("address", None)
    exit_addr = None
    if pay_address is None:
        result = obtain_sub_address()
        if result:
            session['address'], session['subaddr'] = result
            session['token'] = hexlify(os.urandom(12))
            pay_address = result[0]
    subaddr = session.get("subaddr", None)
    amount = get_charge_amount(subaddr)
    amount_left = amount
    token = None
    if subaddr:
        for tx in find_tx_for(subaddr):
            if tx['confirmations'] >= config.REQUIRED_CONFIRMATIONS and not tx['double_spend_seen']:
                amount_left -= tx['amount']
            if amount_left <= 0:
                amount_left = 0
        token = session.get('token')
        token = token.decode('ascii')
        if amount_left == 0 and not logic.has_exit(token):
            exit_addr = k8api.spawn_new_exit()
            logic.grant_exit_for(subaddr, token, exit_addr)
    return render_template("exit.html", token=token, exit_addr=exit_addr, amount=(amount_left / float(multiplier)), pay_address=pay_address)







if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logic.create_tables()
    app.run(config.WEB_HOST, port=config.WEB_PORT, debug=config.DEBUG)
