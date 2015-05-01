#!/usr/bin/python2
from __future__ import print_function
import os
import shutil
#from systemd import journal
import subprocess as sub
import argparse

class Installer():
    """
    Installer
    :desc : Class that installs either systemd-denotify.py v2 or v3
    """

    def __init__(self):
        """
        __init__
        :desc : Function constructor
        Instantiates the installer

        """


    def addXuser_to_group(self):
        """addXuser_to_group
        return void
        :desc : Function that adds the logedin user to systemd-journal group
        CREDITS->http://pymotw.com/2/subprocess/
        """
        login = os.getlogin()
        try:
            who = sub.Popen(['/usr/bin/w'], stdout=sub.PIPE, stderr=sub.PIPE)
            grep = sub.Popen(['/usr/bin/grep', ':0'], stdin=who.stdout, stdout=sub.PIPE)
            cut = sub.Popen(['/usr/bin/cut', '-d ', '-f1'], stdin=grep.stdout, stdout=sub.PIPE)
            sort = sub.Popen(['/usr/bin/sort'], stdin=cut.stdout, stdout=sub.PIPE)
            uniq = sub.Popen(['/usr/bin/uniq'], stdin=sort.stdout, stdout=sub.PIPE)
            who.stdout.close()
            grep.stdout.close()
            cut.stdout.close()
            sort.stdout.close()
            end_of_pipe = uniq.stdout
            for line in end_of_pipe:
                data = line.strip()
                stringify = str(data.decode("utf-8"))
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print("systemd-denotify: "+message)
        #this will autoraise  if exit status non zero
        if login == stringify:
            command = '/usr/sbin/usermod -a -G systemd-journal '+ stringify
            usermod = sub.check_call(command.split(), shell=False)
            if usermod:
                print("systemd-denotify:" +  "Your user was added to the systemd-journal group.You must relogin for the changes to take effect.")
                return True
            else:
                print("systemd-denotify: "+"Your user was not added to the systemd-journal group,but there is a possibility he is already a member of the group.")
                return False
        elif stringify != login:
            command = '/usr/sbin/usermod -a -G systemd-journal '+ stringify
            usermod = sub.check_call(command.split(), shell=False)
            if usermod:
                print("systemd-denotify: "+ "While your login user doesnt match the Xorg loggedin user,he was added to the systemd-journal group.You must relogin for the changes to take effect.")
                return True
            else:
                print("systemd-denotify: "+"Your Xorg loggedin user was not added to the systemd-journal group,but there is a possibility he is already a member of the group.")
                return False
        else:
            command = '/usr/sbin/usermod -a -G systemd-journal '+ login
            usermod = sub.check_call(command.split(), shell=False)
            if usermod:
                print("systemd-denotify: "+ "While we couldnt find the Xorg loggedin user,your loggedin user was added to the systemd-journal group.You must relogin for the changes to take effect.")
                return True
            else:
                print("systemd-denotify: "+ "Your loggedin user was not added to the systemd-journal group, but there is a possibility he is already a member of the group.")
                return False


    def install_v2(self):
        """install_v2
        :return void
        :desc: function that does the heavy job. Copies the v2 files to appropriate places.
         This func also chmod's the files so that the user that starts X is ab        le to execute the program.
        """
        path = os.path.dirname(os.path.abspath(__file__))
        src_c = path+"/systemd-denotify.py"
        src_d = path+"/systemd-denotify/conf/systemd-denotify.desktop"
        src_e = path+"/systemd-denotify/conf/systemd-denotify.conf"
        dst_c = "/usr/local/bin/systemd-denotify.py"
        dst_d = "/etc/xdg/autostart/systemd-denotify.desktop"
        dst_e = "/etc/systemd-denotify.conf"
        try:
            shutil.copy2(src_c, dst_c)
            shutil.copy2(src_d, dst_d)
            shutil.copy2(src_e, dst_e)
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print("systemd-denotify: "+message)
        try:
            os.chmod(dst_c, 0o755)
            os.chmod(dst_d, 0o644)
            os.chmod(dst_e, 0o644)
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print("systemd-denotify: "+message)

        print("systemd-denotify: "+ "successfully installed v2.")

    def install_v3(self):
        """install_v3
        :return void
        :param start:str(actually bool casted to str) specifying whether the DbusNotify Class should be instantiated
        :param minutes:str(actually int casted to str) for the time interval between notifications
        :param *services: str of services separated by a space
        :desc: function that does the heavy job. Copies the v3 files to appropriate places and writes the command line args that
        will be used to start or not the DbusNotify Class. This func also chmod's the files so that the user that starts X is ab        le to execute the program.
        """
        path = os.path.dirname(os.path.abspath(__file__))
        data = ""
        with open(path+"/systemd-denotify.desktop", "r+") as fin:
            data += fin.read()
            fin.seek(0)
            data_replace = data.replace("Exec=/usr/local/bin/systemd-denotify.py", "Exec=/usr/local/bin/systemd-denotify3.py")
            fin.write(data_replace)
        src_c = path+"/systemd-denotify3.py"
        src_d = path+"/systemd-denotify/conf/systemd-denotify.desktop"
        src_e = path+"/systemd-denotify/conf/systemd-denotify.conf"
        dst_c = "/usr/local/bin/systemd-denotify3.py"
        dst_d = "/etc/xdg/autostart/systemd-denotify.desktop"
        dst_e = "/etc/systemd-denotify.conf"
        try:
            shutil.copy2(src_c, dst_c)
            shutil.copy2(src_d, dst_d)
            shutil.copy2(src_e, dst_e)
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print("systemd-denotify: "+message)
        try:
            os.chmod(dst_c, 0o755)
            os.chmod(dst_d, 0o644)
            os.chmod(dst_e, 0o644)
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print("systemd-denotify: "+message)
        print("systemd-denotify: "+ "successfully installed v3.")

    def reset_desktop_file(self):
        path = os.path.dirname(os.path.abspath(__file__))
        data_replace = "[Desktop Entry]\nVersion=1.0\nName=system-denotify\nType=Application\nExec=/usr/local/bin/systemd-denotify.py"
        data = ""
        with open(path+"/systemd-denotify.desktop", "r+") as fin:
            data += fin.read()
            fin.seek(0)
            fin.write(data_replace)
            fin.truncate()

    def remove_old_version(self):
        files = ["/etc/systemd-desktop-notifications.conf", "/etc/xdg/autostart/systemd-notify.desktop", "/usr/local/bin/systemd-notify.py", "/usr/local/bin/systemd-notify3.py"]
        for f in files:
            if os.path.isfile(f):
                try:
                    os.remove(f)
                except OSError as e:  ## if failed, report it back to the user ##
                    print("systemd-denotify: " + "Error: %s - %s." % (e.filename,e.strerror))

    def uninstall(self):
        files = ["/etc/systemd-denotify.conf", "/etc/xdg/autostart/systemd-denotify.desktop", "/usr/local/bin/systemd-denotify.py", "/usr/local/bin/systemd-denotify3.py"]
        for f in files:
            if os.path.isfile(f):
                try:
                    os.remove(f)
                except OSError as e:  ## if failed, report it back to the user ##
                    print("systemd-denotify: " + "Error: %s - %s." % (e.filename,e.strerror))

