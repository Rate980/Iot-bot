import argparse
import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


class Bot(commands.Bot):
    async def setup_hook(self):
        for x in ["notify"]:
            await self.load_extension(f"iot_bot.cogs.{x}")
        await self.tree.sync()


bot = Bot(command_prefix="!", intents=discord.Intents.all())


@bot.hybrid_command()
async def showid(ctx: commands.Context):
    await ctx.send(
        str(ctx.author.id),
        ephemeral=True,
    )


def parse_log_level():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-l",
        "--log-level",
        default="INFO",
        type=str,
        choices=[
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
            "debug",
            "info",
            "warning",
            "error",
            "critical",
        ],
        required=False,
    )
    args = parser.parse_args()
    match args.log_level.upper():
        case "DEBUG" | "D":
            return logging.DEBUG

        case "WARNING" | "W":
            return logging.WARNING

        case "ERROR" | "E":
            return logging.ERROR

        case "CRITICAL" | "C":
            return logging.CRITICAL

        case _:
            return logging.INFO


load_dotenv()

bot.run(os.environ["TOKEN"], root_logger=True, log_level=parse_log_level())
