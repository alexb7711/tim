import optparse
import csv
import tim
import platform
import os

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
        self.m_prj_file = self._get_cache_directory() / Path("projects").with_suffix(".csv")

        # Database csv list of dictionaries standard table format
        self.m_db_csv  = [{"project": '', "charge": '', "start": '', "stop": ''}]
        self.m_prj_db_csv  = [{"project": '', "charge": ''}]

        # Create the directory if it does not exist
        self.m_db_path.mkdir(parents=True, exist_ok=True)

        # Parse the input arguments
        self.parse_options()

        return

    ##===================================================================================
    #
    def __del__(self):
        self._prompt("I'll be here... casting minutes into hours...", True)
        self._write_global_database()
        self._write_database()

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
        options, _ = parser.parse_args(args, values)

        # Pass the options to the runner
        self._run(options)

        return

    #####################################################################################
    # PRIVATE
    #####################################################################################

    ##===================================================================================
    #
    def _run(self, options: dict):
        # Print out the summary if asked to do so
        if options.summary:
            self._print_summary()
            return

        # Create the database if it does not exist
        if not self.m_db_file.is_file(): self._write_database()
        if not self.m_prj_file.is_file(): self._write_global_database()

        # Read in the database
        self.m_db_csv = self.m_db_csv + self._read_database(self.m_db_file)
        self.m_prj_db_csv = self.m_prj_db_csv + self._read_database(self.m_prj_file)
        for row in self.m_prj_db_csv: print(row)

        # Update the tasks first
        self._menu()

        return

    ##===================================================================================
    #
    def _read_database(self, path: str) -> dict:
        # Read in the database
        dict_csv = []
        with open(path, 'r', newline = '') as f:
            db_csv = csv.DictReader(f)

            for row in db_csv: dict_csv.append(row)

        return dict_csv

    ##===================================================================================
    #
    def _write_database(self):
        # Write to the database
        with open(self.m_db_file, 'w', newline = '') as f:
            if len(self.m_db_csv) == 0: return

            writer = csv.DictWriter(f, fieldnames=self.m_db_csv[0].keys())
            writer.writeheader()

            ## Print only non-empty rows
            for row in self.m_db_csv:
                print(row.values())
                if row and all(value for value in row.values()):
                    print("Writing!!!! ", row)
                    writer.writerow(row)
        return

    ##===================================================================================
    #
    def _write_global_database(self):
        # Write to the database
        with open(self.m_prj_file, 'w', newline = '') as f:
            if len(self.m_prj_db_csv) == 0: return

            writer = csv.DictWriter(f, fieldnames=self.m_prj_db_csv[0].keys())
            writer.writeheader()

            ## Print only non-empty rows
            for row in self.m_prj_db_csv:
                if row and all(value for value in row.values()):
                    writer.writerow(row)
        return

    ##===================================================================================
    #
    def _print_summary(self):
        print("SUMMARY")
        return

    ##===================================================================================
    #
    def _add(self):
        # Talk to Tim
        self._prompt("What is the project you are working on?", True)
        project = self._input("Enter a single word for the name")
        self._prompt("Whats the charge code for " + project + "?", True)
        charge_code = self._input("Enter the charge code")
        self._prompt("What time did you start work on " + project + " today?", True)
        start_time = self._input("Enter start time [HH:MM] (24 Hr)")

        # Update global project list
        self._add_or_append(self.m_prj_db_csv, {"project": project, "charge": charge_code})

        # Update daily task list
        self._add_or_append(self.m_db_csv, {"project": project, "charge": charge_code, "start": start_time, "stop": "00:00"})
        return

    ##===================================================================================
    #
    def _update(self):
        # Get the project
        project = self._print_projects()

        # Check if the task was started
        if self._project_started(project) >= 0:
            ## If it was, prompt for and end time
            print("GOTCHA")

        # Otherwise the task was not started yet
        else:
            ## Set the current time and tell the user
            print("hi")

        return

    ##===================================================================================
    #
    def _str_to_datetime(self):
        return

    ##===================================================================================
    #
    def _project_started(self, project: str) -> bool:
        for i, d in enumerate(self.m_db_csv):
            print(f"{d["project"] == project}")
            if d["project"] == project and d["start"] != "00:00" and d["stop"] == "00:00":
                print(i)
                return i
        ## The item was not found
        return -1

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

    ##===================================================================================
    #
    def _get_unique_project(self) -> list:
        return {d["project"]: d["charge"] for d in self.m_db_csv if "project" in d and d["project"]}

    ##===================================================================================
    #
    def _print_projects(self) -> str:
        projects = self._get_unique_project()

        self._prompt("What do you want to update?", True)
        for i, (t, c) in enumerate(projects.items()):
            self._prompt(f"{i}: {t} - {c}")

        pidx = int(self._input(f"[0-{len(projects)-1}]"))
        print(projects)
        return list(projects.keys())[pidx]

    ##===================================================================================
    #
    def _get_term_width(self):
        try:
            terminal_width = os.get_terminal_size().columns
        except OSError:
            # Fallback if terminal size cannot be determined (e.g., in some IDEs)
            terminal_width = 80
        return terminal_width

    ##===================================================================================
    #
    def _prompt_tim(self):
        tim = R"""
  .-````-.
 / -   -  \
|  .-. .- |
|  \o| |o (| 
\     ^    /
 '.  )--' /
   '-...-'
"""

        lines = tim.split("\n")
        for line in lines: print(" " * (self._get_term_width()-20) + line)

        return

    ##===================================================================================
    #
    def _prompt(self, txt: str, prompt_tim: bool = False):
        if prompt_tim: self._prompt_tim()

        lines = txt.split("\n")
        for line in lines: 
            if not line.isspace():
                line = "< " + line
                print(line.rjust(self._get_term_width()))
        return

    ##===================================================================================
    #
    def _input(self, txt: str = ""):
        if txt: txt = txt + " "
        p_txt = txt + "> "
        return input(p_txt)

    ##===================================================================================
    #
    def _menu(self):
        menu = """a: add project
u: update time
s: print summary
q: Bye Tim
        """
        while True:
            try:
                self._prompt(menu, True)
                task = self._input("Type a, u, s, or q")
            except KeyboardInterrupt:
                return

            match task.lower():
                case 'a':
                    self._add()
                case 'u':
                    self._update()
                case 's':
                    self._print_summary()
                case 'q':
                    print("Bye Tim");
                    return

        return

    ##===================================================================================
    #
    def _add_or_append(self, l: list, element: dict):
        # Convert dictionaries to a hashable format (tuple of sorted items)
        hashable_list = [tuple(sorted(d.items())) for d in l]
        hashable_new_dict = tuple(sorted(element.items()))

        if hashable_new_dict not in hashable_list:
            l.append(element)

        return l


#########################################################################################
# SCRIPT
#########################################################################################

tim_text = R"""
                                                         .-````-.
                                                        / -   -  \
   ▄      ▀                                            |  .-. .- |
 ▄▄█▄▄  ▄▄▄    ▄▄▄▄▄                                   |  \o| |o (|   <  Tim
   █      █    █ █ █                                   \     ^    /
   █      █    █ █ █                                    '.  )--' /
   ▀▄▄  ▄▄█▄▄  █ █ █  - the time keeping wizard           '-...-'
"""

def run():
    print(tim_text)

    tim = Tim()
    return
