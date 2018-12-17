# -*- coding: UTF-8 -*-
# Created by Nicholas Masso
# www.github.com/starmaid
# nicholas.masso.14@gmail.com
# created on 12/17/2018
# v1.0.0
#
# A more comprehensive search function for blogs on Tumblr.

# Import modules - requires pytumblr, so pip install that
import pytumblr
import time
import requests
import json
import random

# Authenticate via OAuth
# Fill in your values here
consumer_key = 'KmuUEeLtoJ4HL9i9KbbdhTafsIVadWOV2fVZGkrpIg9qAgcliB'
consumer_secret = 'CVQI6aEsNYU7f8hK7PjlN2382HKeyEJ8UZduHA19bwn3fgVDV8'
oauth_token = '8DyAKgFfKXROVUpWEAVoufIAKg5aew30TX0HJ7V5iIW71uaMTH'
oauth_secret = 'JDsTgHWMDbM1Ss2MQLstmYo4Odww0FlLOk6WZr6ifkAamNIHDX'

# Authenticate
client = pytumblr.TumblrRestClient(
  consumer_key,
  consumer_secret,
  oauth_token,
  oauth_secret
)

# Here are some basic variables for the search regulation
lim_num = 30    # This value gets overwritten
increment = 10  # This cant be more than 20 because of Tumblr's API restrictions

try:
    # User prompts
    blog_name = input( 'Please enter blog name: ' )     # TODO: input verification
    search_term = input( 'Please enter search terms (comma separated): ' ).split( ',' )
    lim_num = int( input( 'Enter how many posts to search: ' ))
    blog_url = 'http://' + blog_name + '.tumblr.com'

    print( 'Searching ' , blog_url , ' for: ' , search_term , ' (press ctrl+c to cancel)...' )

    # TODO: loading animation
    
    # A couple loop control variables
    rep_set = 0
    tally = 0
    results = []
    search_v = False
    while rep_set < lim_num:
        # Retrieve a list of posts
        posts_list = client.posts( blog_name , limit=increment , reblog_info=True , offset=rep_set )
        # Increase the offset for the next time we loop this
        rep_set = rep_set + increment
        # For each post in the list...
        for x in range( increment ):
            # Get info on the post itself
            ind_tags = posts_list['posts'][x]['tags']
            cont = posts_list['posts'][x]['summary']

            # Check for each term the user entered
            for y in range( len( search_term )):
                if str( search_term[y] ) in ind_tags:
                    search_v = True
                elif str( search_term[y] ) in cont:
                    search_v = True
                else:
                    # If the content isnt found in the user's tags, lets check OP
                    try:
                        op_post = client.posts(posts_list['posts'][x]['reblogged_root_name'],id=posts_list['posts'][x]['reblogged_root_id'])
                        op_tags = op_post['posts'][0]['tags']

                        if str(search_term[y]) in str(op_tags):
                            search_v = True
                        else:
                            # Sometimes, if the post is from like twitter or some other weird source
                            # There will be no post response, so there would just be an error
                            pass
                    except:
                        search_v = False
                if search_v == True:
                    results.append(str(search_term[y] + ': ' + posts_list['posts'][x]['short_url'] + '\n'))
                    tally = tally + 1
                    search_v = False

    # This is the file your results will be written to
    with open('search_results.txt','w') as out_file:
        out_file.writelines(results)

    # Print a results overview to the terminal
    print('searched ',lim_num,' posts, completed with ',tally,' results found')
    print('Writing results to \'search results.txt\'')
    time.sleep(5)

except KeyboardInterrupt:
    print('Cancelled')
    time.sleep(5)
