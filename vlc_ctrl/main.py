import logging
import sys

from redcmd.api import CommandLine, CommandLineError
from redlib.api.misc import log

from .client import ClientSubcommands
from .version import __version__


def main():
	commandline = CommandLine(
			prog='vlc-ctrl',
			description='A command line utility to control a running vlc player instance.',
			version=__version__,
			_to_hyphen=True)

	try:
		commandline.execute()
	except CommandLineError as e:
		sys.exit(1)
	sys.exit(0)

