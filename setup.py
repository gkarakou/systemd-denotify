#!/usr/bin/python

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

from distutils.core import setup
from fnmatch        import fnmatch
import os
from setuptools.command.install import install
import subprocess
from install_script import Installer

class MyInstall(install):
#custom class derived from a stackoverflow answer
    def run(self):
        install.run(self)
        installer = Installer()
        installer.remove_old_version()
        installer.reset_desktop_file()
        installer.is_archlinux()
        installer.addXuser_to_group()
        installer.install_v2()

def listfiles(*dirs):
        dir, pattern = os.path.split(os.path.join(*dirs))
        return [os.path.join(dir, filename)
        for filename in os.listdir(os.path.abspath(dir))
           if filename[0] != '.' and fnmatch(filename, pattern)]

setup(
        name             = 'systemd-denotify',
        version          = '1.0',
        description      = 'linux systemd desktop notifications',
        long_description = " A linux desktop app that notifies for user logins, failed systemd services,monitored files and the status of selected services",
        author           = 'George Karakougioumtzis <gkarakou>',
        author_email     = 'gkarakou@gmail.com',
        url              = 'https://github.com/gkarakou/systemd-denotify',
        platforms        = 'linux',
        license          = 'GPL-3.0',
        dependency_links  = ["https://pypi.python.org/packages/source/p/python-systemd/python-systemd-0.0.9.tar.gz",],
        cmdclass	 = {'install': MyInstall}
        )
