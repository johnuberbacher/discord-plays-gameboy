import asyncio
import datetime
from pyboy import PyBoy
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
new_width = 320
new_height = 288
pyboy = PyBoy(rom_path)
pyboy.set_emulation_speed(0)

class MyView(discord.ui.View):
    def __init__(self, pyboy_instance):
        super().__init__(timeout=None)
        self.pyboy = pyboy_instance
        self.message = None
        self.screenshot_countdown = 0
        self.last_activity_time = datetime.datetime.now()  # Track last activity time

    async def take_screenshot(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        previous_screenshots = [file for file in os.listdir() if 'screenshot-' in file and file.endswith('.png')]
        for screenshot in previous_screenshots:
            os.remove(screenshot)

        pil_image = self.pyboy.screen.image
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

    @discord.ui.button(label="⇧", style=discord.ButtonStyle.primary)
    async def click_up(self, interaction: discord.Interaction, button):
        print('UP')
        self.pyboy.button('up')
        await self.reset_screenshot_timer()
        await interaction.response.defer()

    @discord.ui.button(label="⇦", style=discord.ButtonStyle.primary)
    async def click_left(self, interaction: discord.Interaction, button):
        print('LEFT')
        self.pyboy.button('left')
        await self.reset_screenshot_timer()
        await interaction.response.defer()

    @discord.ui.button(label="⇨", style=discord.ButtonStyle.primary)
    async def click_right(self, interaction: discord.Interaction, button):
        print('RIGHT')
        self.pyboy.button('right')
        await self.reset_screenshot_timer()
        await interaction.response.defer()

    @discord.ui.button(label="⇩", style=discord.ButtonStyle.primary)
    async def click_down(self, interaction: discord.Interaction, button):
        print('DOWN')
        self.pyboy.button('down')
        await self.reset_screenshot_timer()
        await interaction.response.defer()

    @discord.ui.button(label="A", style=discord.ButtonStyle.primary)
    async def click_a(self, interaction: discord.Interaction, button):
        print('A')
        self.pyboy.button('a')
        await self.reset_screenshot_timer()
        await interaction.response.defer()

    @discord.ui.button(label="B", style=discord.ButtonStyle.primary)
    async def click_b(self, interaction: discord.Interaction, button):
        print('B')
        self.pyboy.button('b')
        await self.reset_screenshot_timer()
        await interaction.response.defer()

    @discord.ui.button(label="START", style=discord.ButtonStyle.primary)
    async def click_start(self, interaction: discord.Interaction, button):
        print('START')
        self.pyboy.button('start')
        await self.reset_screenshot_timer()
        await interaction.response.defer()

    async def reset_screenshot_timer(self):
        """Resets the screenshot timer on user input with a 0.25-second delay."""
        self.last_activity_time = datetime.datetime.now()
        if self.screenshot_countdown == 0:
            # Start the delay after input
            self.screenshot_countdown = 1  # Ensure it starts the screenshot delay

    async def monitor_inactivity(self):
        """Checks for inactivity and stops screenshots after 10 seconds."""
        while True:
            current_time = datetime.datetime.now()
            if (current_time - self.last_activity_time).total_seconds() >= 10:
                # Stop taking screenshots if no activity for 10 seconds
                self.screenshot_countdown = 0
            await asyncio.sleep(1)

async def pyboy_emulation_loop(view):
    while True:
        pyboy.tick()
        await asyncio.sleep(0)

async def take_screenshot_task(view):
    while True:
        if view.screenshot_countdown > 0:
            # Wait for 0.25 seconds after user input before taking a screenshot
            await asyncio.sleep(0.25)
            await view.take_screenshot()
            await view.update_message()
            view.screenshot_countdown = 0  # Reset countdown after taking screenshot
        await asyncio.sleep(0.5)

@bot.event
async def on_ready():
    channel = bot.get_channel(channel_id)
    print(f'{bot.user} has connected to Discord!')

    view = MyView(pyboy)
    message = await channel.send(view=view)

    view.message = message
    await asyncio.sleep(1)
    await view.take_screenshot()
    await view.update_message()

    # Start background tasks
    emulation_task = bot.loop.create_task(pyboy_emulation_loop(view))
    screenshot_task = bot.loop.create_task(take_screenshot_task(view))
    inactivity_monitor_task = bot.loop.create_task(view.monitor_inactivity())

    await asyncio.gather(emulation_task, screenshot_task, inactivity_monitor_task)

bot.run(bot_token)
