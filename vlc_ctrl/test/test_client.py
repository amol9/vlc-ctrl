from unittest import TestCase, main as ut_main

from vlc_ctrl.client import ClientSubcommands


class TestClient(TestCase):

	def test_volume(self):
		client = ClientSubcommands()
		client.volume('-10%', '10')
		#client.volume('+20%', '0')


	def test_quit(self):
		client = ClientSubcommands()
		client.quit('ls', '2,10', '10')


	def test_play(self):
		client = ClientSubcommands()
		path = '/home/BIG/music/trance'
		client.play(path, random=True, exclude_file=path+'/exclude')


	def test_info(self):
		client = ClientSubcommands()
		client.info()


if __name__ == '__main__':
	ut_main()

