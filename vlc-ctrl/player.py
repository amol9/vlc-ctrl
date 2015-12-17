import dbus

class Player:
	service_name 	= 'org.mpris.MediaPlayer2.vlc'
	object_path 	= '/org/mpris/MediaPlayer2'
	dbus_interface 	= 'org.mpris.MediaPlayer2.Player'

	def __init__(self):
		self._player = None
		self.get_dbus_interface()


	def get_dbus_interface(self):
		player_obj = dbus.SessionBus().get_object(service_name, object_path)
		self._player = dbus.Interface(player_obj, dbus_interface=self.dbus_interface)

	
	def play(self):
		pass


	def pause(self):
		self._player.Pause()


	def toggle(self):
		self._player.PlayPause()

