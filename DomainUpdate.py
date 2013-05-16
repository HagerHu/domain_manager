#!/usr/bin/env python
# encoding: utf-8

"""
DomainUpdate.py

Created by Hager Hu on 2012-03-21.
Copyright (c) 2012 hagerhu.com. All rights reserved.
"""

import os
import httplib2, urllib
import json
import yaml

USER_HOME = os.path.expanduser('~')
INSTALL_FILE = USER_HOME + os.path.sep + '.name_service.yml'

print "user_home:%s install_file:%s" %(USER_HOME, INSTALL_FILE)


HEADERS = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31'}


def install_path():
	stream = file(INSTALL_FILE, 'r')
	config = yaml.load(stream)
	print "config:%s %s" %(config, type(config))
	return config['service_dir']
#end method


CURRENT = install_path()
ADDRESS_CURRENT_FILE = CURRENT+ os.path.sep+ 'currentAddress.txt'

print "ADDRESS_FILE:%s" %(ADDRESS_CURRENT_FILE)

CONFIG_FILE = CURRENT + os.path.sep + "config.yml"

BASE_URL = 'https://api.name.com/api/'

#pragma mark -
#pragma mark load configuration from YAML file

def load_config():
	stream = file(CONFIG_FILE, 'r')
	config = yaml.load(stream)
	#print "config:%s" %(config)
	domains = config['domains_update']
	#print "domains:%s" %(domains)
	
	return config
#end method


def account_user_name():
	conf = load_config()
	return conf['account']['user_name']
#end method


def account_api_token():
	conf = load_config()
	return conf['account']['api_token']
#end method


def need_update_domains():
	conf = load_config()
	return conf['domains_update']
#end method



#pragma mark -
#pragma mark Network Connection

def name_hello():
	h = httplib2.Http()
	url = BASE_URL + "hello"
	
	print "url:%s headers:%s" %(url, HEADERS)
	resp, content = h.request(url, "GET", headers = HEADERS)
	print "response:%s\n\ncontent:%s\n\n" %(resp, content)
	
	return content
#end method


def name_login():
	http = httplib2.Http()
   
	url = BASE_URL + 'login'
	
	user_name = account_user_name()
	api_token = account_api_token()
	#print "username:%s apiToken:%s" %(user_name, api_token)
	
	body = {'username':user_name, 'api_token':api_token}
	print "url:%s headers:%s" %(url, HEADERS)
	response, content = http.request(url, "POST", body=json.dumps(body), headers = HEADERS)
	print "response:%s\n\ncontent:%s\n\n" %(response, content)

	session = json.loads(content)

	return session['session_token']
#end method


def name_logout(session):
	http = httplib2.Http()
	url = BASE_URL + 'logout'
	
	#headers = {'Api-Session-Token':session}
	HEADERS['Api-Session-Token'] = session
	
	print "url:%s headers:%s" %(url, HEADERS)
	response, content = http.request(url, "GET", headers = HEADERS)
	print "response:%s\n\ncontent:%s\n\n" %(response, content)
	
	return content
#end method


#pragma mark -
#pragma Account Info

def name_account(session):
	http = httplib2.Http()

	url = BASE_URL + 'account/get'
	user_name = account_user_name()
	api_token = account_api_token()
	
	#headers = {'Api-Username':user_name, 'Api-Token':api_token}
	HEADERS['Api-Usernme'] = user_name;
	HEADERS['Api-Token'] = api_token;
	HEADERS['Api-Session-Token'] = session;
	
	print "url:%s header:%s" %(url, HEADERS)
	response, content = http.request(url, "GET", headers=HEADERS)

	print "response:%s\n\ncontent:%s\n\n" %(response, content)
	
	return content
#end method


#pragma mark -
#pragma mark Domain Info

def name_domain_list(session):
	http = httplib2.Http()
	
	url = BASE_URL + 'domain/list'
	
	#headers = {'Api-Session-Token':session}
	HEADERS['Api-Session-Token'] = session
	
	print "url:%s headers:%s" %(url, HEADERS)
	response, content = http.request(url, "GET", headers = HEADERS)
	
	print "response:%s\n\ncontent:%s\n\n" %(response, content)
	
	return content
#end method


def get_domain_name_list(content):
	responseJSON = json.loads(content)
	
	result = responseJSON['result']
	print "result:%s\n\n" %(result)
	
	nameList = []
	
	if(int(result['code'])== 100):
		#responseJSON = json.loads(content)
		domainList = responseJSON['domains']
		#print "allKeys[%d]:%s" %(len(allKeys), allKeys)
		return domainList.keys()
	#end if
	
	return nameList
#end method


#pragma mark -
#pragma DNS record update

def name_domain_dns_create(session, domain, hostname, r_type, content, ttl, priority):
	http = httplib2.Http()
	
	url = BASE_URL + 'dns/create'
	
	#headers = {'Api-Session-Token':session}
	body = {'hostname':hostname, 'type':r_type, 'content':content, 'ttl':ttl, 'priority':priority}
	
	print "url:%s header:%s" %(url, HEADERS)
	response, content = http.request(url+"/"+domain, "POST", headers=HEADERS, body=json.dumps(body))
	
	#response, content = http.request(url+domain, "GET", headers = headers)
	print "response:%s\n\ncontent:%s\n\n" %(response, content)
	
	return content
#end method


def name_domain_dns_create_default(session, domain, address):
	return name_domain_dns_create(session, domain, '', 'A', address, 300, 0)
#end method


def name_domain_dns_delete(session, domain, record_id):
	http = httplib2.Http()
	
	url = BASE_URL + 'dns/delete'
	#headers = {'Api-Session-Token':session}
	body = {'record_id':record_id}
	
	print "url:%s header:%s" %(url, HEADERS)
	response, content = http.request(url+"/"+domain, "POST", headers=HEADERS, body=json.dumps(body))
	print "response:%s\n\nconent:%s\n\n" %(response, content)
	
	return content
#end method


def name_domain_dns_list(session, domain):
	http = httplib2.Http()
	
	url = BASE_URL + 'dns/list'
	
	#headers = {'Api-Session-Token':session}
	
	print "url:%s header:%s" %(url, HEADERS)
	response, content = http.request(url+'/'+domain, "GET", headers = HEADERS)
	print "%s\n\n%s\n\n" %(response, content)
	
	return content
#end method


def get_update_record_list(content):
	responseJSON = json.loads(content)
	
	result = responseJSON['result']
	print "result:%s\n\n" %(result)
	
	updateList = []
	
	if(int(result['code'])== 100):
		#responseJSON = json.loads(content)
		dnsList = responseJSON['records']
		for i in range(len(dnsList)):
			dnsRecord = dnsList[i]
			recordType = dnsRecord['type']
			compare = cmp(recordType, 'A')
			if(compare == 0):
				#print "updateRecord:\n%s" %(dnsRecord)
				
				updateList.append(dnsRecord)
				
				#return dnsRecord['record_id']
				
				"""
				recordId = dnsRecord['record_id']
				print "need update record:%s" %(recordId)
				"""
				
				#name_domain_dns_delete(session, domain, recordId)
				#return dnsRecord['record_id']
			else:
				continue
			#end if
		#end for loop
	#end if
				
	return updateList
#end method


#pragma mark -
#pragma Update DNS record

def name_domain_dns_update(session, domain, address):
	response = name_domain_dns_list(session, domain)
	
	updateList = get_update_record_list(response)
	
	print "updateList:\n%s\n\n" %(updateList)
	
	for i in range(len(updateList)):
		dnsRecord = updateList[i]
		recordId = dnsRecord['record_id']
		
		print "recordId:%s" %(recordId)
		
		if(recordId):
			name_domain_dns_delete(session, domain, recordId)
	
		name_domain_dns_create_default(session, domain, address)
#end method


#pragma mark -
#pragma mark Public method

def get_current_address():
	if(os.path.exists(ADDRESS_CURRENT_FILE)):
		handle = open(ADDRESS_CURRENT_FILE,'r')
		linelist = handle.readlines()
		handle.close()
    	
		if(len(linelist) > 0):
			lastline = linelist[len(linelist)-1]
			lastAddress = lastline.split(' ')[2]
	      	return lastAddress.replace('\n', '')
		#end if
	#end if
	
	return None
#end method


def all_domains_dns_record_update(session, address):
	content = name_domain_list(session)
	domainList = get_domain_name_list(content)
	print "domainList[%d]:%s" %(len(domainList), domainList)
	
	for i in range(len(domainList)):
		name = domainList[i]
		print "name:%s\n" %(name)
		name_domain_dns_update(session, name, address)
	#end for loop
#end method


def update_domains_in_configuration(session, address):
	#load domains need to update from configuration file
	domains = need_update_domains()
	
	for i in range(len(domains)):
		name = domains[i]
		name_domain_dns_update(session, name, address)
	#end for loop
#end method



######################################
#########  Main Entrp Point  #########
######################################

def main():
	load_config()
	
	name_hello()
	
	address = get_current_address();
	
	if(address == None):
		print "current address unavailable"
		return
	#end if
	
	print "current address:%s\n\n" %(address)
	
	session = name_login();
	
	#session = 'bda0bfa685ba8c1967a29a390aa2ca4b32b9593c'
	
	#print "session:%s" %(session)
	
	
	name_account(session)
	 	
	update_domains_in_configuration(session, address)
	
	
	#all_domains_dns_record_update(session, address);
	
	#content = name_domain_list(session);
	
	#domainList = get_domain_name_list(content);
	
	#print "domainNameList:%s\n" %(domainList)

	#name_domain_dns_list(session);

	#name_domain_dns_delete(session, '225625973');

	#name_domain_dns_list(session, 'hagerhu.com');

	#name_domain_dns_create(session, 'hagerhu.com','', 'A', address, 300, 0);
	
	#name_domain_dns_update(session, 'hager.hu.com', address);

	name_logout(session);
	#name_account();
#end method


if __name__ == '__main__':
	main()

