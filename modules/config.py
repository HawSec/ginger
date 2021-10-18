#!/usr/bin/python3

webapp_usernames = {'admin':'password', 'joe': 'password', 'suzy': 'password', 'tiffany':'password', 'pat': 'password' }
#proxies = {'http': 'http://127.0.0.1:8090'}
#proxies = {'https': 'http://127.0.0.1:8090'}
proxies = {}

# Default accounts for various components
default_accounts = {
	'HSQLDB':
		{'SA':'', 'HIBUSER': 'PASSWORD', 'hibuser': 'password', 'pentaho_user' : 'PASSWORD', 'PENTAHO_ADMIN' : 'PASSWORD', 'pentaho_admin' : 'password' },
	'MySQL':
		{'jcr_user' : 'password', 'pentaho_user' : 'password', 'hibuser' : 'password' },
	'Oracle':
		{'quartz': 'password', 'admin' : 'password', 'jcr_user' : 'password', 'hibuser' : 'password' },
	'PostgreSQL':
		{'jcr_user': 'password', 'pentaho_user': 'password', 'hibuser': 'password'  },
	'SQLServer':
		{'jcr_user': 'password', 'pentaho_user': 'password', 'hibuser': 'password'  },
	'LDAP':
		{'admin' : 'secret' }
}

is_anon = True

# Some default path to avoid indexing to lower noise
path_store = ['/public/plugin-samples', '/public/bi-developers']
