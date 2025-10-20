import csv

from pathlib import Path

##=======================================================================================
#
def _read_file(path: Path) -> list:
    """!
    Read from a CSV file as a list of dictionaries. The first line of the CSV will dictate
    what the keys are for each dictionary in the list.

    @param path Path to the CSV file

    @return The CSV file represented as a list of dictionaries
    """
    return

##=======================================================================================
#
def _write_file(path: Path, l: list) -> bool:
    """!
    Writes a list of dictionaries into a CSV file. This function will overwrite whatever 
    is in the file. Each dictionary in the list must share the same keys.

    @param path Path to the CSV file
    @param l List of dictionaries to be written

    @return True if successfully written, false otherwise
    """
    return
