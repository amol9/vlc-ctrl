========
vlc-ctrl
========


Lets you control a running instance of vlc player, start a new instance, get track information, etc.


Supported platforms
===================

* python 2.7 / 3.4
* Linux


Features
========

* Controls vlc player over dbus.
* Play, pause, shuffle, toggle, prev, next, stop commands.
* Play all files in a directory (recursively added).
* Add files / directories based on inclusion and exclusion patterns.
* Change volume / fade volume.
* Print current track info.
* Quit vlc.
* Quit based on return code of another command.
* Can be used as a cron job.


Dependencies
============

* vlc player, of course.

* python-dbus or python3-dbus

  On Ubuntu: `>apt-get install python-dbus` or `apt-get install python3-dbus`


Usage
=====

See: `vlc-ctrl -h`


Download
========
* PyPI: http://pypi.python.org/pypi/vlc-ctrl
* Source: https://github.com/amol9/vlc-ctrl

