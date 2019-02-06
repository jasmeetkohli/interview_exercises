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

if __name__ == '__main__':

	###### Logging Setup #########
	logging.basicConfig(filename="log", 
	                    format='%(asctime)s %(message)s', 
	                    filemode='w')
	logger=logging.getLogger() 
	logger.setLevel(logging.INFO) 

	try:
		git_repo = sys.argv[1]
		pom_path = git_repo + "/pom.xml"
	
		#Get XML File 
		with open(pom_path, 'r') as xml_file:
		    pom_xml = xml_file.read()
	except IndexError:
		logger.error("Must provide git-repo path as an argument")	    
	except IOError as err:
		logger.error("IO error !")
		logger.error(err)
		quit(1)
	except Exception as err:
		logger.error(err)
		quit(1)

	try:
		######## Verify Syntax ######
		document = etree.parse(BytesIO(pom_xml))
	except etree.XMLSyntaxError as err:
	    logger.error(err.error_log)
	    quit(1)
	except Exception as err:
		logger.error(err)
		quit(1)
	
	root = document.getroot() # get root of XML
	version = root.find("version", root.nsmap) # get <version>
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
	version.text = text # modify version
	logger.info("New version: " + version.text) #Add ci_foo_bar_branch-SNAPHOST
	etree.ElementTree(root).write(pom_path, pretty_print=True) #save changes
