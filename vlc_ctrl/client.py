

from redcmd import Subcommand, subcmd, CommandLine, CommandLineError

from .player import Player


class ClientSubcommands(Subcommand):

	def __init__(self):
		self._player = Player()

	@subcmd
	def play(self, path=None, random=False, include=None, exclude=None, include_file=None, exclude_file=None):
		'''Play. Resume playback if paused. Optionally add new file/dir to the playlist or replace the current playlist.

		path: path to dir/file/url to be added
		replace: replace the current playlist'''

		filter = None
		if path is not None:
			filter = Filter(include=include, exclude=exclude, include_file=include_file, exclude_file=exclude_file)

		self._player.play(path, filter)


	@subcmd
	def pause(self):
		'Pause the playback.'

		self._player.pause()


	@subcmd
	def toggle(self):
		'Toggle between play and pause.'

		self._player.toggle()



	@subcmd
	def volume(self, level, fade=0):
		'''Get/Set the volume level.

		level: 	volume level (0 for mute, 1 for 100%)
			append % sign to mention level in percentage, e.g. 90%
			prefix +/- to increment / decrement current volume level, e.g. +10%, -0.1
		fade:	time in seconds to fade in / out to the specified level
			
			'''

		level_regex = re.compile("(+|-)(\d*\.\d+)(%)")
		#match and do stuff


	@subcmd
	def info(self):
		'Get the info about current track.'

		info = self._player.track_info()
		print info


	@subcmd
	def quit(self, condition=None, retry=(0, 0), fade=0):
		'''Quit vlc.
		
		condition: 	command to execute
				if return code of command = 0, quit vlc, else not
		fade:		time in seconds to fade out before quitting'''


		self._player.quit(condition, retry, fade)



	#later
	#@common
	#def instance(self, id=1, all):
		'''Common arguments for subcommands dealing with multiple instances.
		id: 	id / index of the player, mention multiple instances by a comma separated list
		all: 	all instances'''

		# New class needed to handle multiple instances and dispatch commands to them.
		# class Players
		# It'll just take the method name, look it up in Player instance and call it
		#
		# Need to fix redcmd for this kind of common argument functionality
		# Usage:
		#  @subcmd(common=instance)
		# This will append the arguments of the method to the subcommand.
		# It'll also append the argument help.
		# While calling the subcommand method, it'll call the common method with args first.

