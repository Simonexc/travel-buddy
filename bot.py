import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from places_api import get_places, get_nearby_places

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PLACES_TYPES = [
    "restaurant",
    "hotel",
    "museum",
]

bot = commands.Bot(
    command_prefix='!',
    intents=discord.Intents(messages=True, reactions=True, message_content=True),
)


@bot.event
async def on_ready():
    print("Bot is ready")


@bot.command()
async def travel(ctx, destination):
    places = get_places(destination)
    if not places:
        await ctx.send(f"no places found for {destination}")
        return
    if len(places) > 1:
        places = places[:9]
        message = await ctx.send(
            "Choose the desired destination:\n" + "\n".join(f"{i + 1}️⃣ {place['name']}" for i, place in enumerate(places))
        )
        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'][:len(places)]

        # Add reactions to the message for user to choose
        for emoji in emojis:
            await message.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.author and str(
                reaction.emoji) in emojis and reaction.message.id == message.id

        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        place = places[emojis.index(reaction.emoji)]
    else:
        place = places[0]

    await ctx.send(f"Traveling to {place['name']}!")

    nearby_places = {place_type: get_nearby_places(place_type, place['latitude'], place['longitude']) for place_type in PLACES_TYPES}
    print(nearby_places)


bot.run(TOKEN)
