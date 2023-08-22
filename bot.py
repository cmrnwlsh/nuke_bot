import os
from os.path import join
import json
from discord import Intents, Client, app_commands, ButtonStyle, Embed
from discord.ui import button, View

intents = Intents.default()
client = Client(intents=intents)
tree = app_commands.CommandTree(client)
path = os.path.dirname(__file__)
token = json.load(open(join(path, 'config.json')))['token']


@tree.command(description='Nuke this channel')
async def nuke(interaction):
    view = Confirm()
    view.interaction_check = lambda self, view_interaction: view_interaction.user.id == interaction.user.id
    await interaction.response.send_message('Do you want to nuke this channel?', view=view)
    await view.wait()


@client.event
async def on_ready():
    await tree.sync()


class Confirm(View):
    def __init__(self):
        super().__init__()

    @button(label='Confirm', style=ButtonStyle.green)
    async def confirm(self, interaction, button):
        new_channel = await interaction.channel.clone()
        await interaction.channel.delete()
        embed = Embed(description='Boom')
        embed.set_image(url='https://i.imgur.com/tCfGwg1.jpg')
        await new_channel.send(embed=embed)
        self.stop()

    @button(label='Cancel', style=ButtonStyle.red)
    async def cancel(self, interaction, button):
        interaction.delete_original_response()
        self.stop()


client.run(token)
