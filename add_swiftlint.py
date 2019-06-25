# This project bootstraps a swift project to add a Swiftlint run phase, attaches a fastlane file, and installs cocoapods with the minimum

import os
import sh
import shutil
import subprocess
from pbxproj import XcodeProject

# setup paths
main_path = os.path.join(os.path.expanduser("~"), "Projects")

print ('This was setup in conjunction with HarborProject!')
print ('--' * 10)

project_name = raw_input("The project name (leave blank if it doesn't exist) ... ")
project_path = raw_input("The project path (not including ~/Projects/) ... ")
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
    swiftlint_file = '{0}/HarborProject/assets/swiftlint/swiftlint.sh'.format(main_path)
    swiftlint_yaml = '{0}/HarborProject/assets/swiftlint/.swiftlint.yml'.format(main_path)

    shutil.copy(swiftlint_file, full_project_path)
    shutil.copy(swiftlint_yaml, full_project_path)

    # Tell the project that this happening...
    pbx = "{0}.xcodeproj/project.pbxproj".format(full_project_path_with_name)
    project = XcodeProject.load(pbx)
    #backup_file = project.backup # lets just back that right up.
    project.add_run_script('bash ${PROJECT_DIR}/swiftlint.sh')

    project.save()

    print ('CHECK THE YAML FOR CONFIG AND TO SET THE INCLUDED DIRECTORIES!')