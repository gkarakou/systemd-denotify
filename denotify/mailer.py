#!/usr/bin/python2
import threading
from systemd import journal
from threading import Thread
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
                    if len(dictionary['smtps_cert']) > 0 and len(dictionary['smtps_key']) > 0:
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
                    if len(dictionary['smtps_cert']) > 0 and len(dictionary['smtps_key']) > 0:
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
                        if len(dictionary['starttls_cert']) > 0 and len(dictionary['starttls_key']) > 0:
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

