import logging

from redcmd import CommandLine, CommandLineError
from redlib.misc import log

from .client import ClientSubcommands
from .version import __version__


def main():
	#log.start('stdout', loglevel=logging.DEBUG)
	#log.debug('log started')

	commandline = CommandLine(
			prog='vlc-ctrl',
			description='A command line utility to control a running vlc player instance.',
			version=__version__)

	try:
		commandline.execute()
	except CommandLineError as e:
		pass

