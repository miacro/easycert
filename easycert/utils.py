import subprocess
import configparser


def runcommand(command, dump=False, run=True):
    if run:
        subprocess.run(command, check=True)
    if not dump:
        return command

    if isinstance(command, list) or isinstance(command, tuple):
        return " ".join(command)
    else:
        return command


def readconfig(filename):
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option.strip()
    config.read(filename)
    sections = config.sections()
    for section in sections:
        new_section = section.strip()
        if section == new_section:
            continue
        items = config.items(section)
        config.add_section(new_section)
        for item in items:
            config.set(new_section, item[0], item[1])
        config.remove_section(section)
    return config


def dumpconfig(config, filename):
    if not isinstance(filename, str):
        config.write(filename)
        return
    with open(filename, "wt") as stream:
        config.write(stream)
