# systemd-denotify
GENERAL
-------------------
systemd-denotify build repo

distutils made setup.py


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


BUILD FOR FEDORA
------------------
<pre>
git clone https://github.com/gkarakou/systemd-denotify.git

cd systemd-denotify

git checkout build

sudo python setup.py bdist_rpm --requires "python python-setuptools systemd-python notify-python pygobject2 python-slip-dbus python-inotify"

sudo rpm -i dist/systemd-denotify-1.0-1.noarch.rpm
</pre>
