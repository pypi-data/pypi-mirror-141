import re
import argparse
import pkg_resources
from pathlib import Path
from .keys import *
from .file import *

__version__ = pkg_resources.require("ymm")[0].version

parser = argparse.ArgumentParser(description='Run actions.')
parser.add_argument('actions', metavar='action', nargs='*',
                    help='actions from ymm.yaml to execute')
parser.add_argument('-f','--file', default=DEFAULT_FILE,
                    help='YAML file of actions')
parser.add_argument('-d','--debug', action='store_true',
                    help='print debugging information')
parser.add_argument('-l','--list', action='store_true',
                    help='list available actions')
parser.add_argument('-v','--version', action='version',
                    version=f'%(prog)s {__version__}')

def context(args):
    ctx = dict(os.environ)
    for arg in vars(args):
        value = getattr(args, arg)
        ctx[arg] = getattr(args, arg)
    return ctx

def main():
    args = parser.parse_args()
    file = args.file
    ymm = load_file(file)
    if args.list:
        print('actions:')
        for action in ymm.actions(): print(f'    - {action}')
    ymm.env = context(args)
    actions = args.actions
    for action in actions:
        print(f'; {action}')
        results = ymm.run(action)

#main()
