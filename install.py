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

    def install_v2(self, start, minutes, *services):
        path = os.path.dirname(os.path.abspath(__file__))
        data = ""
        for service in services:
            ser = ""
            for s in service:
                ser += s 
            with open(path+"/systemd-notify.desktop", "r+") as fin:
                data += fin.read()
                fin.seek(0)
                data_replace = data.replace("Exec=/usr/local/bin/systemd-notify.py", "Exec=/usr/local/bin/systemd-notify.py" + " " + start +" " + str(minutes) + " "+ str(ser))
                fin.write(data_replace)
                fin.truncate()

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

    def install_v3(self, start, minutes, *services):
        path = os.path.dirname(os.path.abspath(__file__))
        data = ""
        for service in services:
            ser = ""
            for s in service:
                ser += s + " "
            with open(path+"/systemd-notify.desktop", "r+") as fin:
                data += fin.read()
                fin.seek(0)
                data_replace = data.replace("Exec=/usr/local/bin/systemd-notify3.py", "Exec=/usr/local/bin/systemd-notify3.py" + " " + start +" " + str(minutes) + " "+ str(ser))
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
input_from_user_bool= input("Would you like to receive notifications for the status of some services? Y/n: ")
if input_from_user_bool:
    if type(input_from_user_bool) == str and input_from_user_bool == "Y" or input_from_user_bool == "y":
        start_dbus = True
    elif type(input_from_user_bool) == str and input_from_user_bool == "N" or input_from_user_bool == "n":
        start_dbus = False
    else:
        print("You must type either Y or N for Yes or No: ")
        #break 
#else:
#    continue
input_from_user_list = input("Which services would you like to receive notifications for?\nBy default we have iptables, rc-local, polkit, autovt@tty2\nType Y if you accept these or type the names of the services that you want to be notified on separated by a space: ")
services_list = ""
if input_from_user_list:
    if type(input_from_user_list) == str and input_from_user_list == "Y" or input_from_user_list == "y" :
        services_list="iptables.service" "rc-local.service" "polkit.service" "autovt@tty2.service"
    elif type(input_from_user_list) == str and  "," in input_from_user_list:
           services_list=str(input_from_user_list) 
            #services += service.split(","))
    else:
        print("Either type Y or type the services you want separated by a space")
 #       continue
#continue
input_from_user_int = input("What should be the interval between the notifications?\nThe default is 30 minutes\nType Y if you accept this time interval or type the moments that you want: ") 
moments = "" 
if input_from_user_int:
    if type(input_from_user_int) == str and input_from_user_int == "Y" or input_from_user_int == "y":
        moments += str(30)
    elif type(input_from_user_int) == str and input_from_user_int != "Y" or input_from_user_int != "y":
        moments += str(input_from_user_int)
    else:
        print("Either type Y if you accept the default time interval of 30 mins between notifications or type the interval that you want: ")
#        continue
#continue
if len(list(sys.argv)) == 1:
    print("Error\nYou must enter one argument: either v2 or v3.\nExiting...") 
    sys.exit(1)
if sys.argv[1] == "v2":
    installer.is_archlinux()
    installer.addXuser_to_group()
    installer.install_v2(str(start_dbus), moments, services_list)
elif sys.argv[1] == "v3":
    installer.get_uid()
   # installer.setuid_root(0)
    installer.addXuser_to_group()
    installer.install_v3(str(start_dbus), moments, services_list)
else:
    print("There can be only one argument: either v2 or v3")
    sys.exit(1)
