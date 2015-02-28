#!/usr/bin/python
from dbus import SystemBus, Interface
import threading
import select
from systemd import login
import time
import datetime
from systemd import journal
from threading import Thread
from gi.repository import Notify
import os

class DbusNotify():

    def __init__(self):
        pass

    def run(self):
        '''API->http://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.html'''
        '''API->http://www.freedesktop.org/wiki/Software/systemd/dbus/'''
        '''Credits->https://zignar.net/2014/09/08/getting-started-with-dbus-python-systemd/'''

        threat = threading.Timer(1800, self.run).start()
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
                journal.send("systemd-notify: "+message)
            try:
                proxy = bus.get_object('org.freedesktop.systemd1', getUnit)
            except  Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                journal.send("systemd-notify: "+message)
            try:
                service_properties = Interface(proxy, dbus_interface='org.freedesktop.DBus.Properties')
            except Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                journal.send("systemd-notify: "+message)
            try:
                state = service_properties.Get('org.freedesktop.systemd1.Unit', 'ActiveState')
            except Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                journal.send("systemd-notify: "+message)
            status = a + " status: %s" % state
            try:
                Notify.init("systemd-notify")
                notificated = Notify.Notification.new("systemd-notify", status)
                notificated.show()
            except Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                journal.send("systemd-notify: "+message)
        return


class logindMonitor(threading.Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        '''API->http://www.freedesktop.org/software/systemd/python-systemd/'''

        while True:
            time.sleep(1)
            try:
                monitor_uids = login.Monitor("uid")
            except Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                journal.send("systemd-notify: "+message)
            poller = select.poll()
            try:
                poller.register(monitor_uids, monitor_uids.get_events())
            except Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                journal.send("systemd-notify: "+message)
            poller.poll()
            users = login.uids()
            for user in users:
                now = datetime.datetime.now()
                try:
                    Notify.init("systemd-notify")
                    notificatio = Notify.Notification.new("systemd-notify", "login from user id: "+str(user) +" at "+str(now)[:19])
                    notificatio.show()
                except Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    journal.send("systemd-notify: "+message)

    def __del__(self):

        #this wont run but we provide it for completeness
        if callable(getattr(threading.Thread, "__del__")):
            super.__del__()
            return
        else:
            del self.run
            return 

class LogReader(threading.Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):

        '''API->http://www.freedesktop.org/software/systemd/python-systemd/'''

        j_reader = journal.Reader()
        j_reader.log_level(journal.LOG_INFO)
        # j.seek_tail() #faulty->doesn't move the cursor to the end of journal

        # it is questionable whether there is actually a record with the real
        # datetime we provide but we assume it moves the cursor to somewhere
        # near the end of the journal fd
        j_reader.seek_realtime(datetime.datetime.now())
        poller = select.poll()
        poller.register(j_reader, j_reader.get_events())
        while poller.poll():
            #next is a debugging call
            # if it prints True it is pollable
            #reliable = j.reliable_fd()
            #print reliable
            waiting = j_reader.process()
            # if JOURNAL append or JOURNAL logrotate
            if waiting == 1 or waiting == 2:
                j_reader.get_next()
                for entry in j_reader:
                    if 'MESSAGE' in entry:
                        pattern = "entered failed state"
                        try:
                            string = entry['MESSAGE']
                            if string and pattern in string:
                                Notify.init("systemd-notify")
                                notificatio=Notify.Notification.new("systemd-notify", string)
                                notificatio.show()
                            else:
                                continue
                        except Exception as ex:
                            template = "An exception of type {0} occured. Arguments:\n{1!r}"
                            message = template.format(type(ex).__name__, ex.args)
                            journal.send("systemd-notify: "+message)
                    else:
                        continue
            else:
                pass
            continue

    def __del__(self):

        '''this wont run but we provide it for completeness'''
        if callable(getattr(threading.Thread, "__del__")):
            super.__del__()
            return 
        else:
            del self.run
            return 

if __name__ == "__main__":
    log_reader = LogReader()
    log_reader.daemon = True
    log_reader.start()
    lm = logindMonitor()
    lm.start()
    if isinstance(log_reader, object) & isinstance(lm, object):
        pid = os.getpid()
        js = journal.send("systemd-notify: successfully started logReader and logindMonitor instances with pid "+ str(pid))
        try:
            with open('/tmp/systemd-notify.pid', 'w') as of:
                of.write(str(pid))
        except Exception as ex:
            templated = "An exception of type {0} occured. Arguments:\n{1!r}"
            messaged = templated.format(type(ex).__name__, ex.args)
            journal.send("systemd-notify: "+messaged)

    #db = DbusNotify()
    #db_started=db.run()
