import ez_setup
ez_setup.use_setuptools()

import platform
import sys
from setuptools import setup, find_packages

from vlc-ctrl.version import __version__


entry_points = {}
entry_points['console_scripts'] = ['wallp=wallp.client.main:main']
if platform.system() == 'Windows':
	entry_points['gui_scripts'] = ['wallps=wallp.client.main:main']


setup(	
	name			= 'vlc-ctrl',
	version			= __version__,
	description		= 'A command line utility to control a running vlc player instance.',
	author			= 'Amol Umrale',
	author_email 		= 'babaiscool@gmail.com',
	url			= 'http://pypi.python.org/pypi/vlc-ctrl/',
	packages		= find_packages(),
	include_package_data	= True,
	scripts			= ['ez_setup.py'],
	entry_points 		= entry_points,
	install_requires	= ['redlib', 'redcmd', 'dbus'],
	classifiers		= [
					'Development Status :: 4 - Beta',
					'Environment :: Console',
					'License :: OSI Approved :: MIT License',
					'Natural Language :: English',
					'Operating System :: POSIX :: Linux',
					'Operating System :: Microsoft :: Windows',
					'Programming Language :: Python :: 2.7',
					'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
					'Topic :: Multimedia :: Graphics'
				]
)

