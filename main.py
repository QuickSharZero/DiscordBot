import datetime

import discord
from discord.ext import commands

import buttons
import config
import database
from qmodules import parser

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(intents=intents,
                      command_prefix='h:'
                      )
client.remove_command('help')


@client.event
async def on_ready():
    await client.tree.sync()
    print("Haruka connected")


@client.event
async def on_guild_join(guild: discord.Guild):
    database.add_server(guild.id)
    await client.tree.sync(guild=discord.Object(id=guild.id))


@client.tree.command(name="embed_url", description="Send embed message")
async def embed_url(interaction: discord.Interaction, label: str, description: str, url: str):
    web = url.split('/')
    if not interaction.user.guild_permissions.administrator or not commands.has_role(database.check(interaction.guild.id)):
        embed = discord.Embed(
            title= "Недостаточно прав",
            color=discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed)
        return
    if description == "None" or description == "-":
        embed = discord.Embed(
            title=label,
            color=discord.Colour.dark_purple()
        )
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
        embed.set_footer(text=web[2])
        await interaction.response.send_message(embed=embed, view=buttons.EmbedURLButton(url), ephemeral=False)
        return
    else:
        embed = discord.Embed(
            title=label,
            description=description,
            color=discord.Colour.dark_purple()
        )
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
        embed.set_footer(text=web[2])
        await interaction.response.send_message(embed=embed, view=buttons.EmbedURLButton(url), ephemeral=False)


@client.tree.command(name="set_mod", description="Set moderation role")
async def set_mod(interaction: discord.Interaction, role: discord.Role):
    if not interaction.user.guild_permissions.administrator:
        embed = discord.Embed(
            title="Недостаточно прав",
            color=discord.Colour.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    database.set_moder(interaction.guild.id, role.id)
    embed = discord.Embed(
        title="Роль модератора успешно установленна.",
        color=discord.Colour.dark_purple()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@client.command()
async def help(ctx):
    await ctx.message.delete(delay=1)
    embed = discord.Embed(
        title="Помощь по командам",
        color=discord.Colour.dark_purple()
    )
    embed.add_field(name="top_charts",
                    value="Доступность: Всем \n``Использование: h:steam_charts`` \nО команде: Выводит embed со списком 25 игр steam по онлайну",
                    inline=False)
    embed.add_field(name="embed_url",
                    value="Доступность: Только админы и модерация\n``Использование: h:embed_url {url} {title} description= {description}`` \n О команде: Выводит embed с кнопкой \n Примечание: Переменные указывать без скобок ``{}``. Теперь не обязательно прописывать description=.",
                    inline=False)
    msg = await ctx.send(embed=embed)
    await msg.delete(delay=60)


@client.command()
@commands.has_guild_permissions(administrator=True)
async def add_server(ctx):
    await ctx.message.delete(delay=1)
    database.add_server(ctx.guild.id)
    embed = discord.Embed(
        title="Сервер успешно добавлен.",
        color=discord.Colour.dark_purple()
    )
    msg = await ctx.send(embed=embed)
    await msg.delete(delay=5)


@client.command()
@commands.cooldown(1, 120, commands.BucketType.user)
async def steam_charts(ctx):
    await ctx.message.delete(delay=1)

    embed = discord.Embed(
        title="Топ игр Steam",
        color=discord.Colour.dark_gold()
    )

    msg = await ctx.send(embed=parser.steam_charts(ctx=ctx, embed=embed))
    await msg.delete(delay=60)


@client.event
async def on_command_error(ctx, error):
    await ctx.message.delete(delay=1)
    if isinstance(error, commands.CommandOnCooldown):
        retry_after = str(datetime.timedelta(seconds=error.retry_after)).split('.')[0]
        msg = await ctx.send(f'**Вы сможете использовать команду через {retry_after}**')
        await msg.delete(delay=5)


@embed_url.error
async def embed_url_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        print(error)
        await ctx.message.delete(delay=1)
        embed = discord.Embed(
            title="Ошибка",
            description="Введена не рабочая ссылка.",
            color=discord.Colour.red(),
        )
        msg = await ctx.send(embed=embed)
        await msg.delete(delay=5)


if __name__ == '__main__':
    database.initialize()
    client.run(config.TOKEN)
