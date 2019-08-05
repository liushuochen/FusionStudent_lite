"""
System prepare.
"""

import util
import os
import json
import logger.log as logs
from util import ClassInstance

def upload(ins):
    """
    upload resource.
    :param ins: <dict> instance dict
    :return: <None>
    """

    logs.info("Begin to upload class information.")
    instance_path = util.root_path() + "/instance"
    instance_list = os.listdir(instance_path)

    for instance in instance_list:
        config_path = instance_path + "/" +  instance + "/class_config.json"
        class_data = get_class_data(config_path)
        if class_data is None:
            continue

        uuid = instance.split("/")[-1]
        name = class_data["name"]
        size = class_data["size"]
        remark = class_data["remark"]
        student_number = class_data["student_number"]
        status = class_data["status"]

        logs.info("Upload class '%s' begin..." % uuid)
        body = {
            "uuid": uuid,
            "size": size,
            "name": name,
            "remark": remark,
            "student_number": student_number,
            "status": status
        }
        old_class = ClassInstance(body)
        students_path = instance_path + "/" + instance + "/student"
        upload_student(old_class, students_path, ins)
        ins["classes"][uuid] = old_class
        logs.info("Upload class '%s' success." % uuid)

    logs.info("Upload class information success.")




def get_class_data(url):
    """
    Get class config data.
    :param url: <str> class config url
    :return: <dict> config data
    """
    try:
        with open(url, "r") as conf:
            data = json.load(conf)
        conf.close()
    except Exception:
        data = None
        logs.warn("Upload class path '%s' do not exit." % url)

    return data


def get_student_data(url):
    """
    Get student config data.
    :param url: <str> student config url
    :return: <dict> config data
    """
    try:
        with open(url, "r") as conf:
            data = json.load(conf)
        conf.close()
    except Exception as e:
        data = None
        logs.warn("Get student data failed. WARNING: %s" % str(e))

    return data



def upload_student(class_instance, path, ins):
    """
    Upload student for class_instance.
    :param class_instance: <ClassInstance> class
    :param path: <str> student path
    :param ins: <dict> instance dict
    :return: <None>
    """
    if class_instance.student_number == 0:
        logs.info("Class %s is empty. Upload student success." % class_instance.uuid)
        return

    student_list = os.listdir(path)
    for student in student_list:
        uuid = (student.split("/")[-1])[:-5]
        config_path = path + "/" + student
        student_data = get_student_data(config_path)
        if student_data is None:
            continue

        name = student_data["name"]
        sex = student_data["sex"]
        logs.info("Upload student '%s' begin..." % uuid)
        body = {
            "uuid": uuid,
            "name": name,
            "sex": sex,
            "class": class_instance.uuid
        }
        student_instance = util.Student(body)
        if class_instance.next is None:
            class_instance.next = student_instance
        else:
            pre = class_instance.next
            class_instance.next = student_instance
            student_instance.next = pre
        ins["students"][uuid] = student_instance
        logs.info("Upload student '%s' success." % uuid)