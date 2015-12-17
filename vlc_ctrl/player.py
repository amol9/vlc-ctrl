import dbus
from time import sleep
from urlparse import unquote


class Player(object):
	service_name 	= 'org.mpris.MediaPlayer2.vlc'
	object_path 	= '/org/mpris/MediaPlayer2'
	dbus_interface 	= 'org.mpris.MediaPlayer2.Player'
	prop_interface	= 'org.freedesktop.DBus.Properties'

	def __init__(self):
		self._player = None
		self._prop = None
		self.get_dbus_interface()


	def get_dbus_interface(self):
		player_obj = dbus.SessionBus().get_object(self.service_name, self.object_path)
		self._player = dbus.Interface(player_obj, dbus_interface=self.dbus_interface)
		self._prop = dbus.Interface(player_obj, dbus_interface=self.prop_interface)

	
	def play(self):
		pass


	def pause(self):
		self._player.Pause()


	def toggle(self):
		self._player.PlayPause()


	def get_prop(self, name):
		return self._prop.Get(self.dbus_interface, name)


	def set_prop(self, name, value):
		return self._prop.Set(self.dbus_interface, name, value)


	def get_volume(self):
		return self.get_prop('Volume')


	def set_volume(self, value):
		self.set_prop('Volume', value)

	
	def fade_volume(self, target, time):
		steps = int(time / 0.1)
		delta = (self.volume - target) / steps
		print steps, delta
		for _ in range(0, steps):
			self.volume -= delta
			sleep(0.1)


	def track_info(self):
		metadata = self.get_prop('Metadata')
		info = {}

		info['album'] 	= str(metadata['xesam:album'])
		info['title'] 	= str(metadata['xesam:title'])
		info['artist'] 	= str(metadata['xesam:artist'][0]) if len(metadata['xesam:artist']) > 0 else None
		info['length'] 	= int(int(metadata['vlc:length']) / 1000)
		info['path']	= unquote(str(metadata['xesam:url']))
		info['genre'] 	= str(metadata['xesam:genre'][0]) if len(metadata['xesam:genre']) > 0 else None

		return info
		



	volume=property(get_volume, set_volume)

