# systemd-denotify
GENERAL
-------------------
systemd-denotify build repo
Differences from master + experimental:


2. the installer doesn't add the x logged in user to group because of permission errors(tried with sudo and pkexec)

3. Therefore the .conf file adds comments to manually start the class/service and defaults now to False(dont start)

4. Stripped the espeak calls and the deps off.

5. What is not been implemented: If one goes yum remove systemd-denotify the module installed will be deleted but not the files that the install_script.py had chmoded and cp'ed to the system dirs(/etc/,/etc/xdg/autostart/,/usr/local/bin). The .spec file is unaware of what the external installer did!




1. the installer doesn't add the x logged in user to group because of permission errors(tried with sudo and pkexec)
 Therefore the .conf file adds comments to manually start the class/service and defaults now to False(dont start)

2. Stripped the espeak calls and the deps off.



Though this module is pypi ready i found it really tedious to install all the dependencies from pip.
Unfortunately this module/app wont be uploaded to pypi. However all the dependencies should be found from the distros repos and if not all many of them should have been allready installed. At a least on a fedora 21 i had to install only python-inotify and notify-python.
Below are some guidelines to generate packages for debian,ubuntu,fedora. Arch should not be difficult either- only
a proper PKGBUILD would be needed.

DEPENDENCIES
-------------------

Fedora 21:

<pre>
systemd-python notify-python pygobject2 python-slip-dbus python-inotify

</pre>
Arch Linux:

<pre>
python2 python2-setuptools python2-notify python2-gobject python2-systemd python2-dbus python-pyinotify

</pre>

Debian:

<pre>
python-systemd python-dbus python-notify python-gobject python-gi python-inotify
</pre>



SOURCE DISTRIBUTION
---------------------

<pre>
git clone https://github.com/gkarakou/systemd-denotify.git

cd systemd-denotify

git checkout build
<<<<<<< HEAD

python2 setup.py sdist


</pre>
=======

python2 setup.py sdist


</pre>


DEBIAN/UBUNTU
----------------
It seems that if you install  stdeb and have a source distribution as generated above creating a .deb to be installed with dpkg is really easy.
If you find any troubles you can follow this guide:
http://shallowsky.com/blog/programming/python-debian-packages-w-stdeb.html

>>>>>>> build-merge

BUILD FOR FEDORA
------------------
<pre>
git clone https://github.com/gkarakou/systemd-denotify.git

<<<<<<< HEAD
DEBIAN/UBUNTU
----------------
It seems that if you install  stdeb and have a source distribution as generated above creating a .deb to be installed with dpkg is really easy.
If you find any troubles you can follow this guide:
http://shallowsky.com/blog/programming/python-debian-packages-w-stdeb.html
=======
cd systemd-denotify
>>>>>>> build-merge

git checkout build

<<<<<<< HEAD
BUILD FOR FEDORA
------------------
<pre>
git clone https://github.com/gkarakou/systemd-denotify.git

cd systemd-denotify

git checkout build

sudo python setup.py bdist_rpm --requires "python python-setuptools systemd-python notify-python pygobject2 python-slip-dbus python-inotify"

sudo rpm -i dist/systemd-denotify-1.0-1.noarch.rpm
=======
sudo python setup.py bdist_rpm --requires "python python-setuptools systemd-python notify-python pygobject2 python-slip-dbus python-inotify" --post-uninstall=postuinstall.sh

sudo rpm -i dist/systemd-denotify-1.0-1.noarch.rpm

or

sudo yum install
>>>>>>> build-merge
</pre>
