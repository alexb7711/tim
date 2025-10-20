import platform

from pathlib import Path

def cache_directory(self, app_name: str = "") -> Path:
    """!
    Returns absolute path to the user's local cache directory. If the directory does not
    exist, this method will create it.

    @param app_name (Optional) Name of the application's cache directory

    @return Path object to the cache directory
    """
    home_dir = Path.home()

    # Retrieve the path to the cache directory depending on the platform
    if platform.system() == "Windows":
        ## On Windows, cache is typically in AppData/Local
        cache_dir = home_dir / "AppData" / "Local" / app_name / "Cache"
    else:
        ## On Linux and other Unix-like systems, follow XDG Base Directory Specification
        ## XDG_CACHE_HOME is preferred, otherwise ~/.cache
        xdg_cache_home = Path.home() / ".cache"
        cache_dir = xdg_cache_home / app_name

    # Create the directory if it does not exist
    cache_dir.mkdir(parents=True, exist_ok=True)

    return cache_dir
