""" rufus.py config """

import os

token = os.environ['BOT_TOKEN']
osu_api_key = os.environ['OSU_API_KEY']
wolfram_api_key = os.environ['WOLFRAM_API_KEY']
lastfm_api_key = os.environ['LASTFM_API_KEY']
omdb_api_key = os.environ['OMDB_API_KEY']
prefix = '>'
docker_game = 'in a trashcan'
#docker_game = 'under development'
game = 'in his container'
description = 'Usage: {}help [command]'.format(prefix)

owner_id = '177098893069254656'
dev_id = ['324943524132814849', '359319833680281601']
swears = ['frick', 'heck']
mention = ['rufus', 'runar']

greetings = [
    'hi',
    'hello',
    'greetings',
    'hey',
    'good to see you',
    'nice to see you',
    'howdy',
    '\'ello',
    'ahoy',
    'hiya',
    'I\'m batman',
    'yo',
    'bonjour',
    'hei',
    'hej',
    'hola',
    'hallo',
    'guten tag',
    'ciao',
    'olá',
    'namaste',
    'salaam',
    'zdras-tvuy-te',
    'ohayo',
    'konnichiwa',
    'konbanwa',
    'jambo',
    'habari',
    'halo',
    'goedendag',
    'vanakkam',
    'nyob zoo',
    'salut',
    'cześć'
]
