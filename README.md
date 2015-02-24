# systemd-notify.py
GENERAL
-------------------
Systemd-notify.py is a set of (python) classes that leverage the power of systemd-python library and many other great python bindings(see Dependencies section).
These classes provide desktop notification upon a user login and when a systemd service fails(by constantly reading the systemd journal).
There is also one class that every specified interval (by default 30 minutes) notifies the user for the status of some services.
This  app doesn't want to be intrusive and distractive every while therefore this class is not started. However one if wishes can start it by editing the systemd-notify.py and uncommenting the last two lines. You can also start watching as many services you like by editing by hand the array variable (a list) in the run method of the class DbusNotify. 
If you have already run INSTALL.sh the file is located at /usr/local/bin/systemd-notify.py

NOTE: For the app to work your desktop user must be a member of systemd-journal group. Though INSTALL.sh adds your current X logged in user to the group if you want another user to start X and the app you have to manually add him to the group.


REQUIREMENTS
-------------------

As the name implies you need to be running a modern linux distribution with systemd.

 You also need a running Xorg, this script(though i like to call it a classy python app) wont work without a desktop session.



DEPENDENCIES
--------------------

Fedora 21:

<pre>
systemd-python
notify-python
pygobject2
python-slip-dbus

</pre>
Arch Linux:

<pre>
python2
python2-notify
python2-gobject
python2-systemd

</pre>
NOTE: if you cant find the packages you can always search them through Pypi.

Fedora:
<pre>
yum install python-pip
</pre>
Arch:
<pre>
pacman -S python2-pip
</pre>

Search a package:

<pre>
pip search dbus
</pre>


INSTALL
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
