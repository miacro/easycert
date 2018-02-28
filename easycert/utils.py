import subprocess
import configparser
import os


class Utils():
    def run_command(command, dump=False, run=True):
        if run:
            subprocess.run(command, check=True)
        if not dump:
            return command

        result = ""
        if isinstance(command, list):
            length = len(command)
            for i in range(length):
                result += str(command[i])
                if i < length - 1:
                    result += " "
        else:
            result = command
        return result

    def read_config(filename="", content="", config=None):
        if not config:
            config = configparser.ConfigParser()
            config.optionxform = lambda option: option.strip()
        if content:
            config.read_string(content)
        else:
            config.read(Utils.abspath(filename))
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

    def write_config(config, filename="", file=None):
        if file:
            config.write(file)
            return
        with open(Utils.abspath(filename), "w") as stream:
            config.write(stream)

    def abspath(path):
        if not path:
            return ""
        return os.path.abspath(
            os.path.expandvars(os.path.expanduser(path)))
