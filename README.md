# Ginger

Ginger is an open source penetration testing tool that ease the process of assessing the security of a given **[Pentaho](https://www.hitachivantara.com/en-us/products/data-management-analytics/pentaho.html)** installation.
It leverages known vulnerabilities, default credentials and documented features to allow extraction of sensitive data and server takeover.

Why making Ginger?
----

During a penetration testing for a client I accidentally stumbled upon the web interface of [Pentaho Business Intelligence server](https://sourceforge.net/projects/pentaho/files/Business%20Intelligence%20Server/) which although old is still widely used. A [Google search](https://www.google.com/search?q=pentaho+hacking) for any previous security work on this software was... well, disappointing: no report of a serious assessment of the platform.

Beginning an analysis on my own is quickly become clear that an enourmous attack surface was exposed, questionable security implementations in place and all of that combined with something miracously passed under the radar till now. As the attack surface expanded, it became clear that a single small script would not have cut it: ginger was born.

Usage
----

Ginger got just one mandatory parameter, the URL of the target Pentaho installation:

```console
user@host:~$ python gynger.py http://localhost:8080/pentaho
```

**Note: do not include a trailing slash (/)**

Doing that will start ginger in Anonymous mode, with limited funcionality. If valid credentials are known, those should be provided:

```console
user@host:~$ python gynger.py http://localhost:8080/pentaho -u admin -p password
```

When the scripted ended the preliminary connection phase, it will prompt and wait for commands. The complete list of available commands can be seen by typing `help`.

Command | Reference
--- | ---
api | try to list available API calls, even as Anonymous user
dbs | list all connected db credentials
files | list all available files in repository
usernames | list all valid usernames
userroles | list all valid usernames and valid roles
shell | upload a reverse shell
version | show Pentaho Version