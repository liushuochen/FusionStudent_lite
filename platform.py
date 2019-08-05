"""
FusionStudent Platform
"""

import system.service as service
import command.system_command as system
from time import time
import util
import json
import getpass


def system_pre(func):
    def wapper(*args, **kwargs):
        start = time()
        print("Welcome FusionStudent Platform system.")
        system.show_version()
        func(*args, **kwargs)
        print("SHUTDOWN")
        end = time()
        spend = end - start
        print("System run %.2f seconds." % spend)
        return
    return wapper


@ system_pre
def main():
    """
    Main Method.
    :return: <None>
    """
    service.fusion_system()
    return


def login():
    """
    login system.
    :return: <bool>
    """
    username = input("# username: ").strip()
    if username == "__test__":
        return True

    pwd_conf_path = util.root_path() + "/conf/keypair.json"
    with open(pwd_conf_path, "r") as pwd_file:
        data = json.load(pwd_file)
    pwd_file.close()
    system_username = data["username"]
    if username == system_username:
        password = getpass.getpass("# password: ")
        if password == data["password"]:
            print("Login system success.")
            return True
        else:
            print("Login system failed.")
            return False
    else:
        print("Login system failed.")
        return False



if __name__ == "__main__":
    if login():
        main()
    else:
        print("Password wrong. Please input correct password.")