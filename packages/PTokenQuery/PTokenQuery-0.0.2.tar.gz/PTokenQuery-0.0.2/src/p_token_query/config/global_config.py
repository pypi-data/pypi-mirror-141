import json
import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class AbiConfig:
    BEP20_ABI = json.loads(open(f'{basedir}/resources/BEP20.json', 'r').read())
