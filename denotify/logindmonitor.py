#!/usr/bin/python2
from .configreader import ConfigReader
from .mailer import Mailer
import threading
import select
from systemd import login
import time
import datetime
from systemd import journal
from threading import Thread
from gi.repository import Notify

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
        conf = ConfigReader()
        dictiona = conf.get_mail_entries()
        email = False
        for k, v in dictiona.iteritems():
            if k == 'email_on_user_logins' and v == True:
                email = True
        while True:
            time.sleep(1)
            monitor_uids = login.Monitor("uid")
            poller = select.poll()
            poller.register(monitor_uids, monitor_uids.get_events())
            poller.poll()
            users = login.uids()
            for user in users:
                now = datetime.datetime.now()
                Notify.init("systemd-denotify")
                notificatio = Notify.Notification.new("systemd-denotify", "login from user id: "+str(user) +" at "+str(now)[:19])
                notificatio.show()
                if email == True:
                    mail = Mailer()
                    mail.run("login from user id: "+str(user) +" at "+str(now)[:19], dictiona)
                break

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

