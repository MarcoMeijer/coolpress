import json
from typing import List

import requests
from django.contrib.auth.models import User
from django.core.validators import URLValidator

from press.models import Post, Category, CoolUser

validate = URLValidator()

def get_or_create_category(category_name) -> Category:
    slug_cat = category_name.lower()

    try:
        cat = Category.objects.get(slug=slug_cat)
    except Exception as _:
        cat = Category.objects.create(slug=slug_cat, label=f"{slug_cat} news")

    return cat

def get_author_user_name(author_name, source):
    username = 'anonymous'
    if author_name != None:
        if 'staff' in author_name.lower():
            username = 'staff'
        else:
            names = author_name.split()
            if len(names) == 1:
                username = author_name
            else:
                username = author_name[0] + author_name.split()[-1]
            username = username.lower()
    domain = source.lower() if source and source.endswith('.com') else 'coolpress.com'
    return f'{username}@{domain}'

def get_or_create_author(author_name, source):
    username = get_author_user_name(author_name, source)

    try:
        cu = CoolUser.objects.get(user__username=username)
    except CoolUser.DoesNotExist:
        first_name = author_name or 'anonymous'
        first_name = first_name.split()[0]
        user = User.objects.create(username=username, first_name=first_name)
        cu = CoolUser.objects.create(user=user)

    return cu

def insert_post_from_mediastack(single_post):
    title = single_post["title"]
    body = single_post["description"]
    image_link = single_post["image"]

    try:
        # check if post exists
        Post.objects.get(title=title, body=body, image_link=image_link)
        return None
    except Post.DoesNotExist:
        # post does not exist, create it
        cat = get_or_create_category(single_post["category"])
        cu = get_or_create_author(single_post["author"], single_post["source"])

        post = Post.objects.create(category=cat, author=cu, title=title, body=body, image_link=image_link)
        return post

def gather_and_create_news(categories, languages, limit) -> List[Post]:
    url = f'http://api.mediastack.com/v1/news'
    params = {
        'limit': limit,
        'languages': ','.join(languages),
        'categories': ','.join(categories),
        'access_key': '293e4cc0bfccd5aec1556f88a8767267'
    }

    response = requests.get(url, params=params)
    data = json.loads(response.content)["data"]

    result = []
    for post in data:
        new_post = insert_post_from_mediastack(post)
        if new_post != None:
            result.append(new_post)

    return result
