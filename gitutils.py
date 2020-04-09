from github import Github


class GitHelper:
    repos = []

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
        for repo in self.g.get_user().get_repos():
            self.repos.append(repo)

    def create_repository(self, project_name, private):
        user = self.g.get_user()
        private_param = True
        if private == 'n':
            private_param = False
        repo = user.create_repo(project_name, private=private_param)
        print(repo)

