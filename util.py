"""
util method.
"""

import os
import string
import random
import command.class_command as class_cmd
import command.student_command as stu_cmd
import logger.log as logs
import json
from exception.fusionexception import ClassException, SystemError, StudentException

STUDENT_UUID_POOL = string.digits + string.ascii_lowercase
CLASS_UUID_POOL = string.ascii_uppercase + string.digits

CLASS_STATUS_OPENING = "Opening"
CLASS_STATUS_ERROR = "Error"
CLASS_STATUS_LOCK = "Lock"
CLASS_STATUS_DELETE = "Delete"

CLASS_STATUS_POOL = {
    CLASS_STATUS_OPENING,
    CLASS_STATUS_ERROR,
    CLASS_STATUS_LOCK
}

class ClassInstance():
    def __init__(self, body):
        self.uuid = body["uuid"]
        self.name = body["name"]
        self.size = body["size"]
        self.remark = body["remark"]
        if "student_number" in body:
            self.student_number = body["student_number"]
        else:
            self.student_number = 0
        self.status = body["status"]
        self.next = None


class Student():
    def __init__(self, body):
        self.uuid = body["uuid"]
        self.name = body["name"]
        self.sex = body["sex"]
        self.class_ins = body["class"]
        self.next = None



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
    :param classes: <dict> class dict
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

        if uuid not in id_pools:
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


def create(type, ins, **kwargs):
    """
    Create a class or student instance.
    :param type: <str> class or student type
    :param ins: <dict> instance dict
    :param kwargs: <dict>
    :return: <func> class_cmd.create_class / stu_cmd.create_student
    """
    if type == "class":
        if "uuid" in kwargs:
            uuid = kwargs["uuid"]
        else:
            uuid = generate_uuid(ins["classes"], id_type="class")

        if ("name" in kwargs) and (kwargs["name"] is not None):
            name = kwargs["name"]
        else:
            name = "class@%s" % uuid

        size = kwargs["size"]
        remark = kwargs["remark"]
        status = CLASS_STATUS_OPENING

        req = {
            "uuid": uuid,
            "name": name,
            "size": size,
            "remark": remark,
            "status": status
        }

        return class_cmd.create_class(req, ins)

    elif type == "student":
        if "uuid" in kwargs:
            uuid = kwargs["uuid"]
        else:
            uuid = generate_uuid(ins["students"], id_type="student")

        if ("name" in kwargs) and (kwargs["name"] is not None):
            name = kwargs["name"]
        else:
            name = "stu@%s" % uuid

        sex = kwargs["sex"]
        class_uuid = kwargs["class_id"]
        req = {
            "uuid": uuid,
            "name": name,
            "sex": sex,
            "class": class_uuid
        }

        return stu_cmd.create_student(req, ins)


def class_delete(ins, uuid):
    """
    Delete class.
    :param ins: <dict> instance dict
    :param uuid: <str> class uuid
    :return: <None>
    """
    if uuid not in ins["classes"]:
        logs.error("Delete class failed. uuid '%s' not exist!" % uuid)
        raise ClassException("BadRequest: uuid '%s' not exist!" % uuid, 401)

    status = get_class_info(uuid, ins)["status"]
    if status == CLASS_STATUS_LOCK:
        raise ClassException("Delete Class '%s' failed. Class is Lock!" % uuid
                             , 403)

    class_ins = ins["classes"][uuid]
    if class_ins.next is not None:
        logs.error("Delete class failed. class '%s' is not empty." % uuid)
        raise ClassException("Can not delete class. Class '%s' is not empty." % uuid,
                             500)

    return class_cmd.destroy_class(ins, uuid)


def show_class(ins, uuid):
    """
    show class information.
    :param ins: <dict> instance dict
    :param uuid: <str> class uuid
    :return: <None>
    """
    if uuid not in ins["classes"]:
        logs.error("Get class info failed. uuid '%s' not exist!" % uuid)
        raise ClassException("BadRequest: uuid '%s' not exist!" % uuid, 401)

    return class_cmd.class_info(ins, uuid)


def set_password(new_password):
    """
    Change admin password.
    :param old_password: <str> input old password.
    :param new_password: <str> input new password.
    :return: <None>
    """

    pwd_conf_path = root_path() + "/conf/keypair.json"
    with open(pwd_conf_path, "r") as pwd_file:
        data = json.load(pwd_file)
    pwd_file.close()

    data["password"] = new_password
    with open(pwd_conf_path, "w") as pwd_file:
        json.dump(data, pwd_file, indent=4)
    pwd_file.close()
    logs.info("Change admin password success.")
    return


def delete_student(stu_id, ins):
    """
    delete a student.
    :param stu_id: <str> student id
    :param ins: <dict> instance dict
    :return: <func> stu_cmd.destroy_student()
    """

    logs.info("Begin to delete student '%s'." % stu_id)
    if stu_id not in ins["students"]:
        logs.error("Delete student %s failed. Can not found student." % stu_id)
        raise StudentException("Student not found. Invalid student id '%s'." % stu_id,
                               400)

    class_info = get_class_info_by_student(stu_id, ins)
    class_status = class_info["status"]
    class_uuid = class_info["uuid"]
    if class_status == CLASS_STATUS_LOCK:
        raise StudentException("Delete student %s failed. Class %s is Lock."
                               % (stu_id, class_uuid), 402)
    class_ins = ins["classes"][class_uuid]
    pre1 = class_ins
    pre2 = pre1.next

    while pre2 is not None:
        if pre2.uuid == stu_id:
            pre1.next = pre2.next
            break
        else:
            pre1 = pre1.next
            pre2 = pre1.next

    student_path = root_path() + "/instance/%s/student/%s.json" % (class_uuid, stu_id)
    del ins["students"][stu_id]
    logs.info("Delete student '%s' success." % stu_id)

    class_ins.student_number -= 1
    class_cmd.set_param(class_uuid, "student_number", class_ins.student_number)

    return stu_cmd.destroy_student(student_path, stu_id)


def check_clear_all_instance():
    select = input("WARNING: It's a dangerous operation."
                   " Are you sure you still want to do this operation?(YES/NO) ").strip()

    if select == "YES":
        return True
    else:
        return False


def set_class_status(uuid, status, ins):
    """
    Set class status.
    :param uuid: <str> class uuid
    :param status: <str> new class status
    :param ins: <dict> instance dict
    :return: <None>
    """
    if status not in CLASS_STATUS_POOL:
        raise ClassException("Invalid new class status '%s'." % status, 404)

    current_status = get_class_info(uuid, ins)["status"]
    if current_status == status:
        raise ClassException("Set class '%s' status failed. Class status is %s now."
                             % (uuid, current_status), 403)

    return class_cmd.set_status(uuid, status, ins)


def lock_class(uuid, ins):
    """
    Lock class.
    :param uuid: <str> class uuid
    :param ins: <dict> instance dict
    :return: <None>
    """
    if uuid not in ins["classes"]:
        raise ClassException("Class '%s' not found." % uuid, 404)

    if get_class_info(uuid, ins)["status"] != CLASS_STATUS_OPENING:
        raise ClassException("Class %s is not Opening, can not Lock." % uuid, 402)

    return set_class_status(uuid, CLASS_STATUS_LOCK, ins)


def unlock_class(uuid, ins):
    """
    Unlock class.
    :param uuid: <str> class uuid
    :param ins: <dict> instance dict
    :return: <None>
    """
    if uuid not in ins["classes"]:
        raise ClassException("Class '%s' not found." % uuid, 404)

    if get_class_info(uuid, ins)["status"] != CLASS_STATUS_LOCK:
        raise ClassException("Class '%s' is not lock." % uuid, 402)

    return set_class_status(uuid, CLASS_STATUS_OPENING, ins)


def get_password():
    """
    Get system password.
    :return: <str> password
    """
    pwd_conf_path = root_path() + "/conf/keypair.json"
    with open(pwd_conf_path, "r") as pwd_file:
        data = json.load(pwd_file)
    pwd_file.close()

    system_password = data["password"]
    return system_password


def get_class_info(uuid, ins):
    """
    Get class information.
    :param uuid: <str> class uuid
    :param ins: <dict> instance dict
    :return: <dict> class information
    """
    if uuid not in ins["classes"]:
        logs.info("Get class info failed. Class %s not found." % uuid)
        raise ClassException("class %s not found." % uuid, 404)

    class_instance = ins["classes"][uuid]
    information = {
        "uuid": uuid,
        "name": class_instance.name,
        "size": class_instance.size,
        "remark": class_instance.remark,
        "student number": class_instance.student_number,
        "status": class_instance.status,
        "free": class_instance.size - class_instance.student_number
    }

    return information


def get_class_info_by_student(uuid, ins):
    """
    Get class information by student uuid.
    :param uuid: <str> student uuid
    :param ins: <dict> instance dict
    :return: <dict> class information
    """
    if uuid not in ins["students"]:
        logs.info("Get class info failed. Student %s not found." % uuid)
        raise StudentException("Student %s not found" % uuid, 404)

    student = ins["students"][uuid]
    class_uuid = student.class_ins

    return get_class_info(class_uuid, ins)