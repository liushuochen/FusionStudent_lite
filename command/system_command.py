"""
system commands.
    version --> show_version()
    system exit --> exit_system()
    system date --> system date()
"""

import datetime
import util
import json
from exception.fusionexception import InputError


def show_version():
    """
    Show FusionStudent Platform current version.
    :return: <str> current version.
    """
    url = util.root_path() + "/conf/host.version"
    version = open(url, "r").read()
    print(version)
    return


def exit_system():
    """
    Exit system(soft).
    :return: <boolean>
    """
    commit = input("Are you sure about exit system?(YES/NO) ").strip()
    if commit == "YES":
        pwd_conf_path = util.root_path() + "/conf/keypair.json"
        with open(pwd_conf_path, "r") as pwd_file:
            data = json.load(pwd_file)
        pwd_file.close()
        data["login"] = False
        with open(pwd_conf_path, "w") as pwd_file:
            json.dump(data, pwd_file, indent=4)
        pwd_file.close()

        print("Thanks.")
        return True
    elif commit == "NO":
        print("Welcome to back.")
        return False
    else:
        raise InputError("Invalid input %s. It must be YES or NO." % commit)


def system_date():
    """
    System date
    :return: <str> system date
    """
    now = datetime.datetime.now()
    return "%s/%s/%s %s:%s:%s CST" % (now.year, now.month, now.day, now.hour, now.minute,
                                  now.second)
