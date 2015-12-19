from unittest import TestCase, main as ut_main

from vlc_ctrl.player_list import PlayerList
from vlc_ctrl.filter import Filter


class TestPlayerList(TestCase):

	def test_play(self):
		players = PlayerList()
		players.play('/home/BIG/music/downloads-1/1', Filter())


	def test_pause(self):
		players = PlayerList()
		players.pause()


if __name__ == '__main__':
	ut_main()

