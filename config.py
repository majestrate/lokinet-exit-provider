# the exit address to serve
EXIT_ADDR='changeme'

# account index in the wallet
ACCOUNT_INDEX = 0
# require this many confirmations before granting the exit
REQUIRED_CONFIRMATIONS = 4

# wallet rpc settings
WALLET_RPC_AUTH_FILE = '/path/to/wallet/rpc/login'
WALLET_RPC_HOST = '127.0.0.1'
WALLET_RPC_PORT = 22023

# the webapp secret key for sessions
API_KEY = 'changeme'

# database creds
DB_URL = 'host=/var/run/postgresql dbname=exit'


def wallet_url():
    """
    get the wallet rpc url
    """
    with open(WALLET_RPC_AUTH_FILE) as f:
        return 'http://{}@{}:{}/json_rpc'.format(f.read(), WALLET_RPC_HOST, WALLET_RPC_PORT)
