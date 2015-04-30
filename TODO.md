Give the users the possibility to disable if they want the login and the journal polling from the .conf

Write a proper setup.py from distutils that will only call our custom setup.py(that will be renamed to smt else). Thus we will ease the package management

OPTIONALLY write code that temporarily allows /etc/pam.d/usermod to auth against us in arch linux. We will revert changes back in setup.py
