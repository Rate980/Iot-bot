import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


class Bot(commands.Bot):
    async def setup_hook(self):
        await self.tree.sync()


bot = Bot(command_prefix="!", intents=discord.Intents.all())


@bot.hybrid_command()
async def showid(ctx: commands.Context):
    await ctx.send(
        str(ctx.author.id),
        ephemeral=True,
    )


load_dotenv()

bot.run(os.environ["TOKEN"])
