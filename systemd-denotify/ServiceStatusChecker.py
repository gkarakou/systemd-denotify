#!/usr/bin/python2
from .ConfigReader import ConfigReader
from .Mailer import Mailer
from dbus import SystemBus, Interface
import threading
from systemd import journal
from gi.repository import Notify

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
        dictionar = conf_reader.get_mail_entries()
        if isinstance(dictio['conf_services_start'], bool) and dictio['conf_services_start'] == False:
            return False
        elif dictio['conf_services_start'] == True and isinstance(dictio['conf_services_interval'], int) and isinstance(dictio['conf_services'], list):
            secs = int(dictio['conf_services_interval']) * 60
            threading.Timer(secs, self.run).start()
            bus = SystemBus()
            systemd = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
            manager = Interface(systemd, dbus_interface='org.freedesktop.systemd1.Manager')
            statuses = ""
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
                statuses += status + "\r\n"
                if notificated:
                    del notificated
            for k, v in dictionar.iteritems():
                if k == 'email_on_services_statuses' and v == True:
                    try:
                        mail = Mailer()
                        mail.run(statuses, dictionar)
                    except Exception as ex:
                        template = "An exception of type {0} occured. Arguments:\n{1!r}"
                        message = template.format(type(ex).__name__, ex.args)
                        journal.send("systemd-denotify: "+message)
        else:
            return False
