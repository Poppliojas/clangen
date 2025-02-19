import logging
import os
import subprocess
import sys
from configparser import ConfigParser

logger = logging.getLogger(__name__)

VERSION_NAME = "0.8.0"
SAVE_VERSION_NUMBER = 1  # This is saved in the clan save-file, and is used for save-file converstion. 

def get_version_info():
    if get_version_info.instance is None:
        is_source_build = False
        version_number = VERSION_NAME
        release_channel = False
        upstream = ""

        if not getattr(sys, 'frozen', False):
            is_source_build = True

        if os.path.exists("version.ini"):
            version_ini = ConfigParser()
            version_ini.read("version.ini", encoding="utf-8")
            version_number = version_ini.get("DEFAULT", "version_number")
            release_channel = version_ini.get("DEFAULT", "release_channel")
            upstream = version_ini.get("DEFAULT", "upstream")
        else:
            try:
                version_number = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
            except:
                logger.exception("Git CLI invocation failed")
        get_version_info.instance = VersionInfo(is_source_build, release_channel, version_number, upstream)
    return get_version_info.instance


get_version_info.instance = None


class VersionInfo:
    def __init__(self, is_source_build: bool, release_channel: str, version_number: str, upstream: str):
        self.is_source_build = is_source_build
        self.release_channel = release_channel
        self.version_number = version_number
        self.upstream = upstream

    def is_dev(self) -> bool:
        if self.release_channel != "stable":
            return True
        else:
            return False
