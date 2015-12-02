#!/usr/bin/python2
from .ConfigReader import ConfigReader
from .Mailer import Mailer
import threading
import select
import datetime
from systemd import journal
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
        dictiona = conf.get_mail_entries()
        dictionn = conf.get_notification_entries()
        #make a new list holding the values of patterns and/or failedservices
        patterns = []
        if isinstance(dictionn['conf_pattern_matcher_start'], bool) and dictionn['conf_pattern_matcher_start'] == True:
            for p in dictionn['conf_pattern_patterns']:
                patterns.append(p)
        if isinstance(dictionn['conf_failed_services_start'], bool) and dictionn['conf_failed_services_start'] == True:
            patterns.append("entered failed state")
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
                        try:
                            string = entry['MESSAGE']
                            for pattern in patterns:
                                if string and pattern in string:
                                    Notify.init("systemd-denotify")
                                    notificatio = Notify.Notification.new("systemd-denotify", string)
                                    notificatio.show()
                                    if notificatio:
                                        del notificatio
                                    for key, value in dictiona.iteritems():
                                        if key == 'email_on_failed_services' and value == True or key == 'email_on_journal_pattern_match' and value == True:
                                            mail = Mailer()
                                            mail.run(string, dictiona)
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

