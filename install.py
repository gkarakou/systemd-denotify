#!/usr/bin/python3
from __future__ import print_function
import os
import shutil
from systemd import journal
import sys
import subprocess as sub

class Installer():

    def __init__(self):
        pass

    def get_uid(self):
        uid = os.getuid()
  #      print("uid= "+ str(uid))
        return uid
   
  #  def setuid_root(self,uid_root):
  #      self.uid_root = uid_root
  #      try:
  #          setuid_toor = os.setuid(uid_root)
  #          if setuid_toor:
  #              print("getting uid in True setuid_root func: "+ str(self.get_uid())) 
  #              return True
  #          else:
  #              print("getting uid in False setuid_root func: "+ str(self.get_uid())) 
  #              return False
  #      except Exception  as ex:
  #          template = "An exception of type {0} occured. Arguments:\n{1!r}"
  #          message = template.format(type(ex).__name__, ex.args)
  #          journal.send("systemd-notify: "+message)

    def is_archlinux(self):
        if  os.path.isfile("/etc/pacman.conf"):
            path = os.path.dirname(os.path.abspath(__file__))
            data = ""
            with open(path+"/systemd-notify.py", "r+") as fin:
                data += fin.read()
                fin.seek(0)
                data_replace = data.replace("python", "python2")
                fin.write(data_replace)
                fin.truncate()
                print("os was arch")

        else:
            print("os wasnt arch")

    def addXuser_to_group(self):
        #CREDITS->http://pymotw.com/2/subprocess/
   #     print("getting uid in addXuser func before setresuid: "+ str(self.get_uid())) 
   #     os.setresuid(0,0,0)
   #     print("getting uid in addXuser func after setresuid: "+ str(self.get_uid())) 

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
            journal.send("systemd-notify: "+message)
        #this will autoraise  if exit status non zero 
        if login == stringify:
            #print("login user matches X user")
            command = '/usr/sbin/usermod -a -G systemd-journal '+ stringify
            usermod = sub.check_call(command.split(), shell=False)
            if usermod:
                print("Your user was added to the systemd-journal group.\nYou must relogin for the changes to take effect")
                return True
            else:
                print("Your user was not added to the systemd-journal group " )
                return False

    def install_v2(self):
        path = os.path.dirname(os.path.abspath(__file__))
        src_c = path+"/systemd-notify.py"
        src_d = path+"/systemd-notify.desktop"
        dst_c = "/usr/local/bin/systemd-notify.py"
        dst_d = "/etc/xdg/autostart/systemd-notify.desktop"
        try:
            shutil.copy2(src_c, dst_c)
            shutil.copy2(src_d, dst_d)
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            journal.send("systemd-notify: "+message)
        try:
            os.chmod(dst_c, 0o755)
            os.chmod(dst_d, 0o644)
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            journal.send("systemd-notify: "+message)

        print("successfully installed systemd-notify v2")

    def install_v3(self):
        path = os.path.dirname(os.path.abspath(__file__))
        data = ""
        with open(path+"/systemd-notify.desktop", "r+") as fin:
            data += fin.read()
            fin.seek(0)
            data_replace = data.replace("notify", "notify3")
            fin.write(data_replace)
            fin.truncate()
        src_c = path+"/systemd-notify3.py"
        src_d = path+"/systemd-notify.desktop"
        dst_c = "/usr/local/bin/systemd-notify3.py"
        dst_d = "/etc/xdg/autostart/systemd-notify.desktop"

        try:
            shutil.copy2(src_c, dst_c)
            shutil.copy2(src_d, dst_d)
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            journal.send("systemd-notify: "+message)
        try:
            os.chmod(dst_c, 0o755)
            os.chmod(dst_d, 0o644)
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            journal.send("systemd-notify: "+message)
        print("successfully installed systemd-notify v3")

    #def __del__(self):

     #   del self.install_v2
     #   del self.install_v3


installer = Installer()
if len(list(sys.argv)) == 1:
    print("Error\nYou must enter one argument: either python2 or python3.\nExiting...") 
    sys.exit(1)
if sys.argv[1] == "python2":
    installer.is_archlinux()
    installer.addXuser_to_group()
    installer.install_v2()
elif sys.argv[1] == "python3":
    installer.get_uid()
   # installer.setuid_root(0)
    installer.addXuser_to_group()
    installer.install_v3()
else:
    print("There can be only one argument: either python2 or python3")
    sys.exit(1)
