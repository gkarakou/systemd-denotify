# systemd-notify.py
GENERAL
-------------------
Systemd-notify is a set of classes that leverage the power of python-systemd library.
These classes provide desktop notification upon a user login and when a systemd service fails(by constantly reading the systemd journal).
There is also one class that every specified interval (by default 30 minutes) notifies the user for the status of some services.
By default this class is not started. However one can start it by editing the systemd-notify.py and uncommenting the last two lines.
If you have already run INSTALL.sh the file is located at /usr/local/bin/systemd-notify.py


DEPENDENCIES

On a fedora 21 installation it depends on these libraries(On other linux distributions these names could be different):

--------------------
python-systemd
python-dbus
python-notify
pygobject2

-------------------------------

INSTALL

Just run as root INSTALL.sh after installing the dependencies.
