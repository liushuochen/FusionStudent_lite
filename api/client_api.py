"""
client API
"""
import getpass
import util
import exception.fusionexception as fusionexp

PASSWORD_MIN_LENGTH = 6

def reset_password():
    """
    reset system login password.
    :return: <None>
    """
    old_pwd_input = getpass.getpass("Old password: ")
    old_pwd = util.get_password()
    if old_pwd != old_pwd_input:
        raise fusionexp.SystemError("Error password input.")

    new_pwd = getpass.getpass("New password: ")
    if not password_policy(new_pwd):
        raise fusionexp.SystemError("Password Policy Exception: password "
                                    "length must more than six.")

    verify_pwd = getpass.getpass("New password confirmation: ")
    if new_pwd != verify_pwd:
        raise fusionexp.InputError("Confirmation new password error.")

    return util.set_password(new_pwd)


def password_policy(pwd):
    """
    Check password policy.
    :param pwd: <str> password
    :return: <None>
    """
    if len(pwd) <= PASSWORD_MIN_LENGTH:
        return False

    return True