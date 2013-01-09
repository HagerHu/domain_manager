#!/usr/bin/env python
# encoding: utf-8

"""
InetAddress.py

Created by Hager Hu on 2012-03-21.
Copyright (c) 2012 hagerhu.com. All rights reserved.
"""

import os
import time
import re,urllib2
from subprocess import Popen, PIPE
import yaml

DEFAULT = '127.0.0.1'

USER_HOME = os.path.expanduser('~')
INSTALL_FILE = USER_HOME + os.path.sep + '.name_service.yml'

#print "user_home:%s install_file:%s" %(USER_HOME, INSTALL_FILE)

def install_path():
	stream = file(INSTALL_FILE, 'r')
	config = yaml.load(stream)
	#print "config:%s %s" %(config, type(config))
	return config['service_dir']
#end method


CURRENT = install_path()

#print "INSTALL_PATH:%s" %(CURRENT)

#CURRENT = os.getcwd()
ADDRESS_HISTORY = CURRENT+ os.path.sep+ 'historyAddress.txt'
ADDRESS_CURRENT = CURRENT+ os.path.sep+ 'currentAddress.txt'

DOMAIN_UPDATE_FILE = CURRENT + os.path.sep + 'DomainUpdate.py'

#print "pwd:%s\nhistory:%s\ncurrent:%s" %(CURRENT, ADDRESS_HISTORY, ADDRESS_CURRENT)


def current():
   current = time.strftime("%Y-%m-%d %X", time.localtime())
   return current 


def currentDay():
   day = time.strftime("%w", time.localtime())
   return day


def currentDate():
   date = time.strftime("%Y%m%d", time.localtime())
   return date


def currentWeek():
   week = time.strftime("%U", time.localtime())
   return week


def inetaddress():
   address = re.search('\d+\.\d+\.\d+\.\d+',urllib2.urlopen("http://www.whereismyip.com").read()).group(0)
   return address


def lastInetAddress():
   if(os.path.exists(ADDRESS_HISTORY)):
       handle = open(ADDRESS_HISTORY,'r')
       linelist = handle.readlines()
       handle.close()
   
       if(len(linelist) > 0):
           lastline = linelist[len(linelist)-1]
           lastAddress = lastline.split(' ')[2]
           return lastAddress.replace('\n', '')
       #end if
   #end if
   
   return DEFAULT
#end method


#pragma mark -
#pragma mark main entry point

def main():
	#print "install_path:%s" %(install_path())
	
	last = lastInetAddress()
	address = inetaddress()
	compare = cmp(last, address)
	value = current()+" "+address+"\n"
	
	if (compare != 0):
		#print "address:%s" %(ADDRESS_HISTORY)
		handle = open(ADDRESS_HISTORY,'a')
		handle.write(value)
		handle.close()
		
		#print "address:%s" %(ADDRESS_CURRENT)
		handle = open(ADDRESS_CURRENT,'w')
		handle.write(value)
		handle.close()
		
		os.system("python "+ DOMAIN_UPDATE_FILE)
	#end if
#end method


if __name__ == '__main__':
	main()