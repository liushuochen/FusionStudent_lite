"""
doc commands.
"""

import webbrowser
import logger.log as logs
import configparser
import util

def open_web_use_doc():
    """
    Open use document in web.
    :return: <None>
    """
    url = util.root_path() + "/conf/sys.ini"
    conf = configparser.ConfigParser()
    conf.read(url)
    blog_path = conf.get("doc", "blog")
    if not webbrowser.open(blog_path):
        logs.error("Can not open web browser.")
        return

    return