import os
import sys
import contextlib

sys.path.append('c:/python38')
sys.path.append('c:/python38/scripts')

with contextlib.redirect_stdout(None):
	os.system('pip install --upgrade pip')
	os.system('pip install --upgrade scode')

__all__ = ['selenium', 'paramiko', 'telegram', 'dropbox', 'util']

__version__ = '0.1.3'

from . import selenium, paramiko, telegram, dropbox, util

from .util import *