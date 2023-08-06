import argparse
from .file import *

parser = argparse.ArgumentParser(description='Run actions.')
parser.add_argument('actions', metavar='action', nargs='+',
                    help='actions from ymm.yaml to execute')
parser.add_argument('-f','--file', default=DEFAULT_FILE,
                    help='YAML file of actions')
def main():
    args = parser.parse_args()
    actions = args.actions
    file = args.file
    ymm = load_file(file)
    for action in actions:
        ymm.log(action)
        result = ymm.run(action)
        [print(r) for r in result]

#main()
