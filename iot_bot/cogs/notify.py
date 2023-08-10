import datetime
import logging
import os

import discord
from discord.ext import commands

SERVER_ID = int(os.environ["SERVER_ID"])
CHANNEL_ID = int(os.environ["CHANNEL_ID"])
ROLE_ID = int(os.environ["ROLE_ID"])

_log = logging.getLogger(__name__)


class Notify(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        # print(member, before, after, sep="\n")
        _log.debug(f"member: {member}")
        _log.debug(f"before: {before}")
        _log.debug(f"after: {after}")
        if member.guild.id != SERVER_ID:
            _log.debug("member.guild.id != SERVER_ID")
            return

        if before.channel == after.channel:
            _log.debug("before.channel == after.channel")
            return

        if member.bot:
            _log.debug("member.bot")
            return

        if member.guild.afk_channel == after.channel:
            _log.debug("AFK")
            return

        if (channel := member.guild.get_channel(CHANNEL_ID)) is None:
            _log.debug("channel is None")
            return

        if not isinstance(channel, discord.abc.Messageable):
            _log.debug("channel is not instance of discord.abc.Messageable")
            return

        if before.channel is not None:
            _log.debug("退出")
            if before.channel is None:
                _log.debug("before.channel is None")
                return

            if len(before.channel.members) != 0:
                _log.debug(
                    f"len(before.channel.members):{len(before.channel.members)} >= 1"
                )
                return

            embed = discord.Embed(title="通話終了", color=discord.Color.red())
            embed.add_field(name="`チャンネル`", value=before.channel.mention)
            message = await channel.send(embed=embed)
            _log.debug(f"url: {message.jump_url}")

        if after.channel is not None:
            if len(after.channel.members) != 1:
                _log.debug(
                    f"len(after.channel.members):{len(after.channel.members)} < 1"
                )
                return

            embed = discord.Embed(title="通話開始", color=discord.Color.green())
            embed.add_field(name="`チャンネル`", value=after.channel.mention)
            embed.add_field(name="`ユーザー`", value=member.display_name)
            embed.add_field(
                name="`開始時間`",
                value=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            )
            message = f"<@&{ROLE_ID}>"
            message = await channel.send(message, embed=embed)
            _log.debug(f"url: {message.jump_url}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Notify(bot))


if __name__ == "__main__":
    import os
    from pathlib import Path

    import discord

    file = Path(__file__).resolve()
    prefix = file.parent

    token = os.environ["DIS_TEST_TOKEN"]

    intents = discord.Intents.all()

    class MyBot(commands.Bot):
        async def on_ready(self):
            print("ready")

        async def setup_hook(self):
            await self.load_extension(file.stem)
            await self.tree.sync()

    bot = MyBot("t!", intents=intents)
    bot.run(token, root_logger=True)
