#!/usr/bin/python3
from modules import config
from modules.auth.login import login

def bruteforce_defaults():
	for user in config.webapp_usernames:
		print (user + ' / ' + config.webapp_usernames[user])
		if login(user, config.webapp_usernames[user]) == True:
			print('Logging in as '+ user + ' / ' + config.webapp_usernames[user])
			config.username = user
			return True
	return False