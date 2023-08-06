import subprocess
import sys
from .keys import *

class YMM:
    def __init__(self, yaml, debug=True):
        self.yaml = yaml
        self.env = {}

    def run(self,arg=False):
        if not arg in self.yaml: sys.exit('ERROR: action [{arg}] not found')
        actions = self.yaml[arg]
        results = [self.execute(cmd) for cmd in actions]
        return results

    def execute(self, cmd):
        if cmd[0] == kCall: return "\n".join(self.run(cmd[1:]))
        sub = cmd.format(**self.env)
        args = sub.split(" ")
        self.log(args)
        result = subprocess.run(args, stdout=subprocess.PIPE)
        msg = result.stdout.decode("utf-8").strip()
        print(f'# {msg}')
        self.env[kLast]=msg
        return msg

    def log(self, arg):
        if self.env.get(kLog, False): print(f'YMM.log {arg}')
