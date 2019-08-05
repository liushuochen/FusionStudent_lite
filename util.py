"""
util method.
"""

import os
import string
import random
import command.class_command as class_cmd
import logger.log as logs
from exception.fusionexception import ClassException

STUDENT_UUID_POOL = string.digits + string.ascii_lowercase
CLASS_UUID_POOL = string.ascii_uppercase + string.digits


class ClassInstance():
    def __init__(self, body):
        self.uuid = body["uuid"]
        self.name = body["name"]
        self.size = body["size"]
        self.remark = body["remark"]
        self.next = None
        self.front = None


def root_path():
    """
    Get FusionStudent project root url.
    :return: <str> root url
    """
    url = os.path.abspath("")
    return url


def generate_uuid(id_pools, id_type="student"):
    """
    Generate instance uuid.
    :param id_pools: <dict> instance id pools
    :param id_type: <str> instance uuid type
    :return: <str> instance uuid
    """
    def generate_temp_uuid(length=4, id_type="student"):
        """
        Generate temp id.
        :param length: <int> id length
        :param id_type: <str> instance uuid type
        :return: <str> temp id
        """
        if id_type == "student":
            temp_uuid = ""
            for i in range(length):
                temp_uuid += random.choice(STUDENT_UUID_POOL)
            return temp_uuid

        elif id_type == "class":
            temp_uuid = ""
            for i in range(length):
                temp_uuid += random.choice(CLASS_UUID_POOL)
            return temp_uuid

        else:
            return ""

    uuid_list = [None] * 5

    while True:
        uuid = ""
        for i in range(len(uuid_list)):
            if i == 0 or i == 4:
                uuid_list[i] = generate_temp_uuid(8, id_type)
            else:
                uuid_list[i] = generate_temp_uuid(4, id_type)

        for temp_uuid in uuid_list:
            uuid = uuid + temp_uuid + "-"

        if uuid not in id_pools[id_type]:
            break

    uuid = uuid.strip("-")
    return uuid



def clear_info_log():
    """
    Clear info log.
    :return: <None>
    """
    info_log_url = root_path() + "/log/info.log"
    if os.path.exists(info_log_url):
        open(info_log_url, "w").write('')

    return


def clear_error_log():
    """
    Clear error log.
    :return: <None>
    """
    error_log_url = root_path() + "/log/error.log"
    if os.path.exists(error_log_url):
        open(error_log_url, "w").write('')

    return


def clear_warn_log():
    """
    Clear warn log.
    :return: <None>
    """
    warn_log_url = root_path() + "/log/warn.log"
    if os.path.exists(warn_log_url):
        open(warn_log_url, "w").write('')

    return


def create(type, id_pools, classes, **kwargs):
    if type == "class":
        if "uuid" in kwargs:
            uuid = kwargs["uuid"]
        else:
            uuid = generate_uuid(id_pools, id_type="class")

        if ("name" in kwargs) and (kwargs["name"] is not None):
            name = kwargs["name"]
        else:
            name = "class@%s" % uuid

        size = kwargs["size"]
        remark = kwargs["remark"]

        req = {
            "uuid": uuid,
            "name": name,
            "size": size,
            "remark": remark
        }

        return class_cmd.create_class(req, id_pools, classes)


def class_delete(classes, uuid):
    """
    Delete class.
    :param classes: <dict> class info dict. uuid: class memory address
    :param uuid: <str> class uuid
    :return: <None>
    """
    if uuid not in classes:
        logs.error("Delete class failed. uuid '%s' not exist!" % uuid)
        raise ClassException("BadRequest: uuid '%s' not exist!" % uuid, 401)

    return class_cmd.destroy_class(classes, uuid)


def show_class(classes, uuid):
    """
    show class information.
    :param classes: <dict> class info dict. uuid: class memory address
    :param uuid: <str> class uuid
    :return: <None>
    """
    if uuid not in classes:
        logs.error("Get class info failed. uuid '%s' not exist!" % uuid)
        raise ClassException("BadRequest: uuid '%s' not exist!" % uuid, 401)

    return class_cmd.class_info(classes, uuid)