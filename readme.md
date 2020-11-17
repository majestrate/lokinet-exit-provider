# lokinet exit provider 

a (toy) vpn provider app server that takes ~~loki~~ oxen as payment.

## requirements

* cli wallet rpc
* postgresql
* python3
* python3-flask
* python3-psycopg2
* python3-requests
* [pylokimq](https://github.com/loki-project/loki-pylokimq)
* python3-gunicorn (optional)
* multipass (optional)

## demo setup

get the server source code:

    $ git clone https://github.com/majestrate/lokinet-exit
    $ cd lokinet-exit

configure the server:

    $ vi config.py

run the webapp:

    $ gunicorn exit_provider:app
    
run the exit auth server:

    $ python3 -m lokinet.auth --cmd ./logic.py --bind 10.0.3.1:5555


spin up an exit provider:

    $ multipass launch exit-provider --cloud-init exit.yaml


log into the exit provider:

    $ multipass shell exit-provider

configure lokinet exit to point lmq auth at `10.0.3.1:5555` in `/var/lib/lokinet/lokinet.ini`

    [network]
    exit=true
    keyfile=/var/lib/lokinet/exit.private
    hops=2
    auth=lmq
    auth-lmq=tcp://10.0.3.1:5555

find the exit's address inside the exit provider using:

    $ dig @127.3.2.1 +short -t cname localhost.loki
