# systemd-notify.py
GENERAL
-------------------
Systemd-notify.py is a set of classes that leverage the power of systemd-python library and many other great python bindings(see Dependencies section).
These classes provide desktop notification upon a user login and when a systemd service fails(by constantly reading the systemd journal).
There is also one class that every specified interval (by default 30 minutes) notifies the user for the status of some services.
By default this class is not started. However one can start it by editing the systemd-notify(3).py and uncommenting the last two lines.
If you have already run INSTALL.sh the file is located at /usr/local/bin/systemd-notify(3).py


REQUIREMENTS
-------------------

As the name implies you need to be running a modern linux distribution with systemd.

 You also need a running Xorg, this script(though i like to call it a classy python app) wont work without a desktop session.



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
python-systemd python-dbus python-notify

</pre>



NOTE: if you cant find the packages in your distro's package manager you can always search them through Pypi.

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

NOTE: There is a chance you installed the equivalent python3 packages. See below in the install section how to


INSTALL
------------------------
<pre>git clone https://github.com/gkarakou/systemd-notify.py.git

cd systemd-notify.py

su -

sh INSTALL.sh -python2

exit
</pre>
or do it with sudo if you believe its safer:
<pre>

sudo sh INSTALL.sh -python2

</pre>


NOTE: if you only find python3 libs in your distro's repos there is a python3 library named systemd-notify3.py, but it has not been thoroughly tested and is not guaranteed to work. To install it:

<pre>
sudo sh INSTALL.sh -python3
</pre>

