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
            class help:  class operation to help.
            student help:  student operation to help.
            doc help:   documents shop.
        """

    elif type == "system":
        message = """
            system version:  show FusionStudent Platform system version.
            system exit:  exit FusionStudent Platform system.
            system date:  show current system date.
            system reset password:  reset admin password.
        """

    elif type == "clear":
        message = """
            clear log [--all] [--error] [--info] [--warn]:  clear logs.
                [--all]  clear info, error and warn logs
                [--info]  only clear info log
                [--error] only clear error log
                [--warn] only clear warn log

            clear system:  Clean up all the data on the FusionStudent Platform lite system.
                It's a dangerous operation.
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
            class lock <uuid>:  lock a class.
                <uuid> class uuid.
            class unlock <uuid>: unlock a class.
                <uuid> class uuid.
        """

    elif type == "student":
        message = """
            student create <--name> <--sex> <--class>:  create a student.
               <--name>  student name, str or integer param. 
               <--sex>  student sex, it must be 'boy' or 'girl'.
               <--class>  student class. class uuid.

            student list:  show student list.
            student delete <uuid>:  delete a student.
                <uuid> student uuid.

            student show <uuid>: show student information.
                <uuid> student uuid.
        """

    elif type == "doc":
        message = """
            doc:    open operation documents.
        """

    print(message)
    return