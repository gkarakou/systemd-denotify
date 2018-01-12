#!/usr/bin/python2
from denotify.configreader import ConfigReader
from denotify.servicestatuschecker import ServiceStatusChecker
from denotify.logindmonitor import LogindMonitor
from denotify.journalparser import JournalParser
from denotify.filenotifier import FileNotifier
from systemd import journal

if __name__ == "__main__":
    """
    __main__
    :desc: Somewhat main function though we are linux only
    based on user configuration starts classes
    """

    try:
        config = ConfigReader()
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        journal.send("systemd-denotify: "+message)
    try:
        diction = config.get_notification_entries()
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        journal.send("systemd-denotify: "+message)

##start classes
    if diction['conf_services_start'] == True:
        ssc = ServiceStatusChecker()
        ssc.run()

    if diction['conf_files_start'] == True:
        FileNotifier()
    if diction['conf_failed_services_start'] == True or diction['conf_pattern_matcher_start'] == True:
        jp = JournalParser()
        #jp.run()
        jp.daemon = True
        jp.start()
    if diction['conf_logins_start'] == True:
        lm = LogindMonitor()
        #lm.daemon = True
        lm.run()
