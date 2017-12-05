import discord
import asyncio
import random
import pickle
import os
from data import token

client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('-------')
	
@client.event
async def on_message(message):
	if message.content.startswith('>ping'):
		await client.send_message(message.channel, 'pong')
	elif message.content.startswith('>flip'):
		flip = random.choice(['Heads', 'Tails'])
		await client.send_message(message.channel, flip)
	elif message.content.startswith('>addquote'):
		if not os.path.isfile('quotes.pk1'):
			quote_list = []
		else:
			with open('quotes.pk1', 'rb') as quotes:
				quote_list = pickle.load(quotes)
		quote_list.append(message.content[9:])
		with open('quotes.pk1', 'wb') as quotes:
			pickle.dump(quote_list, quotes)
	elif message.content.startswith('>quote'):
		with open('quotes.pk1', 'rb') as quotes:
			quote_list = pickle.load(quotes)
		await client.send_message(message.channel, random.choice(quote_list))
client.run(token)