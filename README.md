# systemd-notify.py
GENERAL
-------------------
Systemd-notify.py is a set of (python) classes that leverage the power of python-systemd library.
These classes provide desktop notification upon a user login and when a systemd service fails(by constantly reading the systemd journal).
There is also one class that every specified interval (by default 30 minutes) notifies the user for the status of some services.
This  app doesn't want to be intrusive and distractive every while therefore this class is not started. However one if wishes can start it by editing the systemd-notify.py and uncommenting the last two lines. You can also start watching as many services you like by editing by hand the array variable (a list) in the run method of the class DbusNotify. 
If you have already run INSTALL.sh the file is located at /usr/local/bin/systemd-notify.py

NOTE: For the app to work your desktop user must be a member of systemd-journal group. Though INSTALL.sh adds your current X logged in user to the group if you want another user to start X and the app you have to manually add him to the group.


DEPENDENCIES
--------------------

Fedora 21:
python-systemd
python-dbus
python-notify
pygobject2

Arch Linux:
python2
python2-notify
python2-gobject
python2-systemd

NOTE: if you cant find the packages you can always install them from Pypi.

Fedora:
yum install python-pip

Arch:
pacman -S python2-pip



INSTALL
------------------------
git clone https://github.com/gkarakou/systemd-notify.py.git

cd systemd-notify.py

su -

sh INSTALL.sh

exit

or do it with sudo if you believe its safer:

sudo sh INSTALL.sh
