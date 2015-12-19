import fnmatch
from os.path import exists


class FilterError(Exception):
	pass


class Filter(object):

	def __init__(self, include=None, exclude=None, include_file=None, exclude_file=None, random=False, playtime=None):
		self._include_list 	= self.load(include, include_file)
		self._exclude_list 	= self.load(exclude, exclude_file)
		self._random		= random

	
	def load(self, patterns, pattern_file):
		pattern_list = []

		if patterns is not None:
			pattern_list.extend([p for p in patterns.split(',') if p.strip() != ''])

		if pattern_file is not None:
			if not exists(pattern_file):
				raise FilterError('no such file: %s'%pattern_file)

			with open(pattern_file, 'r') as f:
				pattern_list.extend([p for p in f.read().splitlines() if p.strip() != ''])

		return pattern_list


	def filter(self, name):
		result = None
		if len(self._include_list) > 0 and not any([fnmatch.fnmatch(name, p) for p in self._include_list]):
			return False

		if any([fnmatch.fnmatch(name, p) for p in self._exclude_list]):
			return False

		return True


	def filter_list(self, names):
		return [n for n in names if self.filter(n)]


	def get_random(self):
		return self._random


	def set_random(self, value):
		self._random = value


	random=property(get_random, set_random)

