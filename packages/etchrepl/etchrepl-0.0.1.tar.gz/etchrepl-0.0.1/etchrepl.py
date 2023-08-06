import etch
import requests
import toml
import logging
import sys
import traceback

VERSION_URL = "https://raw.githubusercontent.com/GingerIndustries/Etch/main/pyproject.toml"

def versionCheck():
    logging.info("Checking version...")
    try:
        ver = toml.loads(requests.get(VERSION_URL).text)["tool"]["poetry"]["version"]
    except Exception as e:
        logging.warn("Unable to do version check.")
        logging.debug("An error occured while performing the version check:")
        logging.debug(str(e))
    else:
        if ver != etch.__version__:
            logging.info("Out of date!")
            return ver
    return False

def main(debug=False, no_update_check=False):
    if not no_update_check:
        version = versionCheck()
    else:
        logging.info("Version check disabled.")
        updates = False

    interpreter = etch.Interpreter(debug)
    print("Etch", etch.__version__, "running on", sys.platform, "(" + sys.implementation.name, ".".join([str(i) for i in sys.version_info[:3]]) + ").")
    print("Copyright Ginger Industries 2022.")
    print("Type /help for help.")
    if version:
        print("A new update for Etch is available! (" + etch.__version__ + ") -> (" + version + "). Use your package manager to update.")

    while True:
        i = input(">> ")
        if i.startswith("/"):
            c = i[1:].split(" ")
            command = c[0]
            params = c[1:]
            if command == "help":
                print(
'''Welcome to Etch! For language information go to https://etchlang.org or https://github.com/GingerIndustries/Etch.

Interpreter commands:
/help: Display this menu
/run <filename>: Run an Etch program
/updates: Check for updates
/version: Display version information''')
            elif command == "run":
                path = params.join(" ")
                if not path.endswith(".etch"):
                    path += ".etch"
                f = open(path)
                interpreter.run(f.read())
                f.close()
            elif command == "updates":
                v = versionCheck()
                if v:
                    print("A new update for Etch is available! (" + etch.__version__ + ") -> (" + version + "). Use your package manager to update.")
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