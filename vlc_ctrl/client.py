import re
import textwrap

from redlib.system import terminalsize, is_py3
from redcmd import Subcommand, subcmd, CommandError

from .player_list import PlayerList
from .filter import Filter


class ClientSubcommands(Subcommand):

	def __init__(self):
		self._players = PlayerList()


	@subcmd
	def play(self, path=None, random=False, include=None, exclude=None, include_file=None, exclude_file=None):
		'''Play. Resume playback if paused. Optionally add new file/dir to the playlist.

		path: 		path to dir/file/url to be added
		include:	pattern(s) to include files/dirs, like, *.mp3,*.mp4
				separate mutliple patterns by comma (without spaces)
		exclude:	pattern(s) to exclude files/dirs, like, *.wav,data*
		include_file:	path to a file containing include patterns
		exclude_file:	path to a file containing exclude patterns
		random:		from the given path:
				either: randomly select a dir and play all files in it
				or: randomly select a file and play it'''

		filter = None
		if path is not None:
			filter = Filter(include=include, exclude=exclude, include_file=include_file, exclude_file=exclude_file, random=random)

		self._players.play(path, filter)


	@subcmd
	def pause(self):
		'Pause the playback.'

		self._players.pause()


	@subcmd
	def toggle(self):
		'Toggle between play and pause.'

		self._players.toggle()


	@subcmd
	def prev(self):
		'Go to previous track.'

		self._players.prev()


	@subcmd
	def next(self):
		'Go to next track.'

		self._players.next()


	@subcmd
	def stop(self):
		'Stop the playback.'

		self._players.stop()


	@subcmd
	def shuffle(self):
		'Shuffle the playlist.'

		self._players.shuffle()


	@subcmd
	def volume(self, level, fade='0'):
		'''Get/Set the volume level.

		level: 	volume level (0 for mute, 1 for 100%)
			append % sign to mention level in percentage, e.g. 90%
			prefix +/- to increment / decrement current volume level, e.g. +10%, -0.1
		fade:	time in seconds to fade in / out to the specified level'''

		match = self.validate_input("([+-])?(\\d*\\.?\\d+)(%)?", level, 'invalid volume level value, see help for valid format')
		
		vol = float(match.group(2))
		if match.group(3) == '%':
			vol = vol / 100

		sign = match.group(1)

		if sign == '+':
			vol = self._players.get_volume() + vol
		elif sign == '-':
			vol = self._players.get_volume() - vol

		match = self.validate_input("(\d+)", fade, 'fade value must be a number')
		fade = int(match.group(1))

		self._players.fade_volume(vol, fade)


	@subcmd
	def info(self):
		'Get info about the current track.'

		info = self._players.track_info()

		if all([v is None for v in info.values()]):
			print('track metadata not available')

		col1 = 10
		col2 = terminalsize.get_terminal_size()[0] - col1 - 3

		for name, value in info.items():
			if value is None:
				value = b''

			lines = None
			if not is_py3():
				lines = textwrap.wrap(value, col2)
			else:
				lines = textwrap.wrap(value.decode('utf-8'), col2)

			print("{0:<10}: {1}".format(name, lines[0] if len(lines) > 0 else ''))
			for line in lines[1:]:
				print("{0:<10}  {1}".format('', line))

	
	@subcmd
	def quit(self, condition=None, retry='1,0', fade='0'):
		'''Quit vlc.
		
		condition: 	command to execute
				if return code of command = 0, quit vlc, else not
		retry:		retry count, delay in seconds between retries
				e.g. --retry=5,30
		fade:		time in seconds to fade out before quitting'''


		match = self.validate_input("(\d+),(\d+)", retry, 'invalid input for retry, it must be in form: retry_count,delay_in_seconds, e.g. 3,30')
		retry = (int(match.group(1)), int(match.group(2)))

		match = self.validate_input("(\d+)", fade, 'fade value must be a number')
		fade = int(match.group(1))

		self._players.quit(condition, retry, fade)


	def validate_input(self, regex, input, err_msg):
		#import pdb; pdb.set_trace()
		match = re.compile(regex).match(input)

		if match is None:
			print(err_msg)
			raise CommandError()

		return match




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

