# systemd-notify.py
GENERAL
-------------------
Systemd-notify.py is a set of classes that leverage the power of systemd-python library and many other great python bindings(see the Dependencies section).
These classes provide desktop notification upon a user login and when a systemd service fails (by constantly reading the systemd journal).
There is also one class that every specified interval (by default 30 minutes) notifies the user for the status of some services.
One can start it on demand by answering the questions when installing. See the INSTALL section 


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
<pre>git clone https://github.com/gkarakou/systemd-notify.py.git

cd systemd-notify.py

su -

python3 install.py -v2

exit
</pre>
or do it with sudo if you believe its safer:
<pre>

sudo python3 install.pt -v2

</pre>


NOTE: if you only found the python3 libs in your distro's repos there is a python3 library named systemd-notify3.py. To install it:

<pre>
sudo python3 install.py -v3
</pre>

