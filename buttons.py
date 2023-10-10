import discord
from discord.ext import commands


class EmbedURLButton(discord.ui.View):
    def __init__(self, link):
        super().__init__()
        self.add_item(discord.ui.Button(label="Link",
                                        url=link
                                        ))
