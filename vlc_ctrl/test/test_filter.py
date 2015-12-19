from unittest import TestCase, main as ut_main
from os.path import dirname, abspath, join as joinpath

from vlc_ctrl.filter import Filter, FilterError


class TestFilter(TestCase):
	data_dir = dirname(abspath(__file__))

	def test_include(self):
		f = Filter(include='*.mp3,*.mp4,*.wav')

		self.assertTrue(f.filter('1.mp3'))
		self.assertTrue(f.filter('song.mp3'))
		self.assertTrue(f.filter('nice song.mp3'))
		self.assertTrue(f.filter('1.mp4'))
		self.assertTrue(f.filter('old.wav'))

		self.assertFalse(f.filter('1.mpeg'))
		self.assertFalse(f.filter('list.txt'))
		self.assertFalse(f.filter('old'))


	def test_exclude(self):
		f = Filter(exclude='*.part,*bieber*.*,not_music*')

		self.assertTrue(f.filter('armin.mp3'))
		self.assertTrue(f.filter('two and a half men.mp4'))
		self.assertTrue(f.filter('bryan adams.wav'))

		self.assertFalse(f.filter('big.mp3.part'))
		self.assertFalse(f.filter('justin_bieber_new.mp3'))
		self.assertFalse(f.filter('video_bieber.mp4'))
		self.assertFalse(f.filter('not_music/data.txt'))
		self.assertFalse(f.filter('not_music'))


	def test_include_exclude(self):
		f = Filter(include='*.mp3', exclude='*.part,*bieber*.*,not_music/*')

		self.assertTrue(f.filter('armin.mp3'))
		self.assertTrue(f.filter('more/hardwell.mp3'))

		self.assertFalse(f.filter('two and a half men.mp4'))
		self.assertFalse(f.filter('bryan adams.wav'))
		self.assertFalse(f.filter('big.mp3.part'))
		self.assertFalse(f.filter('justin_bieber_new.mp3'))
		self.assertFalse(f.filter('video_bieber.mp4'))
		self.assertFalse(f.filter('not_music/data.txt'))
		self.assertFalse(f.filter('not_music'))


	def test_exclude_file(self):
		with self.assertRaises(FilterError):
			Filter(exclude_file='none.txt')

		f = Filter(exclude_file=joinpath(self.data_dir, 'exclusion_list.txt'))

		self.assertTrue(f.filter('song.mp3'))
		self.assertTrue(f.filter('/a/b/song.mp3'))

		self.assertFalse(f.filter('data'))
		self.assertFalse(f.filter('data/1.mp3'))
		self.assertFalse(f.filter('data/more/new.mp3'))
		self.assertFalse(f.filter('data/more/1.swp'))
		self.assertFalse(f.filter('doc.swp'))


	def test_filter_list(self):
		f = Filter(include='*.mp3,*.mp4,*.wav')

		self.assertEquals(f.filter_list(['1.mp3', '1.mp4', '2.mp3', '1.txt', '1.wav', '2.txt']), ['1.mp3', '1.mp4', '2.mp3', '1.wav'])


if __name__ == '__main__':
	ut_main()

