#!/bin/bash
if [ -f /etc/pacman.conf ]; then sed -i 's/python/python2/g' systemd-notify.py;fi
xorg_user=$(w | grep ":0" | cut -d' ' -f1 | sort | uniq)
usermod -a -G systemd-journal $xorg_user
cp systemd-notify.py /usr/local/bin
cp systemd-notify.desktop /etc/xdg/autostart
chmod 0755 /usr/local/bin/systemd-notify.py
chmod 0644 /etc/xdg/autostart/systemd-notify.desktop
exit
