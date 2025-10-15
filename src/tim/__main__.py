import optparse
import csv
import tim

from pathlib import Path

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
        # Update the tasks first
        for t in args: self._add_or_update(t)

        # Print out the summary if asked to do so
        if options.summary: self._print_summary()

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

#########################################################################################
# SCRIPT
#########################################################################################


def run():
    tim = Tim()

    tim.parse_options()
