# systemd-notify.py
GENERAL
-------------------
Systemd-notify.py is a set of classes that leverage the power of systemd-python library and many other great python bindings(see the Dependencies section).
These classes provide desktop notification upon a user login and when a systemd service fails.
There is also one class that every specified interval (by default 30 minutes) notifies the user for the status of some services.
One can start it on demand by answering the questions when installing.


REQUIREMENTS
-------------------

As the name implies you need to be running a modern linux distribution with systemd.

You also need a running Xorg, this script(though i like to call it a classy python app) wont work without a desktop session.

As a linux user you have to be comfortable with the terminal.

DEPENDENCIES
-------------------


Fedora 21:

<pre>
systemd-python notify-python pygobject2 python-slip-dbus

</pre>
Arch Linux:

<pre>
python2 python2-notify python2-gobject python2-systemd python2-dbus

</pre>

Debian:

<pre>
python-systemd python-dbus python-notify python-gobject python-gi

</pre>



NOTE: if you cant find the packages in your distro's package manager you can always search them through Pypi and install them afterwards.

Fedora:
<pre>
yum install python-pip
</pre>
Arch:
<pre>
pacman -S python2-pip
</pre>
Debian:
<pre>
apt-get install python-pip
</pre>

Search a package:

<pre>
pip search dbus
</pre>

-------------------------------

NOTE: There is a chance you installed the equivalent python3 packages. See below in the install section what to do.


INSTALL
------------------------
On a terminal:

<pre>git clone https://github.com/gkarakou/systemd-notify.py.git

cd systemd-notify.py

sudo python3 setup.py

</pre>


NOTE: If you installed the python3 dependencies

<pre>
sudo python3 setup.py -i v3
</pre>

