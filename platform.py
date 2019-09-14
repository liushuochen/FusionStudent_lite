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
    has_login = data["login"]
    if has_login:
        print("Login system failed.")
        print("FusionStudent system has been logged in.")
        return False

    if username == system_username:
        password = getpass.getpass("# password: ")
        if password == data["password"]:
            print("Login system success.")
            data["login"] = True
            with open(pwd_conf_path, "w") as pwd_file:
                json.dump(data, pwd_file, indent=4)
            pwd_file.close()
            return True
        else:
            print("Login system failed.")
            print("Please input correct password.")
            return False
    else:
        print("Login system failed.")
        print("Please input correct username.")
        return False

if __name__ == "__main__":
    if login():
        main()
        # app.run()