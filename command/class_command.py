"""
class commands.
"""

import logger.log as logs
import os
import util
import json
from exception.fusionexception import ClassException


def create_class(body, id_pools, classes):
    """
    Create a class.
    :param body: <dict> req
    :param id_pools: <dict> id pools
    :param classes: <dict> class dict
    :return: <function> build_class()
    """

    class_id_pools = id_pools["class"]

    uuid = body["uuid"]
    if uuid in class_id_pools:
        raise ClassException("BadRequest: uuid '%s' has already exist." % uuid, 400)

    size = body["size"]
    if size is None:
        raise ClassException("BadRequest: class size is None.", 400)
    if size < 0:
        raise ClassException("BadRequest: class size is less than zero.", 400)

    new_class = util.ClassInstance(body)
    id_pools["class"].append(uuid)
    logs.info("Create class '%s' success." % uuid)

    return build_class(new_class, classes)


def build_class(new_class, classes):
    """
    Build a class.
    :param new_class: <Class> class instance
    :param classes: <dict> class dict
    :return: <None>
    """
    uuid = new_class.uuid
    classes[uuid] = new_class

    instance_path = util.root_path() + "/instance/%s" % uuid
    logs.info("instance path is %s" % instance_path)
    os.mkdir(instance_path)

    config_path = instance_path + "/class_config.json"

    data = {
        "uuid": uuid,
        "name": new_class.name,
        "size": new_class.size,
        "remark": new_class.remark
    }
    with open(config_path, "w") as conf:
        json.dump(data, conf, indent=4)
    conf.close()

    logs.info("Build class '%s' success." % uuid)
    print("Class %s create success." % uuid)

    return


def class_show(classes):
    """
    Show class list.
    :param classes: <dict> class info dict. uuid: class memory address
    :return: <None>
    """
    print("+" + "-" * 34 + "+")
    print("| uuid" + " " * 28 + " |")
    print("+" + "-" * 34 + "+")
    for item in classes:
        print("| " + item + " |")
        print("+" + "-" * 34 + "+")


def destroy_class(classes, uuid):
    """
    Destroy a class.
    :param classes: <dict> class info dict. uuid: class memory address
    :param uuid: <str> class uuid
    :return: <None>
    """
    logs.info("Begin to delete a class.")
    instance_path = util.root_path() + "/instance/%s" % uuid
    logs.info("Class info path is %s" % instance_path)
    os.system("rm -rf '%s'" % instance_path)
    del classes[uuid]
    logs.info("Delete class '%s' success." % uuid)
    print("Delete class '%s' success." % uuid)
    return


def class_info(classes, uuid):
    """
    Show class information.
    :param classes: <dict> class info dict. uuid: class memory address
    :param uuid: <str> class uuid
    :return: <None>
    """
    class_instance = classes[uuid]
    name = class_instance.name
    size = class_instance.size
    remark = class_instance.remark
    print("+" + "-" * 50)
    print("| uuid:   | %s" % uuid)
    print("| name:   | %s" % name)
    print("| size:   | %s" % size)
    print("| remark: | %s" % remark)
    print("+" + "-" * 50)

    return