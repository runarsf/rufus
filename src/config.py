import os

token = os.environ['BOT_TOKEN']
osu_api_key = os.environ['OSU_API_KEY']
wolfram_api_key = os.environ['WOLFRAM_API_KEY']
lastfm_api_key = os.environ['LASTFM_API_KEY']
omdb_api_key = os.environ['OMDB_API_KEY']
prefixes = ['>', 'rufus ', 'r?', 'r ']
#docker_game = 'under development'
#docker_game = 'in a trashcan'
docker_game = 'under construction'
game = 'in his container'
description = f'prefixes: {str(prefixes).strip("[]")}'
srcDir = (os.path.dirname(os.path.realpath(__file__)))

owner_id = 177098893069254656
dev_id = [324943524132814849, 359319833680281601]
swears = ['frick', 'heck']

greetings = [
    'privet',
    'privyet',
    'chuchichäschtli',
    'grüezi',
    'hi',
    'hello',
    'greetings',
    'hey',
    'good to see you',
    'nice to see you',
    'you should subscribe to pewdiepie',
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
    'bazinga',
    'cześć'
]
