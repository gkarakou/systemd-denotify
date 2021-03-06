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

class LogindMonitor():
    """
    LogindMonitor
    :desc: Class that notifies the user for user logins
    Extends threading.Thread
    Has a constructor that calls the parent one, a run method and a destructor
    """

    def __init__(self):
        """
        __init__
        return daemon thread start
        """
        #Thread.__init__(self)
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()

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
        Notify.init("systemd-denotify")
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
            #journal.send("systemd-denotify: inside logindmonitor run()")
            for user in users:
                now = datetime.datetime.now()
                notificatio = Notify.Notification.new("systemd-denotify","login from user id: "+str(user) +" at "+str(now)[:19])
                notificatio.show()
             #   journal.send("systemd-denotify: inside logindmonitor run() and user loop")
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

