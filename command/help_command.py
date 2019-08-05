"""
help commands.
    "help" -->  help_doc()
    "exit help" --> help_doc("exit")
"""

def help_doc(type="help"):
    """
    command "help".
        command list.
    :param type: <str> help type
    :return: <None>
    """
    message = ""
    if type == "help":
        message = """
            system help:  show FusionStudent Platform system operation to help.
            clear help:  clear resource operation to help.
            class help:  create instance operation to help.
        """

    elif type == "system":
        message = """
            system version:  show FusionStudent Platform system version.
            system exit:  exit FusionStudent Platform system.
            system date:  show current system date.
        """

    elif type == "clear":
        message = """
            clear log [--all] [--error] [--info] [--warn]:  clear logs.
                [--all]  clear info, error and warn logs
                [--info]  only clear info log
                [--error] only clear error log
                [--warn] only clear warn log
        """

    elif type == "class":
        message = """
            class create <--name> <--size> <--remark>:  create a class.
                <--name>  class name, str or integer param.
                <--size>  class size, integer param.
                <--remark>  class remark, str or integer param.
            
            class list: show class list.          
            class delete <uuid>:  delete a class.
                <uuid> class uuid.
            class show <uuid>:  show a class information.
                <uuid> class uuid.
        """

    print(message)
    return