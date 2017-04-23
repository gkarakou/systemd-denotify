#!/bin/sh
getXuser=`/usr/bin/w |grep :0|cut -d " " -f1|sort|uniq`
#fedora
getXorgUser=`/usr/bin/ps -aux|/usr/bin/grep Xorg|/usr/bin/cut -d " " -f1|/usr/bin/sort|/usr/bin/uniq`
getXwaylandUser=`/usr/bin/ps -aux|/usr/bin/grep "Xwayland :0"|/usr/bin/cut -d " " -f1|/usr/bin/sort|/usr/bin/uniq`
if [ ! -z "$getXuser" ];then
/usr/sbin/usermod -a -G systemd-journal $getXuser
elif [ ! -z "$getXorgUser" ];then
/usr/sbin/usermod -a -G systemd-journal $getXorgUser
else [ ! -z "$getXwaylandUser" ];then
/usr/sbin/usermod -a -G systemd-journal $getXwaylandUser
fi
exit 0;
