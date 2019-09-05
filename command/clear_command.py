"""
clear commands.
    clear log <--all> <--error> <--info> <--warn> --> clear_logs()
"""

import util
import time
import logger.log as logs
import json


def clear_logs(logs_type):
    """
    Clear logs.
    :param logs_type: <list> log type list.['all', 'info', 'error', 'warn']
    :return: <None>
    """
    if "all" in logs_type:
        util.clear_info_log()
        util.clear_error_log()
        util.clear_warn_log()
        return

    elif "info" in logs_type:
        util.clear_info_log()

    elif "error" in logs_type:
        util.clear_error_log()

    elif "warn" in logs_type:
        util.clear_warn_log()

    return


def clear_system(ins):
    """
    Clear system
    :param ins: instance dict
    :return: <None>
    """
    time.sleep(5)

    try:
        # clean up students
        student_uuid_set = set(ins["students"])
        for item in student_uuid_set:
            util.delete_student(item, ins)

        # clean up class
        class_uuid_set = set(ins["classes"])
        for item in class_uuid_set:
            util.class_delete(ins, item)

        # clean up logs
        clear_logs("all")

        # set up keypair configure file
        pwd_conf_path = util.root_path() + "/conf/keypair.json"
        with open(pwd_conf_path, "r") as pwd_file:
            data = json.load(pwd_file)
        pwd_file.close()
        data["login"] = False
        with open(pwd_conf_path, "w") as pwd_file:
            json.dump(data, pwd_file, indent=4)
        pwd_file.close()

        return True
    except Exception:
        print("clear system failed.")
        logs.info("clear system failed.")
        return False