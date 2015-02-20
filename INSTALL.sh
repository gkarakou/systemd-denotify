#!/bin/bash
cp systemd-notify.py /usr/local/bin
cp systemd-notify.desktop /etc/xdg/autostart
chmod 0755 /usr/local/bin/systemd-notify.py
chmod 0644 /etc/xdg/autostart/systemd-notify.desktop
exit
