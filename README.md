# systemd-denotify
GENERAL
-------------------
systemd-denotify is a set of classes that leverage the power of systemd-python library and many other great python bindings(see the Dependencies section).
These classes provide desktop notification upon a user login and when a systemd service fails.
There is also one class that every specified interval (by default 30 minutes) notifies the user for the status of some services.
One can edit the global /etc/systemd-denotify.conf file to alter the notifications this program provides.


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

-------------------------------

NOTE: There is a chance you installed the equivalent python3 packages. See below in the install section what to do.


INSTALL
------------------------
On a terminal:

<pre>git clone https://github.com/gkarakou/systemd-denotify.git

cd systemd-denotify

sudo python2 setup.py

</pre>


NOTE: If you installed the python3 dependencies

<pre>git clone https://github.com/gkarakou/systemd-denotify.git

cd systemd-denotify

sudo python2 setup.py -i v3
</pre>

NOTE for archlinux: if you have trouble installing you might have to pam_permit.so temporarilly in /etc/pam.d/usermod
and after the installation revert your changes back;


UNINSTALL
--------------------------

cd systemd-denotify
sudo python2 setup.py -u


BUILDING FOR DISTRIBUTIONS
----------------------------
There is a pypi ready dedicated branch to build binaries called build. However due to the complexity of downloading and installing all the dependencies through pip the module/app wont be uploaded to pypi.
I was successful in building and installing an rpm for fedora 21.

