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
parser.add_argument('-v','--version', action='version',
                    version=f'%(prog)s {__version__}')

def add_versions(ctx):
    try:
        local_version = Path(VERSION_FILE).read_text().strip()
    except e:
        print(e)
        return ctx
    digits = re.findall(r'\d+', local_version)
    last = int(digits[-1])
    devNext = local_version.replace(f'dev{last}',f'dev{last+1}')
    ctx['__version__'] = local_version
    ctx['__version_digits__'] = digits
    ctx['__version_next__'] = devNext
    return ctx

def context(args):
    ctx = add_versions(dict(os.environ))
    for arg in vars(args):
        value = getattr(args, arg)
        ctx[arg] = getattr(args, arg)
    return ctx

def main():
    args = parser.parse_args()
    file = args.file
    ymm = load_file(file)
    ymm.env = context(args)
    actions = args.actions
    for action in actions:
        ymm.log(f'; {action}')
        results = ymm.run(action)

#main()
