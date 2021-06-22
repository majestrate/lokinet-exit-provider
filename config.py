

import os


getenv = lambda name, fallback, mkval: name in os.environ and mkval(os.environ[name]) or mkval(fallback)

mkstr = lambda data : data is not None and str(data) or None

mkbool = lambda data : data is not None and bool(data.lower() == 'true' or data.lower() != 'false') or False

# account index in the wallet
ACCOUNT_INDEX = getenv('LN_EXIT_ACCOUNT_INDEX', '0', int)
# require this many confirmations before granting the exit
REQUIRED_CONFIRMATIONS = getenv('LN_EXIT_CONFIRMATIONS', '4', int)

# wallet rpc settings
WALLET_RPC_AUTH_FILE = getenv("WALLET_RPC_AUTH_FILE", None, mkstr)
WALLET_RPC_AUTHINFO = getenv("WALLET_RPC_AUTHINFO", None, mkstr)
WALLET_RPC_HOST = getenv("WALLET_RPC_HOST", '127.0.0.1', mkstr)
WALLET_RPC_PORT = getenv("WALLET_RPC_PORT", '22023', int)

# the webapp secret key for sessions
API_KEY = getenv("LN_EXIT_APIKEY", 'changeme', mkstr)

# database creds
DB_URL = getenv("LN_EXIT_DB_URL", 'host=/var/run/postgresql dbname=exit', mkstr)


# bind web server to host
WEB_HOST = getenv("LN_EXIT_WEB_HOST", '127.0.0.1', mkstr)
# bind web server to port
WEB_PORT = getenv("LN_EXIT_WEB_PORT", '4000', int)

# run the webapp in debug mode?
DEBUG = getenv("LN_EXIT_DEBUG", 'false', mkbool)

def wallet_url():
    """
    get the wallet rpc url
    """
    authinfo = WALLET_RPC_AUTHINFO
    if WALLET_RPC_AUTH_FILE:
        with open(WALLET_RPC_AUTH_FILE) as f:
            authinfo = f.read()
    return 'http://{}@{}:{}/json_rpc'.format(f.read(), WALLET_RPC_HOST, WALLET_RPC_PORT)
