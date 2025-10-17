import system

from pathlib import Path

def cache_directory(self, app_name: str = "") -> Path:
    """!
    Returns absolute path to the user's local cache directory. If the directory does not
    exist, this method will create it.

    @param app_name (Optional) Name of the application's cache directory

    @return Path object to the cache directory
    """
    return
