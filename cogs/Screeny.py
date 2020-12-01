
from discord.ext import commands


def setup(bot):
    bot.add_cog(Screeny(bot))


class Screeny(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['screenshare', 'screen_share', 'screen-share'], case_insensitive=True)
    async def share(self, ctx):
        if ctx.subcommand_passed is None:
            voice = ctx.author.voice
            if voice:
                guild = ctx.guild
                link = self.generate_link(guild.id, voice.channel.id)
                message = f"Click this link to screen share in {guild}'s channel - {voice.channel}\n{link}"
            else:
                message = "You must be connected to a voice channel!"
            await ctx.author.send(message)
        await ctx.message.delete()

    @share.command()
    async def all(self, ctx):
        guild = ctx.guild
        message = ""
        for vc in guild.voice_channels:
            if vc.permissions_for(ctx.author).connect:
                message += f"{vc.name}: {self.generate_link(guild.id, vc.id)}\n"
        if message:
            header = f"Here are all of {guild}'s channels that you can use screen share:\n"
        else:
            header = f"There are no channels in {guild} that you are permitted to screen share."
        await ctx.author.send(header + message)

    @share.command(hidden=True)
    async def dev(self, ctx, *, channel):
        guild = ctx.guild
        header = ""
        message = ""
        for vc in guild.voice_channels:
            if vc.name.lower() == channel.lower():
                header = f"Click this link to screen share in {guild.name}'s channel - {vc.name}\n\n"
                message = self.generate_link(guild.id, vc.id)

        if not message:
            header = f"Could not find \"{channel}\" in {guild.name}'s voice channels"
        await ctx.author.send(header + message)

    @dev.error
    async def share_error(self, ctx, error):
        if type(error) is commands.MissingRequiredArgument:
            message = f"```\nUsage: {ctx.prefix}{ctx.command} <voice_channel>\n```"
        else:
            message = error
        await ctx.author.send(message)

    @staticmethod
    def generate_link(guild, channel):
        return f'https://discordapp.com/channels/{guild}/{channel}'

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(('You do not have permission to use this feature.\n'
                            'Contact your server administrator.'))
