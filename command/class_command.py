"""
class commands.
"""

import logger.log as logs
import os
import util
import json
from exception.fusionexception import ClassException


def create_class(body, ins):
    """
    Create a class.
    :param body: <dict> req
    :param ins: <dict> instance dict
    :return: <function> build_class()
    """

    uuid = body["uuid"]
    if uuid in ins["classes"]:
        raise ClassException("BadRequest: uuid '%s' has already exist." % uuid, 400)

    size = body["size"]
    if size is None:
        raise ClassException("BadRequest: class size is None.", 400)
    if size < 0:
        raise ClassException("BadRequest: class size is less than zero.", 400)

    new_class = util.ClassInstance(body)
    logs.info("Create class '%s' success." % uuid)

    return build_class(new_class, ins)


def build_class(new_class, ins):
    """
    Build a class.
    :param new_class: <Class> class instance
    :param ins: <dict> instance dict
    :return: <None>
    """
    uuid = new_class.uuid
    ins["classes"][uuid] = new_class

    instance_path = util.root_path() + "/instance/%s" % uuid
    logs.info("instance path is %s" % instance_path)
    os.mkdir(instance_path)

    student_path = instance_path + "/student"
    os.mkdir(student_path)

    config_path = instance_path + "/class_config.json"

    data = {
        "uuid": uuid,
        "name": new_class.name,
        "size": new_class.size,
        "student_number": 0,
        "remark": new_class.remark,
        "status": new_class.status
    }
    with open(config_path, "w") as conf:
        json.dump(data, conf, indent=4)
    conf.close()

    logs.info("Build class '%s' success. Class status is %s" % (uuid, new_class.status))
    print("Class %s create success." % uuid)

    return


def class_show(ins):
    """
    Show class list.
    :param ins: <dict> instance dict
    :return: <None>
    """
    print("+" + "-" * 34 + "+")
    print("| uuid" + " " * 28 + " |")
    print("+" + "-" * 34 + "+")
    for item in ins["classes"]:
        print("| " + item + " |")
        print("+" + "-" * 34 + "+")

    return


def destroy_class(ins, uuid):
    """
    Destroy a class.
    :param ins: <dict> instance dict
    :param uuid: <str> class uuid
    :return: <None>
    """
    logs.info("Begin to delete a class.")
    instance_path = util.root_path() + "/instance/%s" % uuid

    logs.info("Class info path is %s" % instance_path)
    os.system("rm -rf '%s'" % instance_path)
    del ins["classes"][uuid]
    logs.info("Delete class '%s' success." % uuid)
    print("Delete class '%s' success." % uuid)
    return


def class_info(ins, uuid):
    """
    Show class information.
    :param ins: <dict> instance dict
    :param uuid: <str> class uuid
    :return: <None>
    """
    class_instance = ins["classes"][uuid]
    name = class_instance.name
    size = class_instance.size
    remark = class_instance.remark
    free = size - class_instance.student_number
    status = class_instance.status
    print("+" + "-" * 9 + "+" + "-" * 40)
    print("| uuid:   | %s" % uuid)
    print("| name:   | %s" % name)
    print("| size:   | %s" % size)
    print("| remark: | %s" % remark)
    print("| free:   | %s" % free)
    print("| status: | %s" % status)
    print("+" + "-" * 9 + "+" + "-" * 40)

    return


def set_class(classes, uuid, **kwargs):
    """
    Set class params.
    :param classes: <dict> class info dict. uuid: class memory address
    :param uuid: <str> class uuid
    :param kwargs: <dict> set params.
    :return: <None>
    """
    for param in kwargs:
        if param == "size":
            classes[uuid].size = kwargs[param]
            set_param(uuid, param, kwargs[param])
        elif param == "name":
            classes[uuid].name = kwargs[param]
            set_param(uuid, param, kwargs[param])
        elif param == "remark":
            classes[uuid].name = kwargs[param]
            set_param(uuid, param, kwargs[param])
        else:
            logs.info("Modify class param failed. Invalid param '%s' request." % param)
            raise ClassException("Invalid param '%s' request." % param, 500)

    return


def set_param(uuid, param, value):
    """
    Set class param.
    :param uuid: <str> class uuid.
    :param param: <str> class param
    :param value: <str>/<int> class param value
    :return: <None>
    """

    conf_url = util.root_path() + "/instance/%s/class_config.json" % uuid
    with open(conf_url, "r") as conf_file:
        data = json.load(conf_file)
    conf_file.close()

    data[param] = value

    with open(conf_url, "w") as conf_file:
        json.dump(data, conf_file, indent=4)
    conf_file.close()
    logs.info("Set class '%s' param '%s' new value '%s' success." % (uuid, param, value))
    return