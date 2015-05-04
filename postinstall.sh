#!/bin/sh
getXuser=`/usr/bin/w |grep :0|cut -d " " -f1|sort|uniq`
if [ ! -z "$getXuser" ];then
/sbin/usermod -a -G systemd-journal $getXuser
fi
exit 0;
