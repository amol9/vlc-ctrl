import dbus
from dbus import DBusException
from time import sleep
from urlparse import unquote
import random
from os.path import join as joinpath, exists, isdir, isfile
import os
import mimetypes
from subprocess import Popen

from redlib.system import CronDBus, CronDBusError, in_cron, sys_command, DEVNULL
from redlib.misc import Retry


class PlayerError(Exception):
	pass


class Player(object):
	service_name 		= 'org.mpris.MediaPlayer2.vlc'
	object_path 		= '/org/mpris/MediaPlayer2'

	main_interface 		= 'org.mpris.MediaPlayer2'
	player_interface 	= 'org.mpris.MediaPlayer2.Player'
	tracklist_interface 	= 'org.mpris.MediaPlayer2.TrackList'
	prop_interface		= 'org.freedesktop.DBus.Properties'

	obj_no_track		= '/org/mpris/MediaPlayer2/TrackList/NoTrack'

	def __init__(self):
		self._player 	= None
		self._prop 	= None
		self._crondbus 	= None
		self._tracklist = None

		self.setup_crondbus()
		#self.get_dbus_interface()

		self._mime_types = None


	def setup_crondbus(self):
		if in_cron():
			self._crondbus = CronDBus()
			self._crondbus.setup()


	def get_dbus_interface(self):
		try:
			player_obj = dbus.SessionBus().get_object(self.service_name, self.object_path)
		except DBusException as e:
			print(e)
			raise PlayerError('vlc is not running')

		self._player 	= dbus.Interface(player_obj, dbus_interface=self.player_interface)
		self._tracklist = dbus.Interface(player_obj, dbus_interface=self.tracklist_interface)
		self._prop 	= dbus.Interface(player_obj, dbus_interface=self.prop_interface)
		self._main 	= dbus.Interface(player_obj, dbus_interface=self.main_interface)


	def launch(self):
		try:
			r = Popen(['vlc'], stdout=DEVNULL, stderr=DEVNULL)
		except OSError as e:
			print(e)
			raise PlayerError("cannot launch vlc, may be it's not installed")

	
	def play(self, path, filter):
		if path is None:
			self._player.Play()
			return

		self.add(path, filter)

			
	def add(self, path, filter):
		if not exists(path):
			raise PlayerError('no such path: %s'%path)

		if isfile(path):
			if self.mime_type_supported(path):
				self._tracklist.AddTrack('file://' + path, self.obj_no_track, True)
			return

		elif isdir(path):
			if filter.random:
				choices = []
				for root, dirs, files in os.walk(path):
					choices.extend(filter.filter_list(dirs))
					choices.extend(filter.filter_list(files))
					break

				path = joinpath(path, random.choice(choices))
				filter.random = False
				print "random selection: ", path
				self.add(path, filter)
				return

		for root, _, files in os.walk(path):
			for f in files:
				if filter.filter(f):
					self.add(joinpath(root, f), None)


	def mime_type_supported(self, filename):
		if self._mime_types is None:
			self._mime_types = self.get_prop('SupportedMimeTypes', self.main_interface)
	
		if mimetypes.guess_type(filename)[0] in self._mime_types:
			return True
		return False


	def jump(self, pattern):
		pass


	def pause(self):
		self._player.Pause()


	def toggle(self):
		self._player.PlayPause()


	def prev(self):
		self._player.Previous()


	def next(self):
		self._player.Next()


	def get_prop(self, name, iface=None):
		if iface is None:
			iface = self.player_interface

		return self._prop.Get(iface, name)


	def set_prop(self, name, value):
		return self._prop.Set(self.player_interface, name, value)


	def get_volume(self):
		return self.get_prop('Volume')


	def set_volume(self, value):
		self.set_prop('Volume', value)

	
	def fade_volume(self, target, time):
		steps = int(time / 0.1)

		if steps == 0:
			self.set_volume(target)
			return

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
		

	def stop(self):
		self._player.Stop()


	def quit(self, condition, retry, fade):
		if condition is not None:
			r = Retry(retries=retry[0], delay=retry[1], exp_bkf=False)

			while r.left():
				rc, _ = sys_command(condition)
				if rc == 0:
					r.cancel()
				else:
					r.retry()

		if fade > 0:
			saved_volume = self.volume
			self.fade_volume(0, fade)
			self.stop()
			self.volume = saved_volume

		self._main.Quit()		


	def __del__(self):
		if self._crondbus is not None:
			self._crondbus.remove()


	volume=property(get_volume, set_volume)

