import json
import logging
import os

import requests

from .models import Check

url = 'https://api.github.com/graphql'
API_TOKEN = os.environ.get('API_TOKEN')
headers = {'Authorization': 'token {}'.format(API_TOKEN)}


def transform_prs(merged_prs):
    uniq_prs = {}
    for pr in merged_prs:
        proj_name = pr.get('repository').get('name')
        pr_info = (pr.get('url'), pr.get('comments').get('totalCount'))

        if proj_name in uniq_prs:
            uniq_prs[proj_name]['merged_prs'].append(pr_info)
            continue

        url = pr.get('repository').get('url')
        stars = pr.get('repository').get('stargazerCount')
        uniq_prs[proj_name] = {'name': proj_name, 'stars': stars, 'url': url,
                               'merged_prs': [pr_info], 'not_merged_prs': []}

    return uniq_prs


def add_not_merged_prs(prs, merged_prs):
    for pr in prs:
        proj_name = pr.get('repository').get('name')
        pr_info = (pr.get('url'), pr.get('comments').get('totalCount'))
        if proj_name in merged_prs:
            merged_prs[proj_name]['not_merged_prs'].append(pr_info)
            continue

    return merged_prs


def get_user_prs(merged_prs, username):
    jsona = {'query': '''{user(login: "%s") {pullRequests(first: 100, states: [OPEN, CLOSED]) {
                        nodes {url comments {totalCount}
                        repository {name url stargazerCount}}}}}''' % username}

    try:
        response = requests.post(url=url, json=jsona, headers=headers)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        logging.error('Ошибка соединения.')
    except requests.exceptions.HTTPError:
        logging.error(f'Ошибка HTTP, код: {response.status_code}')

    try:
        pr = response.json().get('data').get('user'
                                             ).get('pullRequests').get('nodes')
    except (json.JSONDecodeError, TypeError, AttributeError):
        logging.error('Невозможно декодировать JSON.')

    user_prs = add_not_merged_prs(pr, merged_prs)

    return user_prs


def get_merged_prs(username):
    jsona = {'query': '''{user(login: "%s") {pullRequests(first: 100, states: [MERGED]) {
                        nodes {url comments {totalCount}
                        repository {name url stargazerCount}}}}}''' % username}

    try:
        response = requests.post(url=url, json=jsona, headers=headers)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        logging.error('Ошибка соединения.')
    except requests.exceptions.HTTPError:
        logging.error(f'Ошибка HTTP, код: {response.status_code}')

    try:
        merged_prs = response.json().get('data').get('user').get('pullRequests').get('nodes')  # noqa
    except (json.JSONDecodeError, TypeError, AttributeError):
        logging.error('Невозможно декодировать JSON.')

    transformed_prs = transform_prs(merged_prs)

    return transformed_prs


def collect_user_info(username):
    ''' Collecting information using the Github API '''

    if Check.objects.filter(username=username).exists():
        return None

    merged_prs = get_merged_prs(username)
    user_prs = get_user_prs(merged_prs, username)

    for pr in user_prs.values():
        Check.objects.create(
            project_name=pr['name'],
            url=pr['url'],
            stars_number=pr['stars'],
            merged_prs=str(pr['merged_prs']),
            not_merged_prs=str(pr['not_merged_prs']),
            username=username
        )
