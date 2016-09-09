
from .player import Player, PlayerError
from redcmd.api import CommandError


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


		def player_error_wrapped(method, *args, **kwargs):
			try:
				return method(*args, **kwargs)
			except PlayerError as e:
				raise PlayerListError(e)

		def wrapped(*args, **kwargs):
			try:
				player_error_wrapped(self._list[0].get_dbus_interface)
			except PlayerListError:
				if attr.__name__ in self.launch_on_no_service:
					player_error_wrapped(self._list[0].launch)
					player_error_wrapped(self._list[0].get_dbus_interface, wait=True)

			return player_error_wrapped(attr, *args, **kwargs)

		return wrapped
				




