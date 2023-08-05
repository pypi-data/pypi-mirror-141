__version__ = "0.1.0"
from clean import *
from ffmpeg_concat import *
from reddit_archive import *

import appdirs

from pathlib import Path


# clean_config = Path(appdirs.user_config_dir() / "robolson" / "config" / "clean.toml")

# if not clean_config.exists():
#     with (
#         open(appdirs.user_config_dir() / "robolson" / "config" / "clean.toml", "w")
#     ) as fp:
#         fp.write(
#             """MONTHS = [
#   "Jan",
#   "Feb",
#   "March",
#   "April",
#   "May",
#   "June",
#   "July",
#   "Aug",
#   "Sept",
#   "Oct",
#   "Nov",
#   "Dec"
# ]
# EXCLUSIONS = [ "desktop.ini" ]
# CROWDED_FOLDER = 24

# [FILE_TYPES]
# Large_Files = [ ]
# delete_me = [ ]
# executables = [ ".exe", ".msi" ]
# media = [
#   ".jpg",
#   ".png",
#   ".gif",
#   ".mp3",
#   ".bit",
#   ".bmp",
#   ".txt",
#   ".pdf",
#   ".leo",
#   ".ogg",
#   ".mp4",
#   ".tif",
#   ".psd",
#   ".skba",
#   ".lip",
#   ".gdoc",
#   ".doc",
#   ".gslides",
#   ".gsheet",
#   ".docx",
#   ".odt",
#   ".m4b",
#   ".m4a"
# ]
# misc = [ ]
# programming = [
#   ".py",
#   ".ahk",
#   ".json",
#   ".ini",
#   ".csv",
#   ".nb",
#   ".cdf",
#   ".apk",
#   ".jonsl",
#   ".xml",
#   ".autoenv"
# ]
# syslinks = [ ".lnk", ".url" ]
# "zip files" = [ ".zip", ".7z", ".tar", ".rar", ".gz" ]
# """
#         )