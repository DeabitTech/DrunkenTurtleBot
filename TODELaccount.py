import binanceWrapper


class Client(binanceWrapper.client.Client):
    __slots__ = [setOfKeysID, name, permissions, api_key, secret_key]


class Account:
    __slots__ = [accountID, accountDescription, stesOfKeys]
