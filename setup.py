import ez_setup
ez_setup.use_setuptools()

import platform
import sys
from setuptools import setup, find_packages

from rc_setup import setup_autocomp

from vlc_ctrl.version import __version__


entry_points = {}
entry_points['console_scripts'] = ['vlc-ctrl=vlc_ctrl.main:main']

setup(	
	name			= 'vlc-ctrl',
	version			= __version__,
	description		= 'A command line utility to control a running vlc player instance.',
	author			= 'Amol Umrale',
	author_email 		= 'babaiscool@gmail.com',
	url			= 'http://pypi.python.org/pypi/vlc-ctrl/',
	packages		= ['vlc_ctrl'], 
	include_package_data	= True,
	scripts			= ['ez_setup.py', 'rc_setup.py'],
	entry_points 		= entry_points,
	install_requires	= ['redlib>=1.1.0', 'redcmd>=1.1.3', 'six'],
	classifiers		= [
					'Development Status :: 4 - Beta',
					'Environment :: Console',
					'License :: OSI Approved :: MIT License',
					'Natural Language :: English',
					'Operating System :: POSIX :: Linux',
					'Programming Language :: Python :: 2.7',
					'Programming Language :: Python :: 3.4',
					'Topic :: Multimedia :: Sound/Audio',
					'Topic :: Multimedia :: Sound/Audio :: Players',
					'Topic :: Multimedia :: Sound/Audio :: Players :: MP3',
					'Topic :: Multimedia :: Video'
				]
)


setup_autocomp('vlc_ctrl.client', 'vlc-ctrl', _to_hyphen=True)

