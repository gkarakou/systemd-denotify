# systemd-notify.py
GENERAL
-------------------
<<<<<<< HEAD
Systemd-notify is a set of classes that leverage the power of python-systemd library.
=======
Systemd-notify.py is a set of classes that leverage the power of systemd-python library and many other great python bindings(see Dependencies section).
>>>>>>> d8afeee1f46e6eb0f32d311b78752c443a565303
These classes provide desktop notification upon a user login and when a systemd service fails(by constantly reading the systemd journal).
There is also one class that every specified interval (by default 30 minutes) notifies the user for the status of some services.
By default this class is not started. However one can start it by editing the systemd-notify.py and uncommenting the last two lines.
If you have already run INSTALL.sh the file is located at /usr/local/bin/systemd-notify.py


REQUIREMENTS
-------------------

As the name implies you need to be running a modern linux distribution with systemd.

 You also need a running Xorg, this script(though i like to call it a classy python app) wont work without a desktop session.



DEPENDENCIES
<<<<<<< HEAD

On a fedora 21 installation it depends on these libraries(On other linux distributions these names could be different):

--------------------
python-systemd
python-dbus
python-notify
pygobject2
=======
--------------------

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


NOTE: if you only find python3 libs in your distro's repos there is a python3 library named systemd-notify3.py, but it has not been thoroughly tested and is not guaranteed to work.

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
>>>>>>> d8afeee1f46e6eb0f32d311b78752c443a565303

-------------------------------

INSTALL
<<<<<<< HEAD

Just run as root INSTALL.sh after installing the dependencies.
=======
------------------------
<pre>git clone https://github.com/gkarakou/systemd-notify.py.git

cd systemd-notify.py

su -

sh INSTALL.sh

exit
</pre>
or do it with sudo if you believe its safer:
<pre>

sudo sh INSTALL.sh

</pre>
>>>>>>> d8afeee1f46e6eb0f32d311b78752c443a565303
