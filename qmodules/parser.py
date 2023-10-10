import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup


def steam_charts(ctx, embed: discord.Embed):

    page_response = requests.get(f'https://steamcharts.com/top/p.1').text

    page_soup = BeautifulSoup(page_response, 'lxml')
    blocks = page_soup.find('tbody').find_all('tr')

    for block in blocks:
        top = block.find_next('td').text.strip('.')
        name = block.find_next('td', class_='game-name').text.strip()
        current_players = block.find_next('td', class_="num").text.strip()

        embed.add_field(name=f"{top}. {name}", value=f"Онлайн: {current_players}", inline=False)

    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

    return embed
