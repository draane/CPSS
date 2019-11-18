import requests
import time


def get_repo_list(pages=10):
    if pages < 1 or pages > 10:
        pages = 10
    repo_list = []
    for page in range(pages, pages+1):
        url = "https://api.github.com/search/repositories?q=language:c&sort=stars&order=desc&per_page=100&page=" + str(page)
        r = requests.get(url)

        data = r.json()

        for repo in data['items']:
            repo_list.append(repo)
        time.sleep(2)

    return repo_list

