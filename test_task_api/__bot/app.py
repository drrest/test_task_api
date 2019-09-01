# -*- coding: utf-8 -*-
import datetime
import random
import time

from rest_framework.utils import json

from func.api_connector import APIClient
from func.config_parser import get_setting
from func.generators import Randomizer

config_file = "config/config.ini"

# reading configs from ini file
number_of_users = int(get_setting(config_file, "users", "number_of_users"))
min_post_per_user = int(get_setting(config_file, "posts", "min_post_per_user"))
max_post_per_user = int(get_setting(config_file, "posts", "max_post_per_user"))
max_likes_per_user = int(get_setting(config_file, "likes", "max_likes_per_user"))
jwt_prefix = get_setting(config_file, "system", "jwt_prefix")
api_url = get_setting(config_file, "system", "api_url")
api_port = get_setting(config_file, "system", "api_port")
debug = True if get_setting(config_file, "system", "debug") == "1" else False

# Init external classes
randomize = Randomizer()
api = APIClient(api_url, api_port)

stats = {'users_actions': {},
         'system_actions': [],
         'stats': {'choice': {'like': 0,
                              'unlike': 0}
                   }}
total_created_posts = 0
created_users = []
posts = []

# Create new users ans save they credentials into array `created_users`
for each_new_user in range(1, number_of_users):
    generated_user = randomize.generate_record()
    answer = api.postrequest_json("user/signup/", generated_user)

    stats['system_actions'].append({'action': 'create_user',
                                    'email': generated_user['email'],
                                    'datetime': datetime.datetime.now().isoformat()})

    created_users.append({'email': generated_user['email'],
                          'password': generated_user['password']})
    if debug:
        print("create user -> [%s] with password '%s' " % (
            generated_user['email'], generated_user['password']))

stats['users_credentials'] = created_users

# For each this user
for each_user in created_users:
    # LOGIN into system via each created user
    token = api.login(each_user['email'], each_user['password'])

    # Form out full token string for header
    full_token = jwt_prefix + "  " + token
    stats['system_actions'].append({'action': 'logging_user',
                                    'email': each_user['email'],
                                    'datetime': datetime.datetime.now().isoformat()})

    stats['users_actions'][each_user['email']] = [{'action': 'login',
                                                   'token': token,
                                                   'full_token': full_token,
                                                   'datetime': datetime.datetime.now().isoformat()}]

    # solve for count of posts user will be created and create they
    count_of_creating_posts = random.randrange(5, max_post_per_user)
    total_created_posts += count_of_creating_posts

    for each_post_for_user in range(1, count_of_creating_posts):
        title = randomize.generate_title()
        text = randomize.generate_text()
        create_post = api.creating_post(full_token, title, text)
        stats['users_actions'][each_user['email']].append({'action': 'create_post',
                                                           'title': title,
                                                           'text': text,
                                                           'datetime': datetime.datetime.now().isoformat()})
        if debug:
            print("%s -> create post -> [%s] with title '%s' " % (
                each_user['email'], create_post['response']['answer'], title))

    # get all actual posts as dict
    start_time = time.time()

    all_posts = api.auth_getrequest_json("post/list/", full_token, {}).text
    get_all_posts = json.loads(all_posts)['response']['answer']
    stats['system_actions'].append({'action': 'get_all_posts',
                                    'count': len(get_all_posts),
                                    'execution_time': "%s sec." % (time.time() - start_time),
                                    'datetime': datetime.datetime.now().isoformat()})

    # shuffle it
    random.shuffle(get_all_posts)
    # Get list of unique posts and random count for like or unlike it.
    # Note:Other way is to use random.choice([array], k=[element count])
    list_to_like_unlike = get_all_posts[:random.randrange(4, len(get_all_posts) if max_likes_per_user >= len(
        get_all_posts) else max_likes_per_user)]
    stats['system_actions'].append({'action': 'user_will_like_or_unlike',
                                    'email': each_user['email'],
                                    'posts': [lu['pk'] for lu in list_to_like_unlike],
                                    'datetime': datetime.datetime.now().isoformat()})

    # For each selected post
    for each_like_unlike_post in list_to_like_unlike:
        # randomly select LIKE or UNLIKE (Unlike will remove Like record from this instance of selected POST
        # and vice versa)
        like_or_unlike = random.choice([True, False])  # also can be - bool(random.getrandbits(1))  :)
        text_value_of_like_or_unlike = 'like' if like_or_unlike == True else 'unlike'
        stats['stats']['choice'][text_value_of_like_or_unlike] += 1
        # like or unlike request - (who knows) :)
        response_object = api.like_or_unlike(full_token, each_like_unlike_post['pk'], like_or_unlike)['response']
        stats['users_actions'][each_user['email']].append({'action': 'user_like_or_unlike',
                                                           'choice': text_value_of_like_or_unlike,
                                                           'post': each_like_unlike_post['pk'],
                                                           'datetime': datetime.datetime.now().isoformat()})

        if debug:
            print("%s -> %s post -> [%s] and now this post has %s likes and %s unlikes" % (
                each_user['email'],
                "like" if like_or_unlike == 1 else "unlike",
                each_like_unlike_post['meta']['title'],
                response_object['likes'],
                response_object['unlikes'])
                  )

stats['stats']['users_list'] = len(created_users)
stats['stats']['created_posts'] = total_created_posts

output_file = get_setting(config_file, "system", "output_file")
if output_file:
    with open(output_file,"a+") as stdout:
        stdout.write(json.dumps(stats))
else:
    print(stats)
