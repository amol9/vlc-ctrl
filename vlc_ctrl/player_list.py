from time import sleep

from .player import Player, PlayerError
from redcmd import CommandError


class PlayerListError(Exception):
	pass


class PlayerList:
	launch_on_no_service = ['play']

	def __init__(self):
		self._list = []


	def select(self, id, all=False):
		pass


	def __getattr__(self, name):
		if len(self._list) == 0:
			self._list.append(Player())

		attr = getattr(self._list[0], name, None)

		if attr is None:
			raise PlayerListError('no such member: %s'%name)

		def wrapped(*args, **kwargs):
			try:
				self._list[0].get_dbus_interface()
			except PlayerError as e:
				if attr.__name__ in self.launch_on_no_service:
					self._list[0].launch()
					sleep(0.2)
					self._list[0].get_dbus_interface()
				else:
					print(e)
					raise CommandError()

			try:
				result = attr(*args, **kwargs)
			except PlayerError as e:
				print(e)
				raise CommandError()

			return result

		return wrapped
				




