import subprocess
import configparser
import os


def runcommand(command, dump=False, run=True):
    if run:
        subprocess.run(command, check=True)
    if not dump:
        return command

    if isinstance(command, list) or isinstance(command, tuple):
        return " ".join(command)
    else:
        return command


def readconfig(filename, config=None):
    if not config:
        config = configparser.ConfigParser()
        config.optionxform = lambda option: option.strip()
    if os.path.exists(filename):
        config.read(filename)
    else:
        config.read_string(filename)
    for name in config.sections():
        stripname = name.strip()
        if stripname == name:
            continue
        config.add_section(stripname)
        for option, value in config[name].items():
            config.set(stripname, option, value)
        config.remove_section(name)
    return config


def dumpconfig(config, filename):
    if not isinstance(filename, str):
        config.write(filename)
        return
    with open(filename, "wt") as stream:
        config.write(stream)
