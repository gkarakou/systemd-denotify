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

class ConfigReader():
    """
    ConfigReader
    :desc: Class that reads the user config for entries
    Has an constructor and 3 section specific getters
    """

    def __init__(self):
        """
        __init__
        :desc: Constructor function that by returns a ConfigParser object
        """
        conf = ConfigParser.RawConfigParser()
        self.conf = conf
        return  self.conf

    #def get_global_entries(self):


    def get_notification_entries(self):

        self.conf.read('/etc/systemd-denotify.conf')
        dictionary = {}
        #parse Logins
        dictionary['conf_logins_start'] = self.conf.getboolean("Logins", "start")
        #parse FailedServices
        dictionary['conf_failed_services_start'] = self.conf.getboolean("FailedServices", "start")
        #parse Files section
        dictionary['conf_files_start'] = self.conf.getboolean("Files", "start")
        dictionary['conf_files_dirs'] = self.conf.get("Files", "directories")
        dictionary['conf_files_directories'] = dictionary['conf_files_dirs'].split(",")
        #parse ServicesStatus
        dictionary['conf_services_start'] = self.conf.getboolean("ServicesStatus", "start")
        dictionary['conf_services_interval'] = self.conf.getint("ServicesStatus", "interval")
        dictionary['conf_services_services'] = self.conf.get("ServicesStatus", "services")
        dictionary['conf_services'] = dictionary['conf_services_services'].split(",")

        return dictionary

    def get_mail_entries(self):
        self.conf.read('/etc/systemd-denotify.conf')
        dictionary = {}
        dictionary['conf_email_on_user_logins'] = self.conf.getboolean("EMAIL_NOTIFICATIONS", "email_on_user_logins")
        dictionary['conf_email_on_failed_services'] = self.conf.getboolean("EMAIL_NOTIFICATIONS", "email_on_failed_services")
        dictionary['conf_email_on_file_alteration'] = self.conf.getboolean("EMAIL_NOTIFICATIONS", "email_on_file_alteration")
        dictionary['conf_email_on_services_statuses'] = self.conf.getboolean("EMAIL_NOTIFICATIONS", "email_on_services_statuses")

        dictionary['conf_email_subject'] = self.conf.get("EMAIL", "mail_subject")
        dictionary['conf_email_to'] = self.conf.get("EMAIL", "mail_to")
        dictionary['conf_email_from'] = self.conf.get("EMAIL", "mail_from")


        #parse [AUTH]

        auth = conf.getboolean("AUTH", "active")
        if auth and auth == True:
            auth_user = conf.get("AUTH", "auth_user")
            if len(auth_user) == 0:
                if self.logg == True and self.logg_facility == "both":
                    self.logging.error("You have asked for authentication but you have an empty auth_user name. Please update the /etc/systemd-mailify.conf file with a value ")
                    journal.send("systemd-mailify: ERROR You have asked for authentication but you have an empty auth_user name. Please update the /etc/systemd-mailify.conf file with a value ")
                elif self.logg == True and self.logg_facility == "log_file":
                    self.logging.error("You have asked for authentication but you have an empty auth_user name. Please update the /etc/systemd-mailify.conf file with a value ")
                else:
                    journal.send("systemd-mailify: ERROR You have asked for authentication but you have an empty auth_user name. Please update the /etc/systemd-mailify.conf file with a value ")
                sys.exit(1)
            auth_password = conf.get("AUTH", "auth_password")
            if len(auth_password) == 0:
                if self.logg == True and self.logg_facility == "both":
                    self.logging.error("You have asked for authentication but you have an empty auth_password field. Please update the /etc/systemd-mailify.conf file with a value ")
                    journal.send("systemd-mailify: ERROR You have asked for authentication but you have an empty auth_password field. Please update the /etc/systemd-mailify.conf file with a value ")
                elif self.logg == True and self.logg_facility == "log_file":
                    self.logging.error("You have asked for authentication but you have an empty auth_password field. Please update the /etc/systemd-mailify.conf file with a value ")
                else:
                    journal.send("systemd-mailify: ERROR You have asked for authentication but you have an empty auth_password field. Please update the /etc/systemd-mailify.conf file with a value ")
                sys.exit(1)
            conf_dict['auth'] = True
            conf_dict['auth_user'] = auth_user
            conf_dict['auth_password'] = auth_password
        else:
            conf_dict['auth'] = False

        #parse [SMTP]
        smtp = conf.getboolean("SMTP", "active")
        if smtp and smtp == True:
            conf_dict['smtp'] = True
        else:
            conf_dict['smtp'] = False
        smtp_host = conf.get("SMTP", "host")
        if len(smtp_host) == 0:
            smtp_host = "localhost"
            if self.logg == True and self.logg_facility == "both":
                self.logging.info("You have asked for smtp connection but you have an empty smtp host field. Please update the /etc/systemd-mailify.conf file with a value. We assume localhost here")
                journal.send("systemd-mailify: INFO You have asked for a smtp connection but you have an empty smtp host field. Please update the /etc/systemd-mailify.conf file with a value. We assume localhost here")
            elif self.logg == True and self.logg_facility == "log_file":
                self.logging.info("You have asked for smtp connection but you have an empty smtp host field. Please update the /etc/systemd-mailify.conf file with a value. We assume localhost here")
            else:
                journal.send("systemd-mailify: INFO You have asked for a smtp  connection but you have an empty smtp host field. Please update the /etc/systemd-mailify.conf file with a value. We assume localhost here")
        conf_dict['smtp_host'] = smtp_host
        smtp_port = conf.getint("SMTP", "port")
        if not smtp_port:
            smtp_port = 25
        

        return dictionary

class ServiceStatusChecker():
    """
    ServiceStatusChecker
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
        conf_reader = ConfigReader()
        dictio = conf_reader.get_notification_entries()

        if isinstance(dictio['conf_services_start'], bool) and dictio['conf_services_start'] == False:
            return False
        elif dictio['conf_services_start'] == True and
        isinstance(dictio['conf_services_interval'], int) and isinstance(dictio['conf_services'], list):
            secs = int(dictio['conf_services_interval']) * 60
            threading.Timer(secs, self.run).start()
            bus = SystemBus()
            systemd = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
            manager = Interface(systemd, dbus_interface='org.freedesktop.systemd1.Manager')

            append = ".service"
            for a in dictio['conf_services']:
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

class LogindMonitor(threading.Thread):
    """
    LogindMonitor
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

class JournalParser(threading.Thread):
    """
    JournalParser
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

    db = ServiceStatusChecker()
    db.run()

    if isinstance(config_files_start, bool) and config_files_start == True:
        FileNotifier()
    if isinstance(config_logreader_start, bool) and config_logreader_start == True:
        lg = JournalParser()
        lg.daemon = True
        lg.start()
    if isinstance(config_logins_start, bool) and config_logins_start == True:
        lm = LogindMonitor()
        lm.run()
