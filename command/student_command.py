"""
student commands.
"""

import logger.log as logs
import util
import json
import os
import command.class_command as cls_cmd
from exception.fusionexception import ClassException, StudentException


def create_student(body, ins):
    """
    Create a student.
    :param body: <dict> req
    :param ins: <dict> instance dict
    :return: <function> build_student()
    """
    class_uuid = body["class"]
    if class_uuid not in ins["classes"]:
        logs.error("Create student failed. Point class '%s' not found." % class_uuid)
        raise ClassException("Class %s not found." % class_uuid, 400)

    if util.get_class_status(class_uuid, ins) == util.CLASS_STATUS_LOCK:
        raise StudentException("Create student failed. class '%s' status is Lock."
                               % class_uuid, 402)

    uuid = body["uuid"]
    if uuid in ins["students"]:
        logs.error("Create student failed. BadRequest: uuid '%s' has already exist." % uuid)
        raise StudentException("BadRequest: uuid '%s' has already exist." % uuid, 400)

    sex = body["sex"]
    if sex != "boy" and sex != "girl":
        logs.error("Create student failed. Invalid sex '%s' input. "
                  "It must be boy or girl." % sex)
        raise StudentException("BadRequest: invalid sex '%s' input." % sex, 400)

    class_ins = ins["classes"][class_uuid]
    if class_ins.size - class_ins.student_number <= 0:
        logs.error("Create student '%s' failed. Class '%s' is full."
                   % (uuid, class_uuid))
        raise StudentException("Class %s is full. "
                               "Can not create student in this class." % class_uuid, 500)

    new_student = util.Student(body)
    logs.info("Create student '%s' success." % uuid)

    return build_student(new_student, ins)


def build_student(stu, ins):
    """
    Build a student.
    :param stu: <Student> student instance
    :param ins: <dict> instance dict
    :return: <None>
    """
    class_uuid = stu.class_ins
    if ins["classes"][class_uuid].next is None:
        ins["classes"][class_uuid].next = stu
    else:
        pre = ins["classes"][class_uuid].next
        ins["classes"][class_uuid].next = stu
        stu.next = pre
    logs.info("Add student '%s' to class '%s' success." % (stu.uuid, class_uuid))

    student_path = util.root_path() + "/instance/%s/student/%s.json" % (class_uuid, stu.uuid)
    logs.info("student path is %s" % student_path)

    class_instance = ins["classes"][class_uuid]

    data = {
        "uuid": stu.uuid,
        "name": stu.name,
        "sex": stu.sex,
        "class": class_uuid
    }
    with open(student_path, "w") as stu_conf:
        json.dump(data, stu_conf, indent=4)
    stu_conf.close()

    class_instance.student_number += 1
    current_student_number = class_instance.student_number
    cls_cmd.set_param(class_uuid, "student_number", current_student_number)

    ins["students"][stu.uuid] = stu

    logs.info("Build student '%s' success." % stu.uuid)
    print("Student %s create success." % stu.uuid)

    return


def student_list(ins):
    """
    print student list.
    :param ins: <dict> instance dict
    :return: <None>
    """
    student_id_pool = ins["students"]
    print("+" + "-" * 34 + "+")
    print("| uuid" + " " * 28 + " |")
    print("+" + "-" * 34 + "+")
    for stu in student_id_pool:
        print("| " + stu + " |")
        print("+" + "-" * 34 + "+")

    return


def destroy_student(path, stu_id):
    """
    Destroy a student.
    :param path: <str> student config path.
    :param stu_id: <str> student id.
    :return: <None>
    """

    logs.info("Begin to destroy student '%s'." % stu_id)
    logs.info("path is %s" % path)
    if os.path.exists(path):
        os.system("rm -rf '%s'" % path)
    else:
        raise StudentException("Student '%s' config file not found." % stu_id, 500)
    logs.info("Destroy student '%s' success." % stu_id)
    print("Delete student '%s' success." % stu_id)

    return


def show_student(uuid, ins):
    """
    Show student information.
    :param uuid: <str> student uuid
    :param ins: <dict> instance dict
    :return: <None>
    """
    if uuid not in ins["students"]:
        logs.error("Student '%s' not found. Can not show this student." % uuid)
        raise StudentException("Student '%s' not found." % uuid, 404)

    stu = ins["students"][uuid]
    name = stu.name
    sex = stu.sex
    class_uuid = stu.class_ins

    print("+" + "-" * 9 + "+" + "-" * 40)
    print("| uuid:   | %s" % uuid)
    print("| name:   | %s" % name)
    print("| sex:    | %s" % sex)
    print("| class:  | %s" % class_uuid)
    print("+" + "-" * 9 + "+" + "-" * 40)

    return