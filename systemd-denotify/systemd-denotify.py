#!/usr/bin/python2
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
import ConfigParser
import pyinotify

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

    def run(self):
        """
        run
        return False or void
        :desc: function that starts (or not) a timer thread based on user input
        Helpful API->http://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.html
        Helpful API->http://www.freedesktop.org/wiki/Software/systemd/dbus/
        Credits->https://zignar.net/2014/09/08/getting-started-with-dbus-python-systemd/
        """
        conf = ConfigParser.RawConfigParser()
        conf.read('/etc/systemd-denotify.conf')
        config_start = conf.getboolean("ServicesStatus", "start")
        config_interval = conf.getint("ServicesStatus", "interval")
        config_serv = conf.get("ServicesStatus", "services")
        config_services = config_serv.split(",")

        if isinstance(config_start, bool) and config_start == False:
            return False
        elif config_start == True and isinstance(config_interval, int) and isinstance(config_services, list):
            secs = int(config_interval) * 60
            threading.Timer(secs, self.run).start()
            bus = SystemBus()
            systemd = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
            manager = Interface(systemd, dbus_interface='org.freedesktop.systemd1.Manager')

            append = ".service"
            for a in config_services:
                a+= append
                try:
                    getUnit = manager.LoadUnit(a)
                except  Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    journal.send("systemd-denotify: "+message)
                try:
                    proxy = bus.get_object('org.freedesktop.systemd1', getUnit)
                except  Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    journal.send("systemd-denotify: "+message)
                try:
                    service_properties = Interface(proxy, dbus_interface='org.freedesktop.DBus.Properties')
                except Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    journal.send("systemd-denotify: "+message)
                try:
                    state = service_properties.Get('org.freedesktop.systemd1.Unit', 'ActiveState')
                except Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    journal.send("systemd-denotify: "+message)
                status = a + " status: %s" % state
                try:
                    Notify.init("systemd-denotify")
                    notificated = Notify.Notification.new("systemd-denotify", status)
                    notificated.show()
                except Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    journal.send("systemd-denotify: "+message)
                if notificated:
                    del notificated
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
                journal.send("systemd-denotify: "+message)
            poller = select.poll()
            try:
                poller.register(monitor_uids, monitor_uids.get_events())
            except Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                journal.send("systemd-denotify: "+message)
            poller.poll()
            users = login.uids()
            for user in users:
                now = datetime.datetime.now()
                try:
                    Notify.init("systemd-denotify")
                    notificatio = Notify.Notification.new("systemd-denotify", "login from user id: "+str(user) +" at "+str(now)[:19])
                    notificatio.show()
                except Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    journal.send("systemd-denotify: "+message)
                if notificatio:
                    del notificatio

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
                                Notify.init("systemd-denotify")
                                notificatio=Notify.Notification.new("systemd-denotify", string)
                                notificatio.show()
                                if notificatio:
                                    del notificatio
                            else:
                                continue
                        except Exception as ex:
                            template = "An exception of type {0} occured. Arguments:\n{1!r}"
                            message = template.format(type(ex).__name__, ex.args)
                            journal.send("systemd-denotify: "+message)
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

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        string1 = "file " +event.pathname + " written"
        try:
            Notify.init("systemd-denotify")
            notificatio = Notify.Notification.new("systemd-denotify", string1)
            notificatio.show()
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            journal.send("systemd-denotify: "+message)

    def process_IN_MODIFY(self, event):
        string1 = "file " +event.pathname + " modified"
        try:
            Notify.init("systemd-denotify")
            notificatio = Notify.Notification.new("systemd-denotify", string1)
            notificatio.show()
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            journal.send("systemd-denotify: "+message)

    def process_IN_MOVED_TO(self, event):
        string1 = "file " +event.pathname + " overwritten"
        try:
            Notify.init("systemd-denotify")
            notificatio = Notify.Notification.new("systemd-denotify", string1)
            notificatio.show()
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            journal.send("systemd-denotify: "+message)

    def process_IN_ATTRIB(self, event):
        string1 = "files " +event.pathname + " metadata changed"
        try:
            Notify.init("systemd-denotify")
            notificatio = Notify.Notification.new("systemd-denotify", string1)
            notificatio.show()
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            journal.send("systemd-denotify: "+message)


class FileNotifier():
    def __init__(self):
        configure = ConfigParser.RawConfigParser()
        configure.read('/etc/systemd-denotify.conf')
        config_dirs = configure.get("Files", "directories")
        config_directories = config_dirs.split(",")
        mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MODIFY |pyinotify.IN_MOVED_TO # watched events
        wm = pyinotify.WatchManager()
        notifier = pyinotify.ThreadedNotifier(wm, EventHandler())
        notifier.start()
        # Start watching  paths
        for d in config_directories:
            wm.add_watch(d, mask, rec=True)


if __name__ == "__main__":
    """
    __main__
    :desc: Somewhat main function though we are linux only
    based on user configuration starts classes
    """

    try:
        config = ConfigParser.RawConfigParser()
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        journal.send("systemd-denotify: "+message)
    try:
        config.read('/etc/systemd-denotify.conf')
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        journal.send("systemd-denotify: "+message)
    config_files_start = config.getboolean("Files", "start")
    config_logins_start = config.getboolean("Logins", "start")
    try:
        config_logreader_start = config.getboolean("FailedServices", "start")
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        journal.send("systemd-denotify: "+message)
    try:
        config_services_start = config.getboolean("ServicesStatus", "start")
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        journal.send("systemd-denotify: "+message)

    db = DbusNotify()
    db.run()

    if isinstance(config_files_start, bool) and config_files_start == True:
        FileNotifier()
    if isinstance(config_logreader_start, bool) and config_logreader_start == True:
        lg = LogReader()
        lg.daemon = True
        lg.start()
    if isinstance(config_logins_start, bool) and config_logins_start == True:
        lm = logindMonitor()
        lm.run()
