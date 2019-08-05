"""
FusionStudent Platform
"""

import system.service as service
import command.system_command as system
from time import time


def system_pre(func):
    def wapper(*args, **kwargs):
        start = time()
        print("Welcome FusionStudent Platform system.")
        system.show_version()
        func(*args, **kwargs)
        print("SHUTDOWN")
        end = time()
        spend = end - start
        print("System run %.2f seconds." % spend)
        return
    return wapper


@ system_pre
def main():
    """
    Main Method.
    :return: <None>
    """
    service.fusion_system()
    return



if __name__ == "__main__":
    main()