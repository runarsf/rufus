import os
import json
from typing import List, Set, Dict, Tuple, Optional

from dotenv import load_dotenv
load_dotenv()

#description: str = f'prefixes: {str(prefixes).strip("[]")}'

#owner_ids: int = [ 177098893069254656 ]
dev_ids: List = [ 324943524132814849, 359319833680281601 ]

prefixes: List[str] = [ 'r ', 'rufus ' ]

scoped_games = {
    'default': 'with algorithms',
    'docker': 'with containers'
}

# An array of swear words represented by arrays of unicode characters (int)
# Generate strings with the `arr` bot command
swears: List[List[int]] = [
  [99, 117, 109, 98, 117, 98, 98, 108, 101],
  [102, 117, 99, 107, 116, 114, 117, 109, 112, 101, 116],
  [107, 110, 111, 98, 104, 101, 97, 100],
  [99, 117, 109, 100, 117, 109, 112, 115, 116, 101, 114],
  [119, 97, 110, 107, 101, 114],
  [116, 119, 97, 116, 119, 97, 102, 102, 108, 101],
  [116, 104, 117, 110, 100, 101, 114, 99, 117, 110, 116],
  [100, 105, 99, 107, 104, 101, 97, 100],
  [110, 111, 110, 99, 101],
  [99, 117, 109, 119, 105, 112, 101],
  [112, 105, 115, 115, 119, 97, 114, 100],
  [102, 117, 99, 107, 110, 117, 103, 103, 101, 116],
  [99, 117, 110, 116],
  [97, 114, 115, 101],
  [102, 117, 99, 107, 102, 97, 99, 101],
  [98, 117, 109, 104, 111, 108, 101],
  [99, 117, 110, 116, 102, 108, 97, 112, 115],
  [99, 111, 99, 107],
  [102, 117, 99, 107],
  [102, 114, 105, 99, 107],
  [104, 101, 99, 107],
  [110, 117, 116, 115, 97, 99, 107],
  [112, 114, 105, 99, 107],
  [99, 114, 97, 112],
  [98, 105, 116, 99, 104],
  [119, 104, 111, 114, 101],
  [110, 105, 103, 103, 101, 114],
  [97, 115, 115],
  [115, 104, 105, 116],
  [115, 108, 117, 116],
  [112, 101, 114, 115, 111, 110, 32, 111, 102, 32, 99, 111, 108, 111, 114],
  [112, 101, 114, 115, 111, 110, 32, 111, 102, 32, 99, 111, 108, 111, 117, 114],
  [116, 45, 115, 101, 114, 105, 101, 115],
  [110, 105, 103, 119, 97, 114, 100],
  [116, 119, 97, 116],
  [99, 104, 114, 105, 115, 116, 32, 111, 110, 32, 97, 32, 98, 105, 107, 101],
  [99, 104, 114, 105, 115, 116, 32, 111, 110, 32,
    97, 32, 99, 114, 97, 99, 107, 101, 114],
  [108, 105, 98, 116, 97, 114, 100],
  [116, 115, 101, 114, 105, 101, 115],
  [116, 32, 115, 101, 114, 105, 101, 115],
  [115, 101, 114, 105, 101, 115, 32, 111, 102, 32, 116, 104, 101, 32, 116],
  [127470, 127475],
  [98, 97, 108, 108, 115, 97, 99, 107],
  [116, 119, 97, 116, 119, 97, 102, 102, 108],
  [105, 109, 98, 101, 99, 105, 108, 101],
  [112, 104, 112]
]
# Convert swear words from integers to characters
for index, swear in enumerate(swears):
  for idx, character in enumerate(swear):
    swears[index][idx] = chr(character)
  swears[index] = "".join(swears[index])

  sindex: int = len(swears)

# The reactions that will be added to messages containing swear words
rages: List[str] = ['🚩', '😡', '😠', '🇮🇳', '🚫', '⛔', '🙅', '🚯', '👿', '🤐', '😱', '😳', '😭', '😢']

greetings: List[str] = [
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
