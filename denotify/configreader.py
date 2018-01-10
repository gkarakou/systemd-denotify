#!/usr/bin/python2
import ConfigParser
import sys

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
        dictionary['conf_failed_services_espeak'] = conf.getboolean("FailedServices", "espeak")
        #parse patterns section
        dictionary['conf_pattern_matcher_start'] = conf.getboolean("JournalPatternMatcher", "start")
        dictionary['conf_pattern_patts'] = conf.get("JournalPatternMatcher", "patterns")
        dictionary['conf_pattern_patterns'] = dictionary['conf_pattern_patts'].split(",")
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
        dictionary['email_on_user_logins'] = conf.getboolean("EMAIL_NOTIFICATIONS", "email_on_user_logins")
        dictionary['email_on_failed_services'] = conf.getboolean("EMAIL_NOTIFICATIONS", "email_on_failed_services")
        dictionary['email_on_file_alteration'] = conf.getboolean("EMAIL_NOTIFICATIONS", "email_on_file_alteration")
        dictionary['email_on_services_statuses'] = conf.getboolean("EMAIL_NOTIFICATIONS", "email_on_services_statuses")

        dictionary['email_subject'] = conf.get("EMAIL", "subject")
        dictionary['email_to'] = conf.get("EMAIL", "mail_to")
        dictionary['email_from'] = conf.get("EMAIL", "mail_from")


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

