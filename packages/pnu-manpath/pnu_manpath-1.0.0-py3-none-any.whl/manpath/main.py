#!/usr/bin/env python
""" manpath - display search path for manual pages
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import getopt
import logging
import os
import re
import sys

import libpnu
import libmanconf

# Version string used by the what(1) and ident(1) commands:
ID = "@(#) $Id: manpath - display search path for manual pages v1.0.0 (March 6, 2022) by Hubert Tournier $"

# Default parameters. Can be overcome by environment variables, then command line options
parameters = {
    "Debug level": 0,
    "Locales mode": False,
    "Quiet mode": False,
    "Command flavour": "PNU",
}


################################################################################
def _display_help():
    """Displays usage and help"""
    if parameters["Command flavour"] in ("PNU", "bsd", "bsd:freebsd"):
        print("usage: manpath [--debug] [--help|-?] [--version]", file=sys.stderr)
        print("       [-L] [-d] [-q]", file=sys.stderr)
        print("       [--]", file=sys.stderr)
        print(
            "  ---------  -----------------------------------------------------",
            file=sys.stderr
        )
        print("  -L         Output manual locales list instead of the manual path", file=sys.stderr)
        print("  -d         Print extra debugging information", file=sys.stderr)
        print("  -q         Suppresses warning messages", file=sys.stderr)
        print("  --debug    Enable debug mode", file=sys.stderr)
        print("  --help|-?  Print usage and this help message and exit", file=sys.stderr)
        print("  --version  Print version and exit", file=sys.stderr)
        print("  --         Options processing terminator", file=sys.stderr)
    print(file=sys.stderr)


################################################################################
def _handle_interrupts(signal_number, current_stack_frame):
    """Prevent SIGINT signals from displaying an ugly stack trace"""
    print(" Interrupted!\n", file=sys.stderr)
    _display_help()
    sys.exit(0)


################################################################################
def _process_environment_variables():
    """Process environment variables"""
    # pylint: disable=C0103
    global parameters
    # pylint: enable=C0103

    if "MANPATH_DEBUG" in os.environ:
        logging.disable(logging.NOTSET)

    if "FLAVOUR" in os.environ:
        parameters["Command flavour"] = os.environ["FLAVOUR"].lower()
    if "MANPATH_FLAVOUR" in os.environ:
        parameters["Command flavour"] = os.environ["MANPATH_FLAVOUR"].lower()

    # Command variants supported:
    if parameters["Command flavour"] not in ("PNU", "bsd", "bsd:freebsd"):
        logging.critical("Unimplemented command FLAVOUR: %s", parameters["Command flavour"])
        sys.exit(1)

    logging.debug("_process_environment_variables(): parameters:")
    logging.debug(parameters)


################################################################################
def _process_command_line():
    """Process command line options"""
    # pylint: disable=C0103
    global parameters
    # pylint: enable=C0103

    # option letters followed by : expect an argument
    # same for option strings followed by =
    if parameters["Command flavour"] in ("PNU", "bsd", "bsd:freebsd"):
        character_options = "Ldq?"
        string_options = [
            "debug",
            "help",
            "version",
        ]

    try:
        options, remaining_arguments = getopt.getopt(
            sys.argv[1:], character_options, string_options
        )
    except getopt.GetoptError as error:
        logging.critical("Syntax error: %s", error)
        _display_help()
        sys.exit(1)

    for option, _ in options:

        if option == "-d":
            parameters["Debug level"] += 1

        elif option == "-L":
            parameters["Locales mode"] = True

        elif option == "-q":
            parameters["Quiet mode"] = True

        elif option == "--debug":
            logging.disable(logging.NOTSET)

        elif option in ("--help", "-?"):
            _display_help()
            sys.exit(0)

        elif option == "--version":
            print(ID.replace("@(" + "#)" + " $" + "Id" + ": ", "").replace(" $", ""))
            sys.exit(0)

    logging.debug("_process_command_line(): parameters:")
    logging.debug(parameters)
    logging.debug("_process_command_line(): remaining_arguments:")
    logging.debug(remaining_arguments)

    return remaining_arguments


################################################################################
def _add_directory(directory, manpath, debug_level):
    """Test if the given directory exist and is not already in the manpath. Adds it if needed"""
    found = False
    if os.path.isdir(directory):
        found = True
        if directory in manpath:
            if debug_level > 1:
                print("--   Skipping duplicate manpath entry %s" % directory, file=sys.stderr)
        else:
            if debug_level > 0:
                print("--   Adding %s to manpath" % directory, file=sys.stderr)
            manpath.append(directory)

    return manpath, found


################################################################################
def get_manpath(debug_level=0, quiet_mode=False):
    """Perform manpath processing"""
    manpath = []
    manual_path = ""

    if "MANPATH" in os.environ:
        manual_path = os.environ["MANPATH"]

        if not quiet_mode:
            print("(Warning: MANPATH environment variable set)", file=sys.stderr)
    else:
        if debug_level > 0:
            print("-- Searching PATH for man directories", file=sys.stderr)
        if "PATH" in os.environ:
            for part in os.environ["PATH"].split(os.pathsep):
                manpath, found = _add_directory(part + os.sep + "man", manpath, debug_level)
                if not found:
                    manpath, found = _add_directory(part + os.sep + "MAN", manpath, debug_level)
                if not found and part.endswith(os.sep + "bin"):
                    root = re.sub(r".bin", "", part)
                    manpath, found = _add_directory(
                        root + os.sep + "share" + os.sep + "man",
                        manpath,
                        debug_level
                    )
                    manpath, found = _add_directory(
                        root + os.sep + "man",
                        manpath,
                        debug_level
                    )
                if not found and os.altsep and part.endswith(os.altsep + "bin"):
                    root = re.sub(r".bin", "", part)
                    manpath, found = _add_directory(
                        root + os.altsep + "share" + os.altsep + "man",
                        manpath,
                        debug_level
                    )
                    manpath, found = _add_directory(
                        root + os.altsep + "man",
                        manpath,
                        debug_level
                    )

        if debug_level > 0:
            print("-- Adding default manpath entries", file=sys.stderr)
        for entry in (
            "/usr/share/man",
            "/usr/share/openssl/man",
            "/usr/local/share/man",
            "/usr/local/man"
        ):
            manpath, found = _add_directory(entry, manpath, debug_level)

        config_manpaths, _, _ = libmanconf.read_man_conf_files(
            debug_level,
            manpath_so_far=os.pathsep.join(manpath)
        )

        for part in config_manpaths.split(os.pathsep):
            manpath.append(part)

        manual_path = os.pathsep.join(manpath)

    if debug_level > 0:
        print("-- Using manual path: %s" % manual_path, file=sys.stderr)

    return manual_path


################################################################################
def get_locales(debug_level=0, quiet_mode=False):
    """Perform manpath -L processing"""
    manual_locales = ""

    if "MANLOCALES" in os.environ:
        manual_locales = os.environ["MANLOCALES"]

        if not quiet_mode:
            print("(Warning: MANLOCALES environment variable set)", file=sys.stderr)
    else:
        _, manual_locales, _ = libmanconf.read_man_conf_files(debug_level)

    if debug_level > 0:
        print("-- Available manual locales: %s" % manual_locales, file=sys.stderr)

    return manual_locales


################################################################################
def main():
    """The program's main entry point"""
    program_name = os.path.basename(sys.argv[0])

    libpnu.initialize_debugging(program_name)
    libpnu.handle_interrupt_signals(_handle_interrupts)
    _process_environment_variables()
    _ = _process_command_line()

    if parameters["Locales mode"]:
        print(
            get_locales(
                debug_level=parameters["Debug level"],
                quiet_mode=parameters["Quiet mode"]
            )
        )
    else:
        print(
            get_manpath(
                debug_level=parameters["Debug level"],
                quiet_mode=parameters["Quiet mode"]
            )
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
