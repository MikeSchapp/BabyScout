# conftest.py
import sys
import json
import requests
import os

class Pin:
    def __init__():
        pass

machine = type(sys)('machine')
machine.Pin = Pin

sys.modules['ujson'] = json
sys.modules['urequests'] = requests
sys.modules['uos'] = os
sys.modules['machine'] = machine