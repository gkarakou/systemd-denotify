#!/usr/bin/python
from dbus import SystemBus, Interface
import threading
import select
from systemd import login
import time
import datetime
from systemd import journal
#import logging
from threading import Thread
from gi.repository import Notify
import os

class DbusNotify():

    def __init__(self):
        #print "inside DbusNotify.__init__: getting pid " +str(os.getpid())
        pass

    def run(self):
        self.t = threading.Timer(1800, self.run).start()
        #print "inside Dbus.run(): getting pid " +str(os.getpid())
        bus = SystemBus()
        systemd = bus.get_object(
            'org.freedesktop.systemd1',
            '/org/freedesktop/systemd1')
        manager = Interface(
            systemd,
            dbus_interface='org.freedesktop.systemd1.Manager')

        array = [
            "polkit.service",
            "systemd-logind.service",
            "systemd-udevd.service",
            "autovt@tty2.service",
            ]
        for a in array:
            try:
                getUnit = manager.LoadUnit(a)
            except  Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print message
            try:
                proxy = bus.get_object('org.freedesktop.systemd1', getUnit)
            except  Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print message
            try:
                service_properties = Interface(
                proxy,
                dbus_interface='org.freedesktop.DBus.Properties')
            except Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print message
            try:
                state = service_properties.Get(
                'org.freedesktop.systemd1.Unit',
                'ActiveState')
            except Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print message
            status = a + " status: %s" % state
            try:
                Notify.init("systemd-notify")
                n = Notify.Notification.new("systemd-notify", status)
                n.show()
            except Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print message
        return


class logindMonitor(threading.Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
            while True:
                    time.sleep(1)
                    mu = login.Monitor("uid")
                    p = select.poll()
                    p.register(mu, mu.get_events())
                    p.poll()
                    u = login.uids()
                    for user in u:
                        now = datetime.datetime.now()
                        Notify.init("systemd-notify")
                        n = Notify.Notification.new(
                        "systemd-notify",
                        "login from user id: " +
                        str(user) +
                        " at " +
                        str(now)[
                        :19])
                        n.show()

            return

class LogReader(threading.Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        j = journal.Reader()
        j.log_level(journal.LOG_INFO)
        # j.seek_tail() #faulty->doesn't move the cursor to the end of journal
        # it is questionable whether there is actually a record with the real
        # datetime we provide but we assume it moves the cursor to somewhere
        # near the end of the journal fd

        #print "inside LogReader.run(): getting pid " +str(os.getpid())
        j.seek_realtime(datetime.datetime.now())
        p = select.poll()
        p.register(j, j.get_events())
        # while True:
        #	time.sleep(1)
        while p.poll():
            reliable = j.reliable_fd()
            print reliable
            # if it prints True it is pollable
            waiting = j.process()
            # if JOURNAL append or JOURNAL logrotate
            if waiting == 1 or waiting == 2:
                j.get_next()
                for entry in j:
                    if 'MESSAGE' in entry:
                        pattern = "entered failed state"
                        try:
                            string = entry['MESSAGE'].decode('utf-8')
                            if string and pattern in string:
                                Notify.init("systemd-notify")
                                n=Notify.Notification.new(
                                    "systemd-notify",
                                    string)
                                n.show()
                            else:
                                continue
                        except Exception as ex:
                            template = "An exception of type {0} occured. Arguments:\n{1!r}" 
                            message = template.format(type(ex).__name__, ex.args)
                            print message
                    else:
                        continue
                        break
            else:
                print "journal has no new entries"
            continue

if __name__ == "__main__":
    main_pid=os.getpid()
    print "main pid: "+ str(main_pid)
    time.sleep(3)
    print "attempting to start logReader..."
    lr=LogReader()
    lr.daemon=True
    lr.start()
    time.sleep(3)
    print "attempting to start logindMonitor..."
    lm=logindMonitor()
    lm.start()
    db = DbusNotify()
    db.run()
