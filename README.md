# Ginger

Ginger is an open source security assessment tool that helps in assessing the security of a given **[Pentaho BA](https://www.hitachivantara.com/en-us/products/data-management-analytics/pentaho.html)** application instance.

Please keep in mind that this project is still a work in progress, and not all features might be present or work as intended.

## Usage

Ginger has only one mandatory parameter, the URL of the target Pentaho installation:

```console
user@host:~$ python gynger.py http://localhost:8080/pentaho
```

**Note: do not include a trailing slash (/)**

Doing that will start Ginger in Anonymous mode, with limited funcionality. If valid credentials are known, those should be provided:

```console
user@host:~$ python gynger.py http://localhost:8080/pentaho -u admin -p password
```

When Ginger establishes a connection with Pentaho BA, it will prompt and wait for commands.
The complete list of available commands can be seen by typing `help`.

Command | Reference
--- | ---
api | try to list available API calls, even as Anonymous user
dbs | list all connected db credentials
files | list all available files in repository
usernames | list all valid usernames
userroles | list all valid usernames and valid roles
shell | upload a reverse shell
version | show Pentaho Version

# Warning!

Ginger comes with absolutely NO WARRANTY,
and shall not be used at any system where prior approval has not been granted.
Use at your own risk.
