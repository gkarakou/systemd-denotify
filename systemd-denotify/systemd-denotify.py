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
import ConfigParser
import pyinotify
import smtplib
import email.utils
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    #def get_global_entries(self):


    def get_notification_entries(self):

        conf = ConfigParser.RawConfigParser()
        conf.read('/etc/systemd-denotify.conf')
        dictionary = {}
        #parse Logins
        dictionary['conf_logins_start'] = conf.getboolean("Logins", "start")
        #parse FailedServices
        dictionary['conf_failed_services_start'] = conf.getboolean("FailedServices", "start")
        #parse Files section
        dictionary['conf_files_start'] = conf.getboolean("Files", "start")
        dictionary['conf_files_dirs'] = conf.get("Files", "directories")
        dictionary['conf_files_directories'] = dictionary['conf_files_dirs'].split(",")
        dictionary['conf_files_evs'] = conf.get("Files", "events")
        dictionary['conf_files_events'] = dictionary['conf_files_evs'].split(",")
        #parse ServicesStatus
        dictionary['conf_services_start'] = conf.getboolean("ServicesStatus", "start")
        dictionary['conf_services_interval'] = conf.getint("ServicesStatus", "interval")
        dictionary['conf_services_services'] = conf.get("ServicesStatus", "services")
        dictionary['conf_services'] = dictionary['conf_services_services'].split(",")

        return dictionary

    def get_mail_entries(self):
        conf = ConfigParser.RawConfigParser()
        conf.read('/etc/systemd-denotify.conf')
        dictionary = {}
        dictionary = {}
        dictionary['conf_email_on_user_logins'] = conf.getboolean("EMAIL_NOTIFICATIONS", "email_on_user_logins")
        dictionary['conf_email_on_failed_services'] = conf.getboolean("EMAIL_NOTIFICATIONS", "email_on_failed_services")
        dictionary['conf_email_on_file_alteration'] = conf.getboolean("EMAIL_NOTIFICATIONS", "email_on_file_alteration")
        dictionary['conf_email_on_services_statuses'] = conf.getboolean("EMAIL_NOTIFICATIONS", "email_on_services_statuses")

        dictionary['conf_email_subject'] = conf.get("EMAIL", "subject")
        dictionary['conf_email_to'] = conf.get("EMAIL", "mail_to")
        dictionary['conf_email_from'] = conf.get("EMAIL", "mail_from")


        #parse [AUTH]

        auth = conf.getboolean("AUTH", "active")
        if auth and auth == True:
            auth_user = conf.get("AUTH", "auth_user")
            if len(auth_user) == 0:
                sys.exit(1)
            auth_password = conf.get("AUTH", "auth_password")
            if len(auth_password) == 0:
                sys.exit(1)
            dictionary['auth'] = True
            dictionary['auth_user'] = auth_user
            dictionary['auth_password'] = auth_password
        else:
            dictionary['auth'] = False

        #parse [SMTP]
        smtp = conf.getboolean("SMTP", "active")
        if smtp and smtp == True:
            dictionary['smtp'] = True
        else:
            dictionary['smtp'] = False
        smtp_host = conf.get("SMTP", "host")
        if len(smtp_host) == 0:
            smtp_host = "localhost"
        dictionary['smtp_host'] = smtp_host
        smtp_port = conf.getint("SMTP", "port")
        if not smtp_port:
            smtp_port = 25
        dictionary['smtp_port'] = smtp_port

        #parse [SMTPS]
        smtps = conf.getboolean("SMTPS", "active")
        if smtps == True:
            dictionary['smtps'] = True
            smtps_host = conf.get("SMTPS", "host")
            if len(smtps_host) == 0:
                smtps_host = "localhost"
            dictionary['smtps_host'] = smtps_host
            smtps_port = conf.getint("SMTPS", "port")
            if not smtps_port:
                smtps_port = 465
            dictionary['smtps_port'] = smtps_port
            smtps_cert = conf.get("SMTPS", "cert_file")
            dictionary['smtps_cert'] = smtps_cert
            smtps_key = conf.get("SMTPS", "key_file")
            dictionary['smtps_key'] = smtps_key
        else:
            dictionary['smtps'] = False

        #parse [STARTTLS]
        starttls = conf.getboolean("STARTTLS", "active")
        if  starttls == True:
            dictionary['starttls'] = True
            starttls_host = conf.get("STARTTLS", "host")
            if len(starttls_host) == 0:
                starttls_host = "localhost"

            dictionary['starttls_host'] = starttls_host
            starttls_port = conf.getint("STARTTLS", "port")
            if not starttls_port:
                starttls_port = 587
            dictionary['starttls_port'] = starttls_port
            starttls_cert = conf.get("STARTTLS", "cert_file")
            dictionary['starttls_cert'] = starttls_cert
            starttls_key = conf.get("STARTTLS", "key_file")
            dictionary['starttls_key'] = starttls_key
        else:
            dictionary['starttls'] = False
        #iter through dict sections and check whether there are empty values
        return dictionary

class Mailer(threading.Thread):
    """
    Mailer
    :desc: Class that sends an email
    Extends Thread
    """

    def __init__(self):
        """
        __init__
        :desc: Constructor function that calls parent
        """

        Thread.__init__(self)

    def run(self, stri, dictio):
        """
        run
        :desc : Function that does the heavy lifting
        :params : The string to be mailed and a dict
        containing config options necessary for the mail to be delivered.
        """

        dictionary = dictio
        msg = MIMEMultipart("alternative")
        #get it from the queue?
        stripped = stri.strip()
        part1 = MIMEText(stripped, "plain")
        msg['Subject'] = dictionary['email_subject']
        #http://pymotw.com/2/smtplib/
        msg['To'] = email.utils.formataddr(('Recipient', dictionary['email_to']))
        msg['From'] = email.utils.formataddr((dictionary['email_from'], dictionary['email_from']))
        msg.attach(part1)
        if dictionary['smtp'] == True:
            # no auth
            if dictionary['auth'] == False:
                s = smtplib.SMTP()
                s.connect(host=str(dictionary['smtp_host']), port=dictionary['smtp_port'])
                try:
                    send = s.sendmail(str(dictionary['email_from']), [str(dictionary['email_to'])], msg.as_string())
                except Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    journal.send("systemd-denotify: "+message)
                finally:
                    s.quit()
                    del s

            # auth
            elif dictionary['auth'] == True:
                s = smtplib.SMTP()
                s.connect(host=str(dictionary['smtp_host']), port=dictionary['smtp_port'])
                s.login(str(dictionary['auth_user']), str(dictionary['auth_password']))
                try:
                    send = s.sendmail(str(dictionary['email_from']), [str(dictionary['email_to'])], msg.as_string().strip())
                except Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    journal.send("systemd-denotify: "+message)
                finally:
                     s.quit()
                     del s
            else:
                pass
        #smtps
        if dictionary['smtps'] == True:
            # no auth ?
            if  dictionary['auth'] == False:
                try:
                    if len(dictionary['smtps_cert']) >0 and len(dictionary['smtps_key'])>0:
                        s = smtplib.SMTP_SSL(host=str(dictionary['smtps_host']), port=dictionary['smtps_port'], keyfile=dictionary['smtps_key'], certfile=dictionary['smtps_cert'])
                        s.ehlo_or_helo_if_needed()
                        send = s.sendmail(str(dictionary['email_from']), [str(dictionary['email_to'])], msg.as_string())
                    else:
                        s = smtplib.SMTP_SSL(host=str(dictionary['smtps_host']), port=dictionary['smtps_port'])
                        s.ehlo_or_helo_if_needed()
                        send = s.sendmail(str(dictionary['email_from']), [str(dictionary['email_to'])], msg.as_string())
                except Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    journal.send("systemd-denotify: "+message)
                finally:
                    s.quit()
                    del s
            # auth
            elif dictionary['auth'] == True:
                try:
                    #check whether it is a real file and pem encoded
                    if len(dictionary['smtps_cert']) >0 and len(dictionary['smtps_key'])>0:
                        s = smtplib.SMTP_SSL(host=str(dictionary['smtps_host']), port=dictionary['smtps_port'], keyfile=dictionary['smtps_key'], certfile=dictionary['smtps_cert'])
                        s.ehlo_or_helo_if_needed()
                        s.login(dictionary['auth_user'], dictionary['auth_password'])
                        send = s.sendmail(str(dictionary['email_from']), [str(dictionary['email_to'])], msg.as_string())
                    else:
                        s = smtplib.SMTP_SSL(host=str(dictionary['smtps_host']), port=dictionary['smtps_port'])
                        s.ehlo_or_helo_if_needed()
                        s.login(dictionary['auth_user'], dictionary['auth_password'])
                        send = s.sendmail(str(dictionary['email_from']), [str(dictionary['email_to'])], msg.as_string())
                except Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    journal.send("systemd-denotify: "+message)
                finally:
                    s.quit()
                    del s
            else:
                pass
        #starttls
        if dictionary['starttls'] == True:
            # no auth
            if dictionary['auth'] == False:
                try:
                    s = smtplib.SMTP()
                    s.connect(host=str(dictionary['starttls_host']), port=dictionary['starttls_port'])
                    s.ehlo()
                    #http://pymotw.com/2/smtplib/
                    if s.has_extn("STARTTLS"):
                        #check whether it is a real file and pem encoded
                        if len(dictionary['starttls_cert']) >0 and len(dictionary['starttls_key'])>0:
                            s.starttls(keyfile=dictionary['starttls_key'], certfile=dictionary['starttls_cert'])
                            s.ehlo()
                            send = s.sendmail(str(dictionary['email_from']), [str(dictionary['email_to'])], msg.as_string())
                        else:
                            s.starttls()
                            s.ehlo()
                            send = s.sendmail(str(dictionary['email_from']), [str(dictionary['email_to'])], msg.as_string())
                except Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    journal.send("systemd-denotify: "+message)
                finally:
                    s.quit()
                    del s
            # auth
            elif dictionary['auth'] == True:
                try:
                    s = smtplib.SMTP()
                    s.connect(host=str(dictionary['starttls_host']), port=dictionary['starttls_port'])
                    #http://pymotw.com/2/smtplib/
                    s.ehlo()
                    if s.has_extn("STARTTLS"):
                        #check whether it is a real file and pem encoded
                        if len(dictionary['starttls_cert']) >0 and len(dictionary['starttls_key'])>0:
                            s.starttls(keyfile=dictionary['starttls_key'], certfile=dictionary['starttls_cert'])
                            s.ehlo()
                            s.login(str(dictionary['auth_user']).strip(), str(dictionary['auth_password']))
                            send = s.sendmail(str(dictionary['email_from']), [str(dictionary['email_to'])], msg.as_string())
                        else:
                            s.starttls()
                            s.ehlo()
                            s.login(str(dictionary['auth_user']).strip(), str(dictionary['auth_password']))
                            send = s.sendmail(str(dictionary['email_from']), [str(dictionary['email_to'])], msg.as_string())
                except Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    journal.send("systemd-denotify: "+message)
                finally:
                    s.quit()
                    del s
            else:
                pass


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
        elif dictionar['email_on_services_statuses'] == True and dictio['conf_services_start'] == True and isinstance(dictio['conf_services_interval'], int) and isinstance(dictio['conf_services'], list):
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
                    mail = Mailer()
                    mail.run(status, dictionar)
                except Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    journal.send("systemd-denotify: "+message)
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
        conf = ConfigReader()
        dictiona = conf.get_mail_entries()
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
                if dictiona['email_on_user_logins'] == True:
                    mail = Mailer()
                    mail.run("login from user id: "+str(user) +" at "+str(now)[:19], diction)
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
        conf = ConfigReader()
        dictiona = conf.get_mail_entries()
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
                                if dictiona['email_on_failed_services'] == True:
                                    mail = Mailer()
                                    mail.run(string, diction)
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

    def __init__(self):
        """
        __init__
        return parent constructor
        """
        pyinotify.ProcessEvent.__init__(self)
        conf = ConfigReader()
        #self.desktop_dictio = conf.get_notification_entries()
        self.mail_dictio = conf.get_mail_entries()

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
        if self.mail_dictio['email_on_file_alteration'] == True:
            mail = Mailer()
            mail.run(string1, self.mail_dictio)

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
        if self.mail_dictio['email_on_file_alteration'] == True:
            mail = Mailer()
            mail.run(string1, self.mail_dictio)

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
        if self.mail_dictio['email_on_file_alteration'] == True:
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
        if self.mail_dictio['email_on_file_alteration'] == True:
            mail = Mailer()
            mail.run(string1, self.mail_dictio)


class FileNotifier():
    def __init__(self):
        c_read = ConfigReader()
        dictio = c_read.get_notification_entries()
        #mappings = {"WRITE":pyinotify.IN_CLOSE_WRITE, "MODIFY":pyinotify.IN_MODIFY, "DELETE":pyinotify.IN_DELETE, "ATTRIBUTE":pyinotify.IN_ATTRIB}
        mappings = {"WRITE":8, "MODIFY":2, "DELETE":512, "ATTRIBUTE":4}
        mask =[]
        mask1 = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MODIFY | pyinotify.IN_DELETE
        for k, v in enumerate(dictio['conf_files_events']):
            for key, value in mappings.iteritems():
                if  k == len(dictio['conf_files_events']) -1:
                    if v == key:
                        mask.append(value)
        #debug
                else:
                    if v == key:
                        mask.append(value)
        #mask = mask[1:-1]
        #mask_str = mask.strip('"')
        #mask_r = mask.replace('"', ' ')
        mask_r =0
        for v in mask:
            mask_r |= v
        #journal.send("systemd-denotify: "+" DEBUG " + mask + " mask1 " + str(mask1) + " typeof mask " + str(type(mask)) +" typeof mask1 " + str(type(mask1)))
        wm = pyinotify.WatchManager()
        notifier = pyinotify.ThreadedNotifier(wm, EventHandler())
        notifier.start()
        # Start watching  paths
        for d in dictio['conf_files_directories']:
            wm.add_watch(d, int(mask_r, 10), rec=True)


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

##start classes
    ssc = ServiceStatusChecker()
    ssc.run()

    if isinstance(diction['conf_files_start'], bool) and diction['conf_files_start'] == True:
        FileNotifier()
    if isinstance(diction['conf_failed_services_start'], bool) and diction['conf_failed_services_start'] == True:
        jp = JournalParser()
        jp.daemon = True
        jp.start()
    if isinstance(diction['conf_logins_start'], bool) and diction['conf_logins_start'] == True:
        lm = LogindMonitor()
        lm.run()
