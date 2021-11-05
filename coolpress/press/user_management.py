from typing import Optional

import requests
from bs4 import BeautifulSoup
from libgravatar import Gravatar


def get_gravatar_link(email: str) -> Optional[str]:
    g = Gravatar(email)
    profile_url = g.get_profile()
    res = requests.get(profile_url)
    if res.status_code == 200:
        return g.get_image()
    return None


def extract_github_repositories(content) -> Optional[int]:
    soup = BeautifulSoup(content, 'html.parser')
    css_selector = 'div.UnderlineNav > nav > a:nth-child(2) > span'
    css_selector = 'a[href$="repositories"] span'
    repositories_info = soup.select_one(css_selector)
    return int(repositories_info.text)

def extract_github_followers(content) -> Optional[int]:
    soup = BeautifulSoup(content, 'html.parser')
    css_selector = '#js-pjax-container > div.container-xl.px-3.px-md-4.px-lg-5 > div > div.Layout-sidebar > div > div.js-profile-editable-replace > div.d-flex.flex-column > div.js-profile-editable-area.d-flex.flex-column.d-md-block > div.flex-order-1.flex-md-order-none.mt-2.mt-md-0 > div > a:nth-child(1) > span'
    followers_info = soup.select_one(css_selector)
    return int(followers_info.text)

def get_github_repositories(github_profile):
    url = f'https://github.com/{github_profile}'
    response = requests.get(url)
    gh_repositories = None
    if response.status_code == 200:
        gh_repositories = extract_github_repositories(response.content)
    return gh_repositories

def get_github_followers(github_profile):
    url = f'https://github.com/{github_profile}'
    response = requests.get(url)
    gh_followers = None
    if response.status_code == 200:
        gh_followers = extract_github_followers(response.content)
    return gh_followers
