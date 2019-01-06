import urllib.request, json
import configparser, sys

config = configparser.ConfigParser()
config.read('github.ini')

critical=[]
warning=[]

for section in config.sections():
	for key in config[section]:
		with urllib.request.urlopen("https://api.github.com/orgs/%s" % section) as url:
			data = json.loads(url.read().decode())
			public_repos_found = int(data["public_repos"])
			public_repos_expected = int(config[section]["public_repos_expected"])
			if public_repos_expected != public_repos_found:
				if public_repos_found - public_repos_expected >1:
					critical.append(section)
				if public_repos_found - public_repos_expected <1:
					warning.append(section) 

if critical != []:
	 print("CRITICAL - the number of public repositories is higher than expected, you should probably check nothing is public that should not be on for the follow org(s): %s" % ",".join(critical))
	 sys.exit(2)

if warning != []:
	 print("WARNING - the number of public repositories is lower than expected, you should probably check this alerts config for the follow org(s): %s" % ",".join(warning))
	 sys.exit(1)