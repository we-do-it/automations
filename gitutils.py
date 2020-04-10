import pygit2
from github import Github
from mdutils.mdutils import MdUtils
import os
import time

class GitHelper:
    repos = []
    current_repo = ''

    def __init__(self, token):
        self.token = token
        self.g = Github(token)
        self.set_repos()

    def name_exists(self, name):
        if name == '':
            return True
        match = False
        for repo in self.repos:
            if repo == name:
                match = True
        return match

    def set_repos(self):
        self.repos = []
        for repo in self.g.get_user().get_repos():
            self.repos.append(repo)

    def create_repository(self, project_name, private, folder):
        user = self.g.get_user()
        private_param = True
        if private == 'n':
            private_param = False
        self.current_repo = user.create_repo(project_name, private=private_param)
        print('Created a repository at ', self.current_repo.git_url)
        print('Cloning repository from ' + self.current_repo.git_url + ' into ' + folder)
        callbacks = pygit2.RemoteCallbacks(pygit2.UserPass(self.token, 'x-oauth-basic'))
        print(self.token)
        print(self.current_repo.git_url)
        url = self.create_correct_github_url(self.current_repo.git_url)
        repo = pygit2.clone_repository(url, folder, callbacks=callbacks)
        os.chdir(project_name)
        # create markdown file
        mdFile = MdUtils(file_name='readme', title=project_name)
        mdFile.create_md_file()
        repo.remotes.set_url('origin', url)
        index = repo.index
        index.add_all()
        index.write()
        author = pygit2.Signature('FV', 'fv@cl1.be')
        commiter = pygit2.Signature('FV', 'fv@cl1.be')
        tree = index.write_tree()
        oid = repo.create_commit('refs/heads/master', author, commiter, 'init project' + project_name, tree, [])
        remote = repo.remotes['origin']
        remote.push(['refs/heads/master'], callbacks=callbacks)

    def create_correct_github_url(self, repo):
        # created url
        # git://github.com/we-do-it/tester43.git
        # https://github.com/we-do-it/tester43.git
        new_prefixed_url = 'https://github.com/'
        wrong_prefixed_url = 'git://github.com/'
        repo_url = repo.replace(wrong_prefixed_url, new_prefixed_url)
        return repo_url