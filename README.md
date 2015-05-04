# systemd-denotify
GENERAL
-------------------
systemd-denotify build repo
Differences from master + experimental:


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

python2 setup.py sdist


</pre>


DEBIAN/UBUNTU
----------------

<pre>
sudo apt-get install python-stdeb fakeroot python-all

git clone https://github.com/gkarakou/systemd-denotify.git

cd systemd-denotify

git checkout build

sudo python setup.py sdist_dsc --depends "systemd systemd-libs dbus libnotify python-systemd python-dbus python-notify python-gobject python-gi python-inotify xorg notification-daemon" --build-depends "python-setuptools" bdist_deb

#it should produce a .deb package ready to be installed in deb_dist directory (hint:ls -al deb_dist|grep deb):

sudo dpkg -i deb_dist/systemd-denotify-$VERSION.deb

sudo apt-get -f install
</pre>

If you find any troubles you can follow this guide:
http://shallowsky.com/blog/programming/python-debian-packages-w-stdeb.html


BUILD FOR FEDORA
------------------
<pre>
git clone https://github.com/gkarakou/systemd-denotify.git

cd systemd-denotify

git checkout build

sudo python setup.py bdist_rpm --requires "python,  systemd-python, notify-python, pygobject2, python-slip-dbus, python-inotify, systemd, systemd-libs, libnotify, notification-daemon, dbus, dbus-python, xorg-x11-server-Xorg" --build-requires="python-setuptools" --vendor="gkarakou@gmail.com" --post-install=postinstall.sh

sudo yum --nogpgcheck localinstall dist/systemd-denotify-1.0-1.noarch.rpm

</pre>


ARCHLINUX
-----------------

PKGBUILD

<pre>
pkgname=systemd-denotify
pkgver=r254.de1d483
pkgrel=1
pkgdesc='A set of python classes that provide desktop notification upon a user login and when a systemd service fails.'
arch=(any)
url='https://github.com/gkarakou/systemd-denotify'
license=('GPL')
depends=('python2' 'python2-setuptools' 'libnotify' 'notification-daemon' 'python2-dbus' 'python2-gobject' 'python2-notify' 'python2-systemd' 'python2-pyinotify' 'systemd' 'systemd-libs' 'dbus' 'xorg-server')
source=("${pkgname}::git+https://github.com/gkarakou/systemd-denotify")
md5sums=('SKIP')

pkgver() {
  cd "$pkgname"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package() {
  cd "$pkgname"
  git checkout build
  python2 setup.py install --root="${pkgdir}/"
}

</pre>
