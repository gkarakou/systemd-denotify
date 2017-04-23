#!/bin/sh
getXuser=`/usr/bin/w |grep :0|cut -d " " -f1|sort|uniq`
#fedora
/usr/bin/unalias ps
getXorgUser=`/usr/bin/ps -aux|/usr/bin/grep Xorg|/usr/bin/cut -d " " -f1|/usr/bin/sort|/usr/bin/uniq`
getXwaylandUser=`/usr/bin/ps -aux|/usr/bin/grep "Xwayland :0"|/usr/bin/cut -d " " -f1|/usr/bin/sort|/usr/bin/uniq`
if [ ! -z "$getXuser" ];then
/usr/sbin/usermod -a -G systemd-journal $getXuser
elif [ ! -z "$getXorgUser" ];then
/usr/sbin/usermod -a -G systemd-journal $getXorgUser
elif [ ! -z "$getXwaylandUser" ];then
/usr/sbin/usermod -a -G systemd-journal $getXwaylandUser
else
echo " something went wrong. Please manually add the desktop user to systemd-journal group "
fi
exit 0;
