#!/bin/bash
if [ -f /etc/pacman.conf ]; then sed -i 's/python/python2/g' systemd-notify.py
cp systemd-notify.py /usr/local/bin
cp systemd-notify.desktop /etc/xdg/autostart
chmod 0755 /usr/local/bin/systemd-notify.py
chmod 0644 /etc/xdg/autostart/systemd-notify.desktop
exit
