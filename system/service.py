"""
FusionStudent Platform system
"""

import command.help_command as help
import command.system_command as system
import command.clear_command as clears
import command.class_command as cls_cmd
import command.student_command as stu_cmd
import logger.log as logs
import traceback
import prepare
import util
import getpass
from exception.fusionexception import InputError, ClassException, StudentException
from exception.fusionexception import SystemError

def handle(command):
    command_list = command.split()
    command = " ".join(command_list)
    return command


def fusion_system():
    """
    Fusion system.
    :return: <None>
    """

    # set resource
    print("FusionStudent Platform System starting... please wait.")
    logs.info("FusionStudent Platform System start...")
    ins = {
        "classes": {},
        "students": {}
    }
    prepare.upload(ins)
    print("FusionStudent Platform System start success.")

    # running system
    while True:
        command = handle(input(">>> ").strip())

        if command == "help":
            help.help_doc()

        elif command == "__test":
            try:
                url = logs.get_path()
                print(url)
            except Exception as e:
                print(traceback.format_exc())
                continue

        elif command.startswith("system"):
            if command == "system version":
                system.show_version()
            elif command == "system help":
                help.help_doc("system")
            elif command == "system exit":
                try:
                    if system.exit_system():
                        logs.info("FusionStudent system soft shutdown.")
                        break
                    else:
                        continue
                except InputError as e:
                    print(str(e))
                    logs.error(traceback.format_exc())
                    continue

            elif command == "system date":
                print(system.system_date())

            elif command == "system set password":
                try:
                    old_pwd = getpass.getpass("old password: ")
                    new_pwd = getpass.getpass("new password: ")
                    util.set_password(old_pwd, new_pwd)
                except SystemError as e:
                    print("Change new password failed. Please input correct password.")
                    logs.error(str(e))
                    logs.error(traceback.format_exc())
                    continue

            else:
                print("Invalid command input '%s'. "
                      "Please input help for more information." % command)
                logs.error("Invalid command input: %s. 404" % command)
                continue

        elif command.startswith("clear"):
            if command.startswith("clear log"):
                try:
                    command_list = command.split()
                    if len(command_list) <= 2:
                        print("Lose argument for command 'clear log'. "
                              "Please input help for more information.")
                        logs.error("Clear logs failed.")
                        continue
                    command_list = command_list[2:]
                    logs_type = []
                    for i in command_list:
                        if i == "--error":
                            logs_type.append("error")
                        elif i == "--info":
                            logs_type.append("info")
                        elif i == "--warn":
                            logs_type.append("warn")
                        elif i == "--all":
                            logs_type.append("all")
                            break
                        else:
                            logs.error("Clear logs failed. "
                                       "BadRequest: Invalid argument '%s'." % i)
                            raise InputError("Invalid argument '%s'. "
                                             "Please input help for more information." % i)
                    clears.clear_logs(logs_type)
                    print("Clear log success.")
                except InputError as e:
                    print(str(e))
                    logs.error(str(e))
                    logs.error(traceback.format_exc())
                    continue

            elif command == "clear help":
                help.help_doc("clear")

            else:
                print("Invalid command input '%s'. "
                      "Please input help for more information." % command)
                logs.error("Invalid command %s input." % command)

        elif command.startswith("class"):
            if command.startswith("class create"):
                try:
                    command_list = command.split()[2:]
                    index = 0
                    type = "class"
                    name = None
                    size = None
                    remark = None
                    while index < len(command_list):
                        if command_list[index] == "--name":
                            index += 1
                            name = command_list[index]
                        elif command_list[index] == "--size":
                            index += 1
                            size = int(command_list[index])
                        elif command_list[index] == "--remark":
                            index += 1
                            remark = command_list[index]
                        else:
                            raise InputError("Invalid param %s. "
                                             "Please input 'help' for more information."
                                             % command_list[index])
                        index += 1

                    util.create(type, ins, name=name, size=size,
                                remark=remark)
                except InputError as e:
                    print(str(e))
                    continue
                except ValueError:
                    print("BadRequest: Size must be an integer number.")
                    logs.error("Create class failed.\n"
                               "BadRequest: Size must be an integer number.")
                    logs.error(traceback.format_exc())
                except ClassException as e:
                    print(str(e))
                    logs.error("Create class failed. %s" % str(e))
                    logs.error(traceback.format_exc())

            elif command == "class help":
                help.help_doc("class")

            elif command == "class list":
                cls_cmd.class_show(ins)

            elif command.startswith("class delete"):
                try:
                    command_list = command.split()
                    if len(command_list) != 3:
                        print("Invalid command input '%s'. "
                              "Please input help for more information." % command)
                        logs.error("Invalid command %s input." % command)
                        continue

                    uuid = command_list[-1]
                    util.class_delete(ins, uuid)
                except ClassException as e:
                    print(str(e))
                    continue

            elif command.startswith("class show"):
                try:
                    command_list = command.split()
                    if len(command_list) != 3:
                        print("Invalid command input '%s'. "
                              "Please input help for more information." % command)
                        logs.error("Invalid command %s input." % command)
                        continue

                    uuid = command_list[-1]
                    util.show_class(ins, uuid)
                except ClassException as e:
                    print(str(e))
                    continue

            else:
                print("Invalid command input '%s'. "
                      "Please input help for more information." % command)
                logs.error("Invalid command %s input." % command)

        elif command.startswith("student"):
            if command == "student help":
                help.help_doc("student")

            elif command.startswith("student create"):
                try:
                    command_list = command.split()[2:]
                    index = 0
                    type = "student"
                    name = None
                    sex = None
                    class_id = None
                    while index < len(command_list):
                        if command_list[index] == "--name":
                            index += 1
                            name = command_list[index]
                        elif command_list[index] == "--sex":
                            index += 1
                            sex = command_list[index]
                        elif command_list[index] == "--class":
                            index += 1
                            class_id = command_list[index]
                        else:
                            raise InputError("Invalid param %s. "
                                             "Please input 'help' for more information."
                                             % command_list[index])
                        index += 1

                    util.create(type, ins, name=name, sex=sex, class_id=class_id)
                except InputError as e:
                    print(str(e))
                    continue
                except ClassException as e:
                    print(str(e))
                    continue
                except StudentException as e:
                    print(str(e))
                    continue

            elif command == "student list":
                stu_cmd.student_list(ins)

            elif command.startswith("student delete"):
                try:
                    command_list = command.split()
                    if len(command_list) != 3:
                        raise InputError("Invalid command '%s' input. "
                                         "Please input help for more information.")
                    uuid = command_list[-1]
                    util.delete_student(uuid, ins)

                except InputError as e:
                    print(str(e))
                    continue
                except StudentException as e:
                    print(str(e))
                    continue

            elif command.startswith("student show"):
                try:
                    command_list = command.split()
                    if len(command_list) != 3:
                        raise InputError("Invalid command '%s' input. "
                                         "Please input help for more information.")
                    uuid = command_list[-1]
                    stu_cmd.show_student(uuid, ins)

                except InputError as e:
                    print(str(e))
                    logs.error(str(e))
                    logs.error(traceback.format_exc())
                    continue
                except StudentException as e:
                    print(str(e))
                    logs.error(str(e))
                    logs.error(traceback.format_exc())
                    continue


            else:
                print("Invalid command input '%s'. "
                      "Please input help for more information." % command)
                logs.error("Invalid command %s input." % command)

        else:
            if command == "":
                continue
            else:
                print("Invalid command input '%s'. "
                      "Please input help for more information." % command)
                logs.error("Invalid command %s input." % command)