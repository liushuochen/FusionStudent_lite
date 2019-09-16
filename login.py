"""
login system
"""

import util
import json
import getpass
import logger.log as logs

def login():
    """
    login system.
    :return: <bool>
    """
    username = input("# username: ").strip()
    if username == "root@fusionstudent":
        logs.info("--------------------------------\n" +
                  "user: %s login system succeed." % username)
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

            logs.info("--------------------------------\n" +
                      "user: %s login system succeed." % username)
            return True
        else:
            print("Login system failed.")
            print("Please input correct password.")
            return False
    else:
        print("Login system failed.")
        print("Please input correct username.")
        return False