"""
clear commands.
    clear log <--all> <--error> <--info> <--warn> --> clear_logs()
"""

import util


def clear_logs(logs_type):
    """
    Clear logs.
    :param logs_type: <list> log type list.['all', 'info', 'error', 'warn']
    :return: <None>
    """
    if "all" in logs_type:
        util.clear_info_log()
        util.clear_error_log()
        util.clear_warn_log()
        return

    elif "info" in logs_type:
        util.clear_info_log()

    elif "error" in logs_type:
        util.clear_error_log()

    elif "warn" in logs_type:
        util.clear_warn_log()

    return