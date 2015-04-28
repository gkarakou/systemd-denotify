# systemd-notify.py
GENERAL
-------------------
Systemd-notify.py should not be confused with systemd-notify binary which is part of the systemd core library. Only the names match(that is my mistake since i forgot the c library that is located at /usr/bin), the functionality differs.
Systemd-notify.py is a set of classes that leverage the power of systemd-python library and many other great python bindings(see the Dependencies section).
These classes provide desktop notification upon a user login, when systemd files are modified and when services fail(you will also be notified orally when systemd services fail).
There is also one class that at a specified interval (by default 30 minutes) notifies the user for the status of some services.
One can start it on demand by answering the questions when installing.
I wrote these classes to enhance systemd's role on my desktop, but you can modify it to suit your custom needs if you are familiar with python.

NOTE: if you use vim to edit files that are being monitored by systemd-notify.py in the /etc/systemd/ and /usr/lib/systemd/ directories you will be notified when the backup files that vim writes before saving a file that is modified are written too.
To overcome this annoyance if and only if you have a ups installed (in the case of a power failure you will lose data if you dont own a ups) you can edit /root/.vimrc and add these lines:\n
set nobackup \n
set nowritebackup\n
set noswapfile

Do this only if you own a ups, you have been warned.

REQUIREMENTS
-------------------

As the name implies you need to be running a modern linux distribution with systemd.
You also need a running Xorg, this script(though i like to call it a classy python app) wont work without a desktop session.
As a linux user you have to be comfortable with the terminal.

DEPENDENCIES
-------------------

Fedora 21:

<pre>
systemd-python notify-python pygobject2 python-slip-dbus espeak python-espeak python-inotify

</pre>
Arch Linux:

<pre>
python2 python2-notify python2-gobject python2-systemd python2-dbus espeak python-espeak python-inotify

</pre>

Debian:

<pre>
python-systemd python-dbus python-notify python-gobject python-gi espeak espeak-data python-espeak python-inotify

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

