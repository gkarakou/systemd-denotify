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
import sys

class DbusNotify():
    """
    DbusNotify 
    :desc: Class that notifies the user for the status of some systemd services
    Has an empty constructor and a run method
    """

    def __init__(self):
        """
        __init__ 
        :desc: Constructor function that by default does nothing
        """
        pass

    def run(self, *args):
        """
        run 
        return False or void   
        :param *args: user supplied args 
        :desc: function that starts (or not) a timer thread based on user input
        Helpful API->http://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.html
        Helpful API->http://www.freedesktop.org/wiki/Software/systemd/dbus/
        Credits->https://zignar.net/2014/09/08/getting-started-with-dbus-python-systemd/
        """
        if sys.argv[1] == "False":
            return False
        elif sys.argv[1] == "True":
            secs = int(sys.argv[2]) * 60
            threading.Timer(secs, self.run, args).start()
            bus = SystemBus()
            systemd = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
            manager = Interface(systemd, dbus_interface='org.freedesktop.systemd1.Manager')
            len_args = len(args)
            for a in args[3:len_args]:
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
        else:
            return False


class logindMonitor(threading.Thread):
    """
    logindMonitor
    :desc: Class that notifies the user for user logins
    Extends threading.Thread
    Has a constructor that calls the parent one, a run method and a destructor
    """

    def __init__(self):
        """
        __init__
        return parent constructor
        """
        Thread.__init__(self)

    def run(self):
        """
        run
        return void
        :desc: function that goes on an infinite loop polling the logind daemon for user logins 
        Helpful API->http://www.freedesktop.org/software/systemd/python-systemd/
        """

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
        """
        __del__
        return parent destructor or del objects
        :desc: destructor function that wont run because the gc will run first, but we provide it for completeness
        """
        if callable(getattr(threading.Thread, "__del__")):
            super.__del__()
            return
        else:
            del self.run
            return 

class LogReader(threading.Thread):
    """
    LogReader
    :desc: Class that notifies the user for failed systemd services 
    Extends threading.Thread
    Has an constructor that calls the parent one, a run method and a destructor
    """

    def __init__(self):
        """
        __init__
        return parent constructor
        """
        Thread.__init__(self)

    def run(self):
        """
        run
        return void
        :desc: function that goes on an infinite loop polling the systemd-journal for failed services
        Helpful API->http://www.freedesktop.org/software/systemd/python-systemd/
        """
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
        """__del__
        return parent destructor or del objects
        :desc: destructor function that wont run because the gc will run first, but we provide it for completeness
        """
        if callable(getattr(threading.Thread, "__del__")):
            super.__del__()
            return 
        else:
            del self.run
            return 

if __name__ == "__main__":
    """
    __main__
    :desc: Somewhat main function though we are linux only
    Starts logReader and logindMonitor instances (threads)
    Writes pid file on /tmp cause we dont have and dont want root rights
    based on user input
    Instantiates DbusNotify class and starts run function with string args (True/False, time, services)
    """
    log_reader = LogReader()
    log_reader.daemon = True
    log_reader.start()
    lm = logindMonitor()
    lm.start()
    if isinstance(log_reader, object) & isinstance(lm, object):
        pid = os.getpid()
        js = journal.send("systemd-notify: successfully started with pid "+ str(pid))
        try:
            with open('/tmp/systemd-notify.pid', 'w') as of:
                of.write(str(pid))
        except Exception as ex:
            templated = "An exception of type {0} occured. Arguments:\n{1!r}"
            messaged = templated.format(type(ex).__name__, ex.args)
            journal.send("systemd-notify: "+messaged)
    db = DbusNotify()
    db_started = db.run(*sys.argv)
