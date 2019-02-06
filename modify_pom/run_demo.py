'''
Please use the provided pom.xml and create a python script which customizes the project pom version 
to match this pattern `<version>ci_{git hub org name here}_{branch name here}-SNAPSHOT</version>`.

As an example, when this script runs on code that lives in the `Team_Foo` git hub organization on 
a branch named `Bar`, the resulting version would be `ci_Team_Foo_Bar-SNAPSHOT`.
 

## Python script requirements
 * It must validate the pom is syntactically correct
 * It must confirm the existing version is a snapshot prior to making any changes
 * The resulting pom version needs to match this format `ci_{git hub org name here}_{branch name here}-SNAPSHOT`
 * Unit tests are an added bonus
 * Execution within a docker container is an extra bonus
 
Please provide details on how to execute your solution, as well as any presumptions/issues/etc that you 
feel is appropriate for the reviewer to be aware of.
'''

from lxml import etree
from io import BytesIO
from pygit2 import Repository
import os.path
from os import path
import logging
import sys 

def check_snapshot(snapshot_path):
	return path.exists(snapshot_path)

def get_snapshot_path(root, current_version, git_repo):
	app_dir = root.find("artifactId", root.nsmap)
	if app_dir is None:
		app_name = ""
	else:
		app_name = app_dir.text
		
	snapshot_path = git_repo + "/target/" + app_name + "-" + current_version + ".jar"
	return snapshot_path

def change_version(version, text):
	version.text = text

def save_changes(root):
	etree.ElementTree(root).write(pom_path, pretty_print=True) #save changes

if __name__ == '__main__':

	git_repo = sys.argv[1]
	pom_path = git_repo + "/pom.xml"

	###### Logging Setup #########
	logging.basicConfig(filename="log", 
	                    format='%(asctime)s %(message)s', 
	                    filemode='w')
	logger=logging.getLogger() 
	logger.setLevel(logging.INFO) 



	######## Get XML File ######
	if not path.exists(pom_path):
		print pom_path
		quit(2)

	with open(pom_path, 'r') as xml_file:
	    myxml = xml_file.read()

	######## Verify Syntax ######
	try:
		document = etree.parse(BytesIO(myxml))
	except etree.XMLSyntaxError as err:
	    logger.error(err.error_log)
	    quit(1)
	except Exception as err:
		logger.error(err)
		quit(1)

	# get root of XML
	root = document.getroot()

	# get <version>
	version = root.find("version", root.nsmap)

	snapshot_path = get_snapshot_path(root, version.text, git_repo)

	# check if SNAPHSHOT exists
	if not check_snapshot(snapshot_path):
		logger.error("SNAPSHOT DOES NOT EXIST, CHECKED PATH: " + snapshot_path)
		quit(1)

	######## Get Git Details ######
	repo = Repository(git_repo)
	org_name = repo.remotes["origin"].url.split("/")[-2]
	branch_name = repo.head.shorthand


	logger.info("Current version: " + version.text)
	text = 'ci_' + org_name + "_" + branch_name + "-SNAPSHOT"
	change_version(version, text)
	logger.info("New version: " + version.text) #Add ci_foo_bar_branch-SNAPHOST
	save_changes(root, pom_path)
