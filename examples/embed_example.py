"""
embed=discord.Embed(title=title, url=httpurl, description=descropt, color=0x0080c0)
embed.set_author(name=author_name, url=author_link,icon_url=author_icon)
embed.set_thumbnail(url=icon)
embed.add_field(name=field1_name, value=field1_value, inline=False)
embed.add_field(name=field2_name, value=field_2value, inline=True)
embed.set_footer(text=footer_text)

await self.bot.say(embed=embed)
"""
