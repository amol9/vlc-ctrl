import dbus
from dbus import DBusException
from time import sleep
from six.moves.urllib.parse import unquote
import random
from os.path import join as joinpath, exists, isdir, isfile
import os
import mimetypes
from subprocess import Popen
import shlex

from redlib.api.system import CronDBus, CronDBusError, in_cron, sys_command, DEVNULL
from redlib.api.misc import Retry, log


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

	launch_wait		= 10

	def __init__(self):
		self._player 	= None
		self._prop 	= None
		self._crondbus 	= None
		self._tracklist = None

		self.setup_crondbus()

		self._mime_types = None


	def setup_crondbus(self):
		if in_cron():
			self._crondbus = CronDBus()
			self._crondbus.setup()


	def get_dbus_interface(self, wait=False):
		retry_count = self.launch_wait if wait else 1
		retry = Retry(retries=retry_count, delay=1, exp_bkf=False, final_exc=PlayerError('vlc is not running'))

		while retry.left():
			try:
				player_obj = dbus.SessionBus().get_object(self.service_name, self.object_path)
				retry.cancel()
			except DBusException as e:
				retry.retry()

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
		uqpath = shlex.split(path)[0]

		if not exists(uqpath):
			raise PlayerError('no such path: %s'%uqpath)

		if isfile(uqpath):
			if self.mime_type_supported(uqpath):
				self._tracklist.AddTrack('file://' + uqpath, self.obj_no_track, True)
			return

		elif isdir(uqpath):
			if filter.random:
				choices = []
				for root, dirs, files in os.walk(uqpath):
					choices.extend(filter.filter_list(dirs))
					choices.extend(filter.filter_list(files))
					break

				uqpath = joinpath(uqpath, random.choice(choices))
				filter.random = False
				self.add(uqpath, filter)
				return

		for root, _, files in os.walk(uqpath):
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


	def set_prop(self, name, value, iface=None):
		if iface is None:
			iface = self.player_interface

		return self._prop.Set(iface, name, value)


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
		for _ in range(0, steps):
			self.volume -= delta
			sleep(0.1)


	def track_info(self):
		metadata = self.get_prop('Metadata')
		info = {}

		def unc(input):
			if input is None:
				return None
			return input.encode('utf-8')

		mget = lambda k : metadata.get(k, None)

		info['album'] 	= unc(mget('xesam:album'))
		info['title'] 	= unc(mget('xesam:title'))
		info['artist'] 	= unc(mget('xesam:artist')[0]) if mget('xesam:artist') is not None and len(mget('xesam:artist')) > 0 else None
		info['length'] 	= unc(str(int(mget('vlc:length') / 1000))) if mget('vlc:length') is not None else None
		info['path']	= unc(unquote(mget('xesam:url')))
		info['genre'] 	= unc(mget('xesam:genre')[0]) if mget('xesam:genre') is not None and len(mget('xesam:genre')) > 0 else None

		return info
		

	def stop(self):
		self._player.Stop()


	def shuffle(self):
		self.set_prop('Shuffle', True)


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

