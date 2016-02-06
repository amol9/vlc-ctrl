from importlib import import_module
import sys

from redlib.api.system import is_linux


def setup_autocomp(commands_module, command_name, _to_hyphen=False):
	if not is_linux():
		return

	args = sys.argv

	if len(args) > 1 and args[1] == 'install':
		rc_api = None
		try:
			rc_api = import_module('redcmd.api')
		except ImportError as e:
			print('cannot setup autocomplete for %s'%command_name)
			return
		
		rc_api.setup_autocomp(commands_module, command_name, _to_hyphen=_to_hyphen)
		print('autocomplete setup for %s'%command_name)

