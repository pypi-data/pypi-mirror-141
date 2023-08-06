import etch
import requests
import toml
import logging
import sys
import argparse

__version__ = "0.1.2"

ETCH_URL = "https://raw.githubusercontent.com/GingerIndustries/Etch/main/pyproject.toml"
REPL_URL = "https://raw.githubusercontent.com/GingerIndustries/etchrepl/main/pyproject.toml"

parser = argparse.ArgumentParser(description="A repl for Etch.")
parser.add_argument("file", nargs="?", help="An etch file to run")
parser.add_argument("--interpreter-debug", action='store_true', help="Activate debugging")
parser.add_argument("--no-update-check", action='store_true', help="Don't check for updates")
#parser.add_argument("-v", "--verbose", action = "count", help="Increase verbosity", default=0)


def versionCheck(url, current):
    logging.info("Checking version for package " + url + "...")
    try:
        ver = toml.loads(requests.get(url).text)["tool"]["poetry"]["version"]
    except Exception as e:
        logging.warn("Unable to do version check for package: " + url)
        logging.debug("An error occured while performing the version check:")
        logging.debug(str(e))
    else:
        if ver != current:
            logging.info("Package " + url + " is out of date!")
            return ver
    return False

def main():
    args = parser.parse_args()
    logging.info("Starting")
    if not args.no_update_check:
        version = versionCheck(ETCH_URL, etch.__version__)
        replVersion = versionCheck(REPL_URL, __version__)
    else:
        logging.info("Version check disabled.")
        version = None

    interpreter = etch.Interpreter(args.interpreter_debug)
    if args.file:
        f = open(args.file)
        interpreter.run(f.read())
        f.close()
        return
    print("Etch", etch.__version__, "running on", sys.platform, "(" + sys.implementation.name, ".".join([str(i) for i in sys.version_info[:3]]) + ").")
    print("Copyright Ginger Industries 2022.")
    print("Type /help for help.")
    if version:
        print("A new update for Etch is available! (" + etch.__version__ + ") -> (" + version + "). Use your package manager to update.")
    if replVersion:
        print("A new update for the REPL is available! (" + __version__ + ") -> (" + replVersion + "). Use your package manager to update.")

    while True:
        try:
            i = input(">> ")
        except KeyboardInterrupt:
            print("Goodbye!")
            return
        if i.startswith("/"):
            c = i[1:].split(" ")
            command = c[0]
            params = c[1:]
            if command == "help":
                print(
'''Welcome to Etch! For language information go to https://etchlang.org or https://github.com/GingerIndustries/Etch.

Interpreter commands:
/help: Display this list
/run <filename>: Run an Etch program
/version: Display version information''')
            elif command == "run":
                path = " ".join(params)
                if not path.endswith(".etch"):
                    path += ".etch"
                f = open(path)
                interpreter.run(f.read())
                f.close()
            elif command == "version":
                print("Etch", etch.__version__, "running on", sys.platform, "(" + sys.implementation.name, ".".join([str(i) for i in sys.version_info[:3]]) + ").")
        else:
            try:
                interpreter.run(i)
            except KeyboardInterrupt:
                print("Program terminated.")
            except Exception as e:
                print(e)
            


if __name__ == "__main__":
    main()