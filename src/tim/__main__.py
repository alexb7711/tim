import argparse

from pathlib import Path

#########################################################################################
# TIM CLASS
#########################################################################################


class Tim:
    ##===================================================================================
    #
    def __init__(self):
        return

    ##===================================================================================
    #
    def parse_options(self, args=None, values=None):
        """
        Define and parse `argparse` options for command-line usage.
        """

        # Program description and use
        usage = """%(prog)s [options]"""
        desc = "Tim the time tracking application."
        # Optional flags
        parser = argparse.ArgumentParser(prog="Tim", usage=usage, description=desc)
        parser.add_argument(
            "-a",
            "--add",
            dest="task",
            default=None,
            help="Create a task",
        )
        parser.add_argument(
            "-u",
            "--update",
            dest="task",
            default=None,
            help="Update a task",
        )
        parser.add_argument(
            "-s",
            "--summary",
            dest="std_output",
            default=False,
            help="Summarize what you did today",
        )

        # Parse the input arguments
        options = parser.parse_args(args, values)

        # Save the options
        return vars(options)


#########################################################################################
# SCRIPT
#########################################################################################


def run():
    tim = Tim()

    tim.parse_options()
