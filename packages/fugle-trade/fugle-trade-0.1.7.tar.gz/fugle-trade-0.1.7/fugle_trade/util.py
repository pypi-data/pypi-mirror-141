from getpass import getpass
from keyring import get_password, set_password
from hashlib import md5

def hash_value(val):
    # hashlib.md5("whatever your string is".encode('utf-8')).hexdigest()
    return md5(val.encode('utf-8')).hexdigest()


def ft_get_password(key, user_account):
    return get_password(key, user_account)


def ft_check_password(user_account):
    __check_password(user_account, get_password, set_password)


def ft_set_password(user_account):
    __set_password(user_account, get_password, set_password)

def __check_password(user_account, get_password, set_password):
    if not get_password("fugle_trade_sdk:account", user_account):
        set_password(
            "fugle_trade_sdk:account",
            user_account,
            getpass("Enter esun account password:\n"))

    if not get_password("fugle_trade_sdk:cert", user_account):
        set_password(
            "fugle_trade_sdk:cert",
            user_account,
            getpass("Enter cert password:\n"))


def __set_password(user_account,  get_password, set_password):
    set_password(
        "fugle_trade_sdk:account",
        user_account,
        getpass("Enter esun account password:\n"))
    set_password(
        "fugle_trade_sdk:cert",
        user_account,
        getpass("Enter cert password:\n"))
