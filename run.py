import os
import requests
import subprocess
import shutil
import json
from sh import git
from bitbucket.bitbucket import Bitbucket

'''
System level Requirements: sh, requests, bitbucket-api, django
To do: Add a requirements.txt document so that everything
'''

bb = Bitbucket("harbordev", "rabbit01")

edging = 100

script_path = os.path.dirname(os.path.abspath(__file__))
templates_path = "{0}/harborproject".format(script_path)
save_path = os.path.join(os.path.expanduser("~"), "Desktop")

project_name = raw_input("Project Name:")

print("*" * edging)

project_path = "{0}/{1}".format(save_path, project_name)
ios_path = "{0}/ios/".format(project_path)
cms_path = "{0}/cms".format(project_path)
design_path = "{0}/designs".format(project_path)
documents_path = "{0}/documents".format(project_path)
	
print("Starting: Creating project at %s" % project_path)
if os.path.isdir(project_path):
	exit("Error: Project couldn't be created because the directory exists!")
else:
	print("Status: creating structure")
	os.mkdir(project_path)	
	os.mkdir(ios_path)
	os.mkdir(cms_path)
	os.mkdir(design_path)	
	os.mkdir(documents_path)
	
	print("*" * edging)

print("Starting: Adding git repos to the ios directory")
os.chdir(ios_path)
subprocess.call(['git', 'init'])

print("Copying: iOS Template to ios directory")
ios_template_src = "{0}/ios_template/".format(templates_path)
ios_template_dest = "{0}/{1}".format(ios_path, project_name)
shutil.copytree(ios_template_src, ios_template_dest)

print('Renaming: Asterisk to Project')
baddies = {'Asterisk',}
for path, dirs, files in os.walk(ios_template_dest):
	
	for f in dirs:
		
		if [e in f for e in baddies if e in f]:
			
			file = f.split(".")
			shutil.move(f, "{0}.{1}".format(project_name, file[1]))
	
	for f in files:
		
		if [e in f for e in baddies if e in f]:
			
			file = f.split(".")
			shutil.move(f, "{0}.{1}".format(project_name, file[1]))

exit();

print("Starting: Adding git repos to the cms directory")
os.chdir(cms_path)
subprocess.call(['git', 'init'])
print('*'  * edging)

print("Starting: Adding venv to cms")
subprocess.call(['virtualenv', '--no-site-packages', 'venv'])
print('*'  * edging)

print("Starting: updating pip in venv")
#pip install --upgrade setuptools
subprocess.call(['./venv/bin/pip', 'install', '--upgrade', 'pip'])

print("Copying: Requirements.txt to cms")
requirements_src = "{0}/requirements.txt".format(templates_path)
requirements_dest ="{0}/requirements.txt".format(cms_path)
shutil.copy(requirements_src, requirements_dest)

print("Starting: Adding CMS requirements from Requirements")
subprocess.call(['./venv/bin/pip', 'install', '-r', 'requirements.txt'])
print("*" * edging)

print('Starting: Creating Django Project')
subprocess.call(['django-admin', 'startproject', project_name, '.'])
subprocess.call(['django-admin', 'startapp', 'mobile'])
print("*" * edging)

print('Copying: .gitignore to cms')
cms_gitignore_src = "{0}/python.gitignore".format(templates_path)
cms_gitignore_dest ="{0}/.gitignore".format(cms_path)
shutil.copy(cms_gitignore_src, cms_gitignore_dest)

print('Starting: Intial git add and commit')
subprocess.call(['git', 'add', '.'])
subprocess.call(['git', 'commit', '-m', 'Initial commit'])
subprocess.call(['git', 'status'])

print('Starting: creating a private repo on bitbucket')
cms_repo_name = "{0}-CMS".format(project_name)
success, result = bb.repository.create(cms_repo_name)

if success:
	print("Starting: pushing initial commit to content to bitbucket")
	subprocess.call(["git", "remote", "add", "origin", "https://harbordev@bitbucket.org/harbordev/{0}.git".format(cms_repo_name)])
	subprocess.call(["git", "push", "-u", "origin", "--all"])
else:
	print("Error: couldn't push initial repository")
	
print("PROJECT SETUP IS COMPLETED - PLEASE REVIEW FOR ISSUES AND FAILURES!")	
	
	