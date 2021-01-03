#!/usr/bin/env python
# encoding: utf-8
# https://github.com/python/cpython/blob/3.9/Lib/configparser.py

if re.compile(r'^2.*').findall(sys.version):
    import ConfigParser as configparser
elif re.compile(r'^3.*').findall(sys.version):
    import configparser
else:
    print("Not support python 4 or more.")
    sys.exit(1)


class MyConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        configparser.ConfigParser.__init__(self, *args, **kwargs)

    def optionxform(self, optionstr):
        # return optionstr.lower()      # original
        return optionstr
    
    def read_file(self, *args, **kwargs):
        if re.compile(r'^2.*').findall(sys.version):
            return self.readfp(*args, **kwargs)
        elif re.compile(r'^3.*').findall(sys.version):
            return configparser.ConfigParser.read_file(self, *args, **kwargs)
        else:
            print("Not support python 4 or more.")
            sys.exit(1)


def read_config(file):
    config = MyConfigParser()
    # config = MyConfigParser(default_section='')
    # default_section is 'DEFAULT' by default, modify DEFAULT is a normal section;
    # default_section value is the special section holding default values for other sections and interpolation purposes.
    try:
        config.read_file(open(file))
    except configparser.DuplicateOptionError as e:
        print(e)
        config = configparser.ConfigParser()    # return an empty ConfigParser
    return config


def print_config(config):
    """print config.ini"""
    for section in config.sections():
        print("[{section}]".format(section=section))
        for opt, val in config.items(section):
            if config.has_section(section):
                print("{o} = {v}".format(o=opt, v=val))
        print()


def revert_config2dict(config):
    rlt = {}
    for section in config.sections():
        rlt[section] = {}
        for opt, val in config.items(section):
            rlt[section][opt] = val
            # rlt[section][opt] = config[section][opt]
    return rlt


def modify_example(config):
    # add section, case sensitive, include DEFAULT
    if not config.has_section('type'):
        config.add_section('type')

    # add or modify option in sepecific section
    config.set('type', 'stuno', '1021120')

    # get option in sepecific section
    if config.has_option('type', 'stuno'):
        print(config.get('type', 'stuno'))

    # remove option
    try:
        config.remove_option('log', 'path')
    except configparser.NoSectionError as e:
        print(e)
    else:
        print("delete succ")

    # remove section
    config.remove_section('port_list')


if __name__ == "__main__":
    config = read_config("./temp.1.ini")
    print_config(config)
    d = revert_config2dict(config)
    modify_example(config)
    # write to file
    config.write(open("./temp.2.ini", "w"))
