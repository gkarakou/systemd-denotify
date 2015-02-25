#!/bin/bash
if [ -f /etc/pacman.conf ]; then sed -i 's/python/python2/g' systemd-notify.py;fi
xorg_user=$(w | grep ":0" | cut -d' ' -f1 | sort | uniq)
if [ -z $xorg_user ]
then
    echo "either you dont have the w command line utility installed or you are not logged in to your desktop.\n Install w or login to a desktop session and rerun the script";
    exit
else
    usermod -a -G systemd-journal $xorg_user;
fi
cp systemd-notify.py /usr/local/bin
cp systemd-notify.desktop /etc/xdg/autostart
chmod 0755 /usr/local/bin/systemd-notify.py
chmod 0644 /etc/xdg/autostart/systemd-notify.desktop
if [ -f /etc/xdg/autostart/systemd-notify.desktop ] && [ -f /usr/local/bin/systemd-notify.py ];then echo "installation was successful";
else 
echo "something is wrong with your PATH env, or your current working directory is not systemd-notify.py.\n cd first or fix PATH issues and rerun the script.";
fi
exit
