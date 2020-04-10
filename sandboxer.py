import pygit2
import json
from github import Github
folder = '/Users/creativelambda/git/tester42'
url = 'https://github.com/we-do-it/tester2.git'
with open("config.json") as json_data_file:
    token = json.load(json_data_file)['access_token']


g = Github(token)
users = g.get_users()
for u in users:
    print(u)
