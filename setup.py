#!/usr/bin/python2

# Copyright (C) 2015 George Karakou (gkarakou)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You can get a copy of the GNU General Public License at
# <http://www.gnu.org/licenses/>.

#http://stackoverflow.com/questions/11536764/attempted-relative-import-in-non-package-even-with-init-py
if __package__ is None:
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from install_script import Installer
else:
    from .install_script import Installer
from distutils.core import setup
import os
from setuptools.command.install import install

class MyInstall(install):
#custom class derived from a stackoverflow answer
    def run(self):
        install.run(self)
        installer = Installer()
        installer.remove_old_version()
        installer.reset_desktop_file()
        #installer.addXuser_to_group()
        installer.install_v2()

setup(
name = 'systemd-denotify',
version = '1.0',
description = 'linux systemd related desktop notifications',
long_description = 'A linux desktop app that notifies for user logins, failed systemd services, monitored files and the status of selected services',
author = 'George Karakougioumtzis <gkarakou>',
author_email = 'gkarakou@gmail.com',
url = 'https://github.com/gkarakou/systemd-denotify',
platforms = 'linux',
license = 'GPL-3.0',
#py_modules=['systemd-denotify', 'install_script'],
packages = ['systemd-denotify'],
package_data = {'systemd-denotify': ['conf/*']},
install_requires= ['dbus-python', 'pygobject', 'python-systemd', 'pyinotify'],
#dependency_links = ["https://pypi.python.org/packages/source/p/python-systemd/python-systemd-0.0.9.tar.gz", "https://pypi.python.org/packages/source/n/notify2/notify2-0.3.tar.gz", "https://pypi.python.org/packages/source/P/PyGObject/pygobject-2.28.3.tar.bz2#md5=aa64900b274c4661a5c32e52922977f9", "https://pypi.python.org/packages/source/d/dbus-python/dbus-python-0.84.0.tar.gz", "https://pypi.python.org/packages/source/p/pyinotify/pyinotify-0.9.5.tar.gz"],
cmdclass = {'install': MyInstall},
classifiers = ['Development Status :: 1.0 - Stable',
'Environment :: Desktop',
'Intended Audience :: End Users/Desktop',
'Intended Audience :: System Administrators',
'License :: GPL-3.0 ',
'Operating System :: Linux',
'Programming Language :: Python2.7'],
)
