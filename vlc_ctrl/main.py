from redcmd import CommandLine, CommandLineError

from .client import ClientSubcommands


def main():
	commandline = CommandLine()
	try:
		commandline.execute()
	except CommandLineError as e:
		pass

