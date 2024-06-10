# import discord
# from . import embed_builder

# async def help_command(interaction):
#     embed = discord.Embed(
#         title="Help command",
#         description="__Commands__ \n**help** : Display this message.\n**lovecalc @1 @2** : Calculate the love between two people (with accuracy fr fr)\n**play <music>** : Play a music in the General Voice Channel.\n> __Music names (case sensitive) :__\n> ``standing`` | Elton John - I'm still Standing\n> ``erika`` | German Soldier Song\n> ``teufelslied`` | German March Song\n> ``festin`` | Ratatouille OST\n> ``china`` | Red Sun In The Sky\n> ``redstrongest`` | The Red Army Is The Strongest\n> ``katyusha`` | Katyusha\n**disconnect** : Disconnects the bot from VC.\nYou can also use <@1186799421636231208> + message to chat with me !\nNot much else for now <a:RotatingSkull:1145453604086485075>",
#         color=0x00ff00
#     )
#     embed = embed_builder.embed_default_builder(interaction, embed)
#     await interaction.response.send_message(embed=embed)

import discord
from discord.ext import commands
from . import embed_builder

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="help",
        description="Help for the entirety of the available bot commands."
    )
    async def help_command(self, ctx):  # Pass `self` as the first argument
        embed = discord.Embed(
            title="Help command",
            description="__Commands__ \n**help** : Display this message.\n**lovecalc @1 @2** : Calculate the love between two people (with accuracy fr fr)\n**play <music>** : Play a music in the General Voice Channel.\n> __Music names (case sensitive) :__\n> ``standing`` | Elton John - I'm still Standing\n> ``erika`` | German Soldier Song\n> ``teufelslied`` | German March Song\n> ``festin`` | Ratatouille OST\n> ``china`` | Red Sun In The Sky\n> ``redstrongest`` | The Red Army Is The Strongest\n> ``katyusha`` | Katyusha\n**disconnect** : Disconnects the bot from VC.\nYou can also use <@1186799421636231208> + message to chat with me !\nNot much else for now <a:RotatingSkull:1145453604086485075>",
            color=0x00ff00
        )
        embed = embed_builder.embed_default_builder(ctx, embed)
        await ctx.response.send_message(embed=embed)
        pass

def setup(bot):
    bot.add_cog(HelpCog(bot))
