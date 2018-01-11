#!/usr/bin/python2
#import sys
#sys.path.append("/usr/lib/python2.7/site-packages")
from .configreader import ConfigReader
from .mailer import Mailer
import threading
import select
import datetime
import pyttsx3
from systemd import journal
from espeakng import ESpeakNG
from threading import Thread
from gi.repository import Notify

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
        return void(Actually returns None type in python)
        :desc: function that goes on an infinite loop polling the systemd-journal for failed services
        Helpful API->http://www.freedesktop.org/software/systemd/python-systemd/
        """
        conf = ConfigReader()
        dict_mail = conf.get_mail_entries()
        dict_notifications = conf.get_notification_entries()
        mail_on_failed = False
        espeak_on_failed = False
        mail_on_pattern = False
        for key, value in dict_mail.iteritems():
            if key == 'email_on_failed_services' and value == True:
                mail_on_failed = True
            if key == 'email_on_journal_pattern_match' and value == True:
                mail_on_pattern = True
        #make a new list holding the values of patterns and/or failedservices
        patterns = []
        if isinstance(dict_notifications['conf_pattern_matcher_start'], bool) and dict_notifications['conf_pattern_matcher_start'] == True:
            for pat in dict_notifications['conf_pattern_patterns']:
                patterns.append(pat)
        if isinstance(dict_notifications['conf_failed_services_start'], bool) and dict_notifications['conf_failed_services_start'] == True:
            patterns.append("entered failed state")
        if isinstance(dict_notifications['conf_failed_services_espeak'], bool) and dict_notifications['conf_failed_services_espeak'] == True:
            espeak_on_failed = True
        Notify.init("systemd-denotify")
        j_reader = journal.Reader()
        j_reader.log_level(journal.LOG_INFO)
        j_reader.seek_realtime(datetime.datetime.now())
        poller = select.poll()
        poller.register(j_reader, j_reader.get_events())
        while poller.poll():
            waiting = j_reader.process()
            # if JOURNAL append or JOURNAL logrotate
            if waiting == 1 or waiting == 2:
                j_reader.get_next()
                for entry in j_reader:
                    if 'MESSAGE' in entry:
                        try:
                            string = entry['MESSAGE']
                            for pattern in patterns:
                                if string and pattern in string:
                            #        Notify.init("systemd-denotify")
                                    notificatio = Notify.Notification.new("systemd-denotify", string)
                                    notificatio.show()
                                    if espeak_on_failed == True:
                                        #engine = pyttsx3.init()
                                        engine= ESpeakNG()
                                        stri = string.replace(".service:", "")
                                        engine.say(stri)
                                        #engine.runAndWait()
                                    else:
                                        pass
                                    if mail_on_failed == True or mail_on_pattern == True:
                                        mail = Mailer()
                                        mail.run(string, dict_mail)
                                    else:
                                        pass
                                else:
                                    pass
                        except Exception as ex:
                            template = "An exception of type {0} occured. Arguments:\n{1!r}"
                            message = template.format(type(ex).__name__, ex.args)
                            journal.send("systemd-denotify: "+message)
                        #journal.send("systemd-denotify: DEBUG: "+".. after 1st pattern..")
                            break
                    else:
                        pass

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

