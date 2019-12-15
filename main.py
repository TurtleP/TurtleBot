#!/usr/bin/python3

import os

import discord
from discord.ext import commands

from data.utility import extensions, get_config_data, set_ext_status
import traceback

# Get our environment variables
BOT_PREFIX = get_config_data("prefix")
BOT_TOKEN = os.environ['BOT_TOKEN']

# Create a new Bot instance
bot = commands.Bot(BOT_PREFIX,
                   description=get_config_data("description"))

for item in extensions:
    try:
        bot.load_extension(f"data.cogs.{item}")
        set_ext_status(item, True)
    except commands.ExtensionFailed as e:
        set_ext_status(item, False)


@bot.event
async def on_command_error(ctx, error):
    if not isinstance(error, commands.CommandNotFound):
        return await ctx.send(error)

    if isinstance(error, commands.MissingPermissions):
        return await ctx.send("You don't have the right permissions to use this command!")

bot.run(BOT_TOKEN)
