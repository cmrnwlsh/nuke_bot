import asyncio
import os
from os.path import join
import json

from discord import Intents, Client, app_commands, ButtonStyle, Embed
from discord.ui import button, View

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)
tree = app_commands.CommandTree(client)
path = os.path.dirname(__file__)
token = json.load(open(join(path, 'config.json')))['token']


@tree.command(description='Nuke this channel')
async def nuke(interaction):
    if ('eye of god' in [role.name.lower() for role in interaction.user.roles]
            or interaction.guild.owner_id == interaction.user.id):
        view = Confirm(interaction)
        view.interaction_check = async_partial(interaction_check, interaction)
        await interaction.response.send_message('Do you want to nuke this channel?', view=view)
        await view.wait()
    else:
        await interaction.response.send_message(
            'You do not have the correct role to use this command', ephemeral=True)


@client.event
async def on_ready():
    await tree.sync()


def async_partial(f, *args):
    async def f2(*args2):
        result = f(*args, *args2)
        if asyncio.iscoroutinefunction(f):
            result = await result
        return result

    return f2


async def interaction_check(view_interaction, interaction):
    return view_interaction.user.id == interaction.user.id


class Confirm(View):
    def __init__(self, original):
        super().__init__()
        self.original = original

    @button(label='Confirm', style=ButtonStyle.green)
    async def confirm(self, interaction, button):
        new_channel = await interaction.channel.clone()
        await interaction.channel.delete()
        embed = Embed(description='Boom')
        embed.set_image(url='https://media2.giphy.com/media/XUFPGrX5Zis6Y/giphy.gif?cid='
                            '6c09b952mf36fghxmzmzet11pi81n5wbwjwt4iqo42fs9aze&ep=v1_gifs_search&rid=giphy.gif&ct=g')
        await new_channel.send(embed=embed)
        self.stop()

    @button(label='Cancel', style=ButtonStyle.red)
    async def cancel(self, interaction, button):
        await self.original.delete_original_response()
        self.stop()


client.run(token)
