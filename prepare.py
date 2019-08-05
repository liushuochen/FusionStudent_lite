"""
System prepare.
"""

import util
import os
import json
import logger.log as logs
from util import ClassInstance

def upload(classes, id_pools):

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

        logs.info("Upload class '%s' begin..." % uuid)
        body = {
            "uuid": uuid,
            "size": size,
            "name": name,
            "remark": remark
        }
        upload_class = ClassInstance(body)
        classes[uuid] = upload_class
        id_pools["class"].append(uuid)
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