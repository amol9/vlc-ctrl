from unittest import TestCase, main as ut_main
from os.path import join as joinpath

from vlc_ctrl.player import Player
from vlc_ctrl.filter import Filter


class TestPlayer(TestCase):

	def test_toggle(self):
		player = Player()
		player.toggle()


	def test_volume(self):
		player = Player()
		v = player.volume
		print v
		player.volume = (v + 0.01)
		print player.volume

	
	def test_fade_volume(self):
		player = Player()
		player.fade_volume(0.2, 10)


	def test_metadata(self):
		player = Player()
		print player.track_info()


	def test_add(self):
		player = Player()

		path = '/home/BIG/music/trance'
		filter = Filter(exclude_file=joinpath(path, 'exclude'), random=True)

		player.add(path, filter)


	def test_launch(self):
		player = Player()
		player.launch()


	def test_quit(self):
		player = Player()
		player.quit(None, (1, 0), 5)


	def test_quit_condition(self):
		player = Player()
		player.quit("grep test123 a.txt", (10, 10), 5)


if __name__ == '__main__':
	ut_main()

