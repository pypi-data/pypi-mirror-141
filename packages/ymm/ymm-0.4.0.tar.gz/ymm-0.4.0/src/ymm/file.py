import yaml
import os,shutil
from .keys import DEFAULT_FILE
from .ymm import YMM

def load_file(yaml_file=DEFAULT_FILE):
    print("Loading "+yaml_file)
    with open(yaml_file) as data:
        raw_yaml = yaml.full_load(data)
        return YMM(raw_yaml)

def run_file(yaml_file=DEFAULT_FILE):
    ymm = from_file(name, spark, folder)
    return ymm.run()
