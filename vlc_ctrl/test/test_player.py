from unittest import TestCase, main as ut_main

from vlc_ctrl.player import Player


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


if __name__ == '__main__':
	ut_main()

