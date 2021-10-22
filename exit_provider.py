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

import utils

logic.create_tables()

log = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = config.API_KEY


@app.route("/")
def exit_auth():
    pay_address = session.get("address", None)
    exit_addr = None
    if pay_address is None:
        result = utils.obtain_sub_address()
        if result:
            session['address'], session['subaddr'] = result
            session['token'] = hexlify(os.urandom(12))
            pay_address = result[0]

    amount = utils.get_charge_amount()
    amount_left = amount
    token = None
    subaddr = session.get("subaddr", None)

    if subaddr:
        for tx in utils.find_tx_for(subaddr):
            if tx['confirmations'] >= config.REQUIRED_CONFIRMATIONS and not tx['double_spend_seen']:
                amount_left -= tx['amount']
            if amount_left <= 0:
                amount_left = 0
        token = session.get('token')
        token = token.decode('ascii')
        if amount_left == 0 and not logic.has_exit(token):
            exit_addr = utils.obtain_exit()
            logic.grant_exit_for(subaddr, token, exit_addr)
    return render_template("exit.html", token=token, exit_addr=exit_addr, amount=utils.atomic_to_human(amount_left), pay_address=pay_address)







if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(config.WEB_HOST, port=config.WEB_PORT, debug=config.DEBUG)
