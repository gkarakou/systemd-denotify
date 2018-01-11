# systemd-denotify

Updated to v1.2

GENERAL
-------------------
systemd-denotify is a set of classes that leverage the power of systemd-python library and many other great python bindings.
These classes provide desktop and email notifications upon a user login, when systemd files are modified and when services fail.
There is also another class that at a specified interval (by default 30 minutes) notifies the user for the status of some services.
Added support for journal pattern matching in version 1.2.
One can override the notifications he/she gets by editing the file /etc/systemd-denotify.conf.


CAUTION:

if you use vim to edit files that are being monitored by systemd-denotify.py  you will be notified when the backup files that vim writes before saving a file that is modified are written too(also known as swap files =.swp).
To overcome this annoyance you can edit /root/.vimrc and add these lines:
<pre>
set nobackup

set nowritebackup

set noswapfile
</pre>
You can expect data corruption if you dont have a ups installed, you have been warned.

INSTALLATION
------------------------------------


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

BUILD FOR FEDORA 22 AND UPWARDS
------------------
<pre>
git clone https://github.com/gkarakou/systemd-denotify.git

cd systemd-denotify

sudo python setup.py bdist_rpm --requires "python2, systemd-python, notify-python, pygobject2, python-slip-dbus, python-inotify, systemd, systemd-libs, libnotify, dbus, dbus-python" --build-requires="python-setuptools" --vendor="gkarakou@gmail.com" --post-install=postinstall.sh --no-autoreg

sudo dnf --nogpgcheck install dist/systemd-denotify-1.2-1.noarch.rpm

</pre>

Trouble installing?

Verify that you have all the build tools installed (rpm-build-libs, auto-buildrequires, python2-devel) and update the system.
If you still have problems add the command line parameter
<pre>
--no-autoreq
</pre>
in the python setup.py command above.

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

Simply read and edit the /etc/systemd-denotify.conf file.
