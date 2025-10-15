import optparse
import csv
import tim
import platform

from pathlib import Path
from datetime import datetime

#########################################################################################
# TIM CLASS
#########################################################################################


class Tim:

    #####################################################################################
    # PUBLIC
    #####################################################################################

    ##===================================================================================
    #
    def __init__(self):
        # Set the database paths
        self.m_db_path = self._get_cache_directory() / Path(str(datetime.now().year))
        self.m_db_file = self.m_db_path / Path(str(datetime.now().month)).with_suffix(".csv")

        # Database csv list of dictionaries standard table format
        self.m_db_csv  = [{"task": None, "charge": None, "start": None, "stop": None}]

        # Create the directory if it does not exist
        self.m_db_path.mkdir(parents=True, exist_ok=True)

        # Parse the input arguments
        self.parse_options()

        return

    ##===================================================================================
    #
    def parse_options(self, args=None, values=None):
        """
        Define and parse `optparse` options for command-line usage.
        """

        # Program description and use
        usage = """%prog [OPTIONS] [TASKNAME]"""
        desc = "Tim the time tracking application."
        ver = str(tim.__version__)
        # Optional flags
        parser = optparse.OptionParser(prog="Tim", usage=usage, description=desc, version=ver)
        parser.add_option(
            "-s",
            "--summary",
            dest="summary",
            default=False,
            action="store_true",
            help="Summarize what you did today",
        )

        # Parse the input arguments
        options, args = parser.parse_args(args, values)

        # Pass the options to the runner
        self._run(options, args)

        return

    #####################################################################################
    # PRIVATE
    #####################################################################################

    ##===================================================================================
    #
    def _run(self, options: dict, args: list):
        # Read in the database
        self._read_database()

        # Update the tasks first
        for t in args: self._add_or_update(t)

        # Print out the summary if asked to do so
        if options.summary: self._print_summary()

        return

    ##===================================================================================
    #
    def _read_database(self):
        # Create the database if it does not exist
        if not self.m_db_file.is_file():
            self._write_database()

        # Read in the database
        with open(self.m_db_file, 'r', newline = '') as f:
            m_db_csv = csv.DictReader(f)

        return

    ##===================================================================================
    #
    def _write_database(self):
        # Write to the database
        with open(self.m_db_file, 'w', newline = '') as f:
            writer = csv.DictWriter(f, fieldnames=self.m_db_csv[0].keys())
            writer.writeheader()
            writer.writerows(self.m_db_csv)
        return

    ##===================================================================================
    #
    def _add_or_update(self, task: str):
        print(task)
        return

    ##===================================================================================
    #
    def _print_summary(self):
        print("SUMMARY")
        return

    ##===================================================================================
    #
    def _get_cache_directory(self, app_name="tim") -> Path:
        """
        Returns a Path object representing the application's cache directory
        for the current user, handling both Windows and Linux.
        """
        home_dir = Path.home()

        # Retrieve the path to the cache directory depending on the platform
        if platform.system() == "Windows":
            # On Windows, cache is typically in AppData/Local
            cache_dir = home_dir / "AppData" / "Local" / app_name / "Cache"
        else:
            # On Linux and other Unix-like systems, follow XDG Base Directory Specification
            # XDG_CACHE_HOME is preferred, otherwise ~/.cache
            xdg_cache_home = Path.home() / ".cache"
            cache_dir = xdg_cache_home / app_name

        # Create the directory if it does not exist
        cache_dir.mkdir(parents=True, exist_ok=True)

        return cache_dir

#########################################################################################
# SCRIPT
#########################################################################################


def run():
    tim = Tim()
    return
