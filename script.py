import asyncio
import datetime
from pyboy import PyBoy, WindowEvent
import os
import discord
from discord.ext import commands
from config import bot_token, channel_id
import pygetwindow as gw
from PIL import Image

intents = discord.Intents.default()
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Create PyBoy instance outside of on_ready
rom_path = 'rom.gb'
new_width=320
new_height=288
pyboy = PyBoy(rom_path, game_wrapper=True)
pyboy.set_emulation_speed(2)


class MyView(discord.ui.View):
    def __init__(self, pyboy_instance):
        super().__init__(timeout=None)
        self.pyboy = pyboy_instance
        self.message = None
        self.screenshot_countdown = 0 
        
    async def take_screenshot(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        previous_screenshots = [file for file in os.listdir() if 'screenshot-' in file and file.endswith('.png')]
        for screenshot in previous_screenshots:
            os.remove(screenshot)

        await asyncio.sleep(0.0)
        pil_image = self.pyboy.screen_image()

        file_path = f'screenshot-{timestamp}.png'
        pil_image.save(file_path)

    async def update_message(self, file_path=None):
        if file_path is None:
            screenshot_files = [file for file in os.listdir() if 'screenshot-' in file and file.endswith('.png')]
            if screenshot_files:
                file_path = screenshot_files[0]
            else:
                return

        if new_width and new_height:
            img = Image.open(file_path)
            img = img.resize((new_width, new_height))
            resized_file_path = os.path.basename(file_path)
            img.save(resized_file_path)

        filename = os.path.basename(file_path)
        file = discord.File(file_path, filename=filename)

        # Remove all previous attachments
        await self.message.edit(content="", view=self, embed=None, attachments=[file])


    @discord.ui.button(label="\u200b", style=discord.ButtonStyle.gray, disabled = True)
    async def click_here1(self, interaction: discord.Interaction, button: discord.Button):
        button.disabled = True
        await interaction.response.defer()

    @discord.ui.button(label="⇧", style=discord.ButtonStyle.primary)
    async def click_up(self, interaction: discord.Interaction, button):
        print('UP')
        self.pyboy.send_input(WindowEvent.PRESS_ARROW_UP)
        await asyncio.sleep(0.0)
        self.pyboy.send_input(WindowEvent.RELEASE_ARROW_UP)
        await advance_frames(self) 
        await interaction.response.defer()

    @discord.ui.button(label="\u200b", style=discord.ButtonStyle.gray, disabled = True)
    async def click_here2(self, interaction: discord.Interaction, button: discord.Button):
        button.disabled = True
        await interaction.response.defer()

    @discord.ui.button(label="\u200b", style=discord.ButtonStyle.gray, disabled = True)
    async def click_here3(self, interaction: discord.Interaction, button: discord.Button):
        button.disabled = True
        await interaction.response.defer()

    @discord.ui.button(label="\u200b", style=discord.ButtonStyle.gray, disabled = True)
    async def click_here4(self, interaction: discord.Interaction, button: discord.Button):
        button.disabled = True
        await interaction.response.defer()

    @discord.ui.button(label="⇦", style=discord.ButtonStyle.primary)
    async def click_left(self, interaction: discord.Interaction, button):
        print('LEFT')
        self.pyboy.send_input(WindowEvent.PRESS_ARROW_LEFT)
        await asyncio.sleep(0.0)
        self.pyboy.send_input(WindowEvent.RELEASE_ARROW_LEFT)
        await advance_frames(self) 
        await interaction.response.defer()

    @discord.ui.button(label="\u200b", style=discord.ButtonStyle.gray, disabled = True)
    async def click_here5(self, interaction: discord.Interaction, button: discord.Button):
        button.disabled = True
        await interaction.response.defer()

    @discord.ui.button(label="⇨", style=discord.ButtonStyle.primary)
    async def click_right(self, interaction: discord.Interaction, button):
        print('RIGHT')
        self.pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
        await asyncio.sleep(0.0)
        self.pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
        await advance_frames(self) 
        await interaction.response.defer()

    @discord.ui.button(label="\u200b", style=discord.ButtonStyle.gray, disabled = True)
    async def click_here6(self, interaction: discord.Interaction, button: discord.Button):
        button.disabled = True
        await interaction.response.defer()

    @discord.ui.button(label="A", style=discord.ButtonStyle.primary)
    async def click_a(self, interaction: discord.Interaction, button):
        print('A')
        self.pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
        await asyncio.sleep(0.0)
        self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
        await advance_frames(self) 
        await interaction.response.defer()

    @discord.ui.button(label="\u200b", style=discord.ButtonStyle.gray, disabled = True)
    async def click_here7(self, interaction: discord.Interaction, button: discord.Button):
        button.disabled = True
        await interaction.response.defer()

    @discord.ui.button(label="⇩", style=discord.ButtonStyle.primary)
    async def click_down(self, interaction: discord.Interaction, button):
        print('DOWN')
        self.pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)
        await asyncio.sleep(0.0)
        self.pyboy.send_input(WindowEvent.RELEASE_ARROW_DOWN)
        await advance_frames(self) 
        await interaction.response.defer()

    @discord.ui.button(label="\u200b", style=discord.ButtonStyle.gray, disabled = True)
    async def click_here8(self, interaction: discord.Interaction, button: discord.Button):
        button.disabled = True
        await interaction.response.defer()

    @discord.ui.button(label="B", style=discord.ButtonStyle.primary)
    async def click_b(self, interaction: discord.Interaction, button):
        print('B')
        self.pyboy.send_input(WindowEvent.PRESS_BUTTON_B)
        await asyncio.sleep(0.0)
        self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_B)
        await advance_frames(self) 
        await interaction.response.defer()

    @discord.ui.button(label="\u200b", style=discord.ButtonStyle.gray, disabled = True)
    async def click_here9(self, interaction: discord.Interaction, button: discord.Button):
        button.disabled = True
        await interaction.response.defer()

    @discord.ui.button(label="S", style=discord.ButtonStyle.primary)
    async def click_start(self, interaction: discord.Interaction, button):
        print('START')
        self.pyboy.send_input(WindowEvent.PRESS_BUTTON_START)
        await asyncio.sleep(0.0)
        self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_START)
        await advance_frames(self) 
        await interaction.response.defer()

    @discord.ui.button(label="\u200b", style=discord.ButtonStyle.gray, disabled = True)
    async def click_here10(self, interaction: discord.Interaction, button: discord.Button):
        button.disabled = True
        await interaction.response.defer()

    @discord.ui.button(label="Start", style=discord.ButtonStyle.primary)
    async def click_start(self, interaction: discord.Interaction, button):
        print('START')
        self.pyboy.send_input(WindowEvent.PRESS_BUTTON_START)
        await asyncio.sleep(0.0)
        self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_START)
        await advance_frames(self) 
        await interaction.response.defer()

    @discord.ui.button(label="\u200b", style=discord.ButtonStyle.gray, disabled = True)
    async def click_here11(self, interaction: discord.Interaction, button: discord.Button):
        button.disabled = True
        await interaction.response.defer()

    @discord.ui.button(label="\u200b", style=discord.ButtonStyle.gray, disabled = True)
    async def click_here12(self, interaction: discord.Interaction, button: discord.Button):
        button.disabled = True
        await interaction.response.defer()

    @discord.ui.button(label="\u200b", style=discord.ButtonStyle.gray, disabled = True)
    async def click_here13(self, interaction: discord.Interaction, button: discord.Button):
        button.disabled = True
        await interaction.response.defer()

    pil_image = pyboy.screen_image()
    pil_image.save('screenshot.png')

async def advance_frames(view):
   # await view.take_screenshot()
   # await asyncio.sleep(0.0)
   # await view.update_message() 
   # await asyncio.sleep(1)
    view.screenshot_countdown = 5

async def pyboy_emulation_loop(view):
    while True:
        pyboy.tick()
        await asyncio.sleep(0)

async def take_screenshot_task(view):
    while True:
        if view.screenshot_countdown > 0:
            await view.take_screenshot()
            await view.update_message()
            view.screenshot_countdown -= 1
        await asyncio.sleep(0.5)

@bot.event
async def on_ready():
    channel = bot.get_channel(channel_id)
    print(f'{bot.user} has connected to Discord!')

    view = MyView(pyboy)
    message = await channel.send(view=view)

    view.message = message
    await asyncio.sleep(2)
    await view.take_screenshot()
    await view.update_message()

    emulation_task = bot.loop.create_task(pyboy_emulation_loop(view))
    screenshot_task = bot.loop.create_task(take_screenshot_task(view))

    await asyncio.gather(emulation_task, screenshot_task)

@bot.command()
async def start_screenshots(ctx):
    view = ctx.bot.views[ctx.channel.id]
    view.screenshot_countdown = 10  # Set the countdown to 10 seconds
    await ctx.send("Screenshots will be taken for the next 10 seconds.")

@bot.command()
async def reset_screenshots(ctx):
    view = ctx.bot.views[ctx.channel.id]
    view.screenshot_countdown = 10  # Reset the countdown to 10 seconds
    await ctx.send("Screenshot countdown reset.")

bot.run(bot_token)