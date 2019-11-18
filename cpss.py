import git
import os
import time
from scanners.github import get_repo_list

CLONE_PATH = "./temp/"


def main():
    repo_list = get_repo_list(1)
    for repo in repo_list:
        print("cloning:", repo['full_name'])
        clone_url = repo['clone_url']
        os.mkdir(CLONE_PATH)
        git.Repo.clone_from(url=clone_url, to_path=CLONE_PATH)
        print("Executing cppcheck")
        os.system("cppcheck " + CLONE_PATH + " --quiet --xml 2>reports/" + repo['full_name'].replace('/', '.') + ".xml")
        print("removing the folder")
        os.system("rm -rf " + CLONE_PATH)


if __name__ == '__main__':
    main()
