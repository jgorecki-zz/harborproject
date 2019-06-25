import os
import sh
import shutil
import subprocess
from pbxproj import XcodeProject

# setup paths
main_path = os.path.join(os.path.expanduser("~"), "Projects")

print ('This was setup in conjunction with HarborProject!')
print ('--' * 10)

print 'Starting with: {0}'.format(main_path)

project_name = 'OneStudent' #raw_input("The project name (leave blank if it doesn't exist) ... ")
project_path = 'OneStudent/ios' #raw_input("The project path (not including ~/Projects/) ... ")
full_project_path = "{0}/{1}".format(main_path, project_path)
full_project_path_with_name = "{0}/{1}/{2}/".format(
    main_path, project_path, project_name)

print ('--' * 10)
print ('Full Project Path is: {0}'.format(full_project_path))
print ('Full Project Path With Project Name: {0}'.format(full_project_path_with_name))

are_those_correct = raw_input('Are those correct? Y/n: ')

if are_those_correct == 'Y':

    # copy assets into the project at the root, not the full project.  
    # Warning ... this may be different based on project layout!
    fastlane_directory = '{0}/HarborProject/assets/fastlane/'.format(main_path)

    shutil.copytree(fastlane_directory, full_project_path_with_name + '/fastlane/')
    
    subprocess.call(['fastlane', 'init'], shell=True, cwd = full_project_path_with_name)
    subprocess.call(['mkdir', 'builds'], shell=True, cwd=full_project_path)

    print '!!! YOU NEED TO CONTINUE CONFIG IN THE FASTLANE FOLDER AND CHECK THE BATCH SCRIPTS !!!'
