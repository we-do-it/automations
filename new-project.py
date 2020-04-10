import json
import os

from gitutils import GitHelper

# load github token
with open("config.json") as json_data_file:
    token = json.load(json_data_file)['access_token']

git = GitHelper(token)
# configuration
from utils import print_line

version = '0.1'
path = "/Users/creativelambda/git"

#
# # start of script
os.chdir(path)
print('Project creator ' + version)
print_line()

project_name = ''
name_exists = True
while name_exists:
    project_name = input('Project name:')
    name_exists = git.name_exists(project_name)
    if name_exists:
        print('Project name already exists')

private = ''
while private != 'y' and private != 'n':
    print('Private? (y/n)')
    private = input()
#
# # # create folder
# try:
#     os.mkdir(project_name)
#     print('Directory created')
# except FileExistsError:
#     print('Project with that name already exists')
#     sys.exit()
#
# # go inside created directory
# os.chdir(project_name)

# create git repository
private_param = True
if private == 'n':
    private_param = False

folder = path + '/' + project_name
git.create_repository(project_name, private_param, folder)



# push code to repo


