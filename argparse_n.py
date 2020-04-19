import argparse


parser = argparse.ArgumentParser()

# default value
parser.add_argument("-u", "--user", default="root",
                    help="the user login servers default: [root]")

# required value
parser.add_argument("-c", "--command", required=True,
                    help="exec command")

# group value
group = parser.add_mutually_exclusive_group()
group.add_argument("-j", "--json", action='store_true',
                   help="output json format")
group.add_argument("-p", "--plain", action='store_true',
                   help="output plain format")

# not group value
parser.add_argument("-v", "--version", action='store_true',
                    help="version info")

# choices
parser.add_argument("-t", "--type", choices=["tgw", "pgw"],
                    help="type of the gw")
# value type
parser.add_argument("-i", "--index", type=int,
                    help="index of the sth.")

args = parser.parse_args()
print(args)
# python argparse_n.py -c cmd
# Namespace(command='cmd', index=None, json=False, plain=False, type=None,
#           user='root', version=False)
