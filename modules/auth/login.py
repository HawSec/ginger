#!/usr/bin/python3
from modules import config

def login(username, password):
	login_headers = {"Referer": f"{config.pentaho_path}/Login"}
	login_data = {"j_username": username, "j_password": password, "locale": "en_US"}
	response = config.session.post(f"{config.pentaho_path}/j_spring_security_check", headers=login_headers, data=login_data, proxies=config.proxies)
	if '/Home' in response.url:
		return True
	else:
		return False