# systemd-denotify

GENERAL
-------------------
systemd-denotify is a set of classes that leverage the power of systemd-python library and many other great python bindings.
These classes provide desktop and email notification upon a user login, when systemd files are modified and when services fail.
There is also another class that at a specified interval (by default 30 minutes) notifies the user for the status of some services.
One can override the notifications he/she gets by editing the file /etc/systemd-denotify.conf.

NOTE: if you use vim to edit files that are being monitored by systemd-denotify.py in the /etc/systemd/ and /usr/lib/systemd/ directories you will be notified when the backup files that vim writes before saving a file that is modified are written too.
To overcome this annoyance if and only if you have a ups installed (in the case of a power failure you will lose data if you dont own a ups) you can edit /root/.vimrc and add these lines:
<pre>
set nobackup

set nowritebackup

set noswapfile
</pre>
Do this only if you own a ups, you have been warned.


Though this module is pypi ready i found it really tedious to install all the dependencies from pip.
Unfortunately this module/app wont be uploaded to pypi. Hopefully this package gets its way into the repos.
Below are some guidelines to generate packages for debian,ubuntu,fedora. Arch should not be difficult either- only
a proper PKGBUILD would be needed.

SOURCE DISTRIBUTION
---------------------

<pre>
git clone https://github.com/gkarakou/systemd-denotify.git

cd systemd-denotify

python2 setup.py sdist


</pre>

BUILD FOR FEDORA
------------------
<pre>
git clone https://github.com/gkarakou/systemd-denotify.git

cd systemd-denotify

sudo python setup.py bdist_rpm --requires "python,  systemd-python, notify-python, pygobject2, python-slip-dbus, python-inotify, systemd, systemd-libs, libnotify, dbus, dbus-python, xorg-x11-server-Xorg" --build-requires="python-setuptools" --vendor="gkarakou@gmail.com" --post-install=postinstall.sh

sudo yum --nogpgcheck localinstall dist/systemd-denotify-1.0-1.noarch.rpm

</pre>

-------------------------------

DEBIAN/UBUNTU
----------------

<pre>
sudo apt-get install python-stdeb fakeroot python-all

git clone https://github.com/gkarakou/systemd-denotify.git

cd systemd-denotify

sudo python setup.py sdist_dsc --depends "systemd systemd-libs dbus libnotify python-systemd python-dbus python-notify python-gobject python-gi python-inotify xorg notification-daemon" --build-depends "python-setuptools" bdist_deb

#it should produce a .deb package ready to be installed in deb_dist directory (hint:ls -al deb_dist|grep deb):

sudo dpkg -i deb_dist/systemd-denotify-$VERSION.deb

sudo apt-get -f install
</pre>

If you find any troubles you can follow this guide:
http://shallowsky.com/blog/programming/python-debian-packages-w-stdeb.html


ARCHLINUX
-----------------

systemd-denotify is already in AUR:
https://aur.archlinux.org/packages/systemd-denotify/

USAGE
------------------

Simply read and edit accordingly /etc/systemd-denotify.conf
