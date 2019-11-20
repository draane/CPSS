import git
import os
from scanners.github import get_repo_list

CLONE_PATH = "./temp/"


def main():
    ignore_list = []
    f = open("ignore_list.txt", "r")
    for line in f:
        ignore_list.append(line.strip())

    repo_list = [repo for repo in get_repo_list() if repo['full_name'] not in ignore_list]
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
