import os
import json

with open('secrets.json') as json_data_file:
    data = json.load(json_data_file)

prefixes = ['>', 'rufus ', 'r ']
devGame: str = 'under construction' # under development
dockerGame: str = 'in his container'
description: str = f'prefixes: {str(prefixes).strip("[]")}'
dockerStatus: bool = os.environ.get('DOCKER_MODE') == True
srcDir: str = (os.path.dirname(os.path.realpath(__file__)))

owner_id: int = 177098893069254656
dev_id = [324943524132814849, 359319833680281601] # 330837514246029312

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
