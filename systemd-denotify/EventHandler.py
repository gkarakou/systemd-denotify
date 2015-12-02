#!/usr/bin/python2
from .ConfigReader import ConfigReader
from .Mailer import Mailer
from systemd import journal
from gi.repository import Notify
import pyinotify
import inspect

class EventHandler(pyinotify.ProcessEvent):

    def __init__(self):
        """
        __init__
        return parent constructor
        """
        pyinotify.ProcessEvent.__init__(self)
        conf = ConfigReader()
        #self.desktop_dictio = conf.get_notification_entries()
        self.mail_dictio = conf.get_mail_entries()
        self.strings = ""

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
        for k, v in self.mail_dictio.iteritems():
            if k == 'email_on_file_alteration' and v == True:
                self.wait_for(string1)
                #mail = Mailer()
                #mail.run(string1, self.mail_dictio)

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
        for k, v in self.mail_dictio.iteritems():
            if k == 'email_on_file_alteration' and v == True:
                self.wait_for(string1)
            #    mail = Mailer()
            #    mail.run(string1, self.mail_dictio)

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
        for k, v in self.mail_dictio.iteritems():
            if k == 'email_on_file_alteration' and v == True:
                mail = Mailer()
                mail.run(string1, self.mail_dictio)

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
        for k, v in self.mail_dictio.iteritems():
            if k == 'email_on_file_alteration' and v == True:
                mail = Mailer()
                mail.run(string1, self.mail_dictio)

    def get_caller(self):
        return inspect.stack()[2][3]

    def wait_for(self, string):
        caller = self.get_caller()
        strings = ""
        if caller == "process_IN_MODIFY":
            self.strings += string + "\r\n"
        #    print "inside wait_for in if process_IN_MODIFY " + self.strings
            return self.strings
        elif caller == "process_IN_CLOSE_WRITE":
            self.strings += string + "\r\n"
         #   print "inside wait_for in elif process_IN_CLOSE_WRITE " + self.strings
            mail = Mailer()
            mail.run(self.strings, self.mail_dictio)

