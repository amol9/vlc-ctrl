from unittest import TestCase, main as ut_main


class TestPlayer(TestCase):

	def test_toggle(self):
		player = Player()
		player.toggle()


if __name__ == '__main__':
	ut_main()

