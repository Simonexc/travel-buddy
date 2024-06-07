import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from gemmini_integration import generate_text
from places_api import get_places, get_nearby_places
import logging

from database import create_query_table, insert_query

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
logger = logging.getLogger('discord-bot')


create_query_table()


@bot.event
async def on_ready():
    logger.info("Bot is ready")


@bot.command()
async def travel(ctx, destination):
    places = await get_places(destination)

    def check(message, emojis):
        def _check(reaction, user):
            return user == ctx.author and str(
                reaction.emoji) in emojis and reaction.message.id == message.id

        return _check

    if not places:
        await ctx.send(f"no places found for {destination}")
        logger.info(f"No places found for {destination}")
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

        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check(message, emojis))
        place = places[emojis.index(reaction.emoji)]
    else:
        place = places[0]

        # Selecting adventure type
    adventure_types = ["Adventure", "Exploration", "Chill", "Family Time"]
    type_message = await ctx.send(
        "Select trip type:\n" + "\n".join(
            f"{i + 1}️⃣ {atype}" for i, atype in enumerate(adventure_types))
    )

    type_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣'][:len(adventure_types)]
    for emoji in type_emojis:
        await type_message.add_reaction(emoji)

    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check(type_message, type_emojis))
    adventure_type = adventure_types[type_emojis.index(reaction.emoji)]

    # Selecting duration
    duration_message = await ctx.send("Select the duration (2-9 days):")
    duration_emojis = ['2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
    for emoji in duration_emojis:
        await duration_message.add_reaction(emoji)

    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check(duration_message, duration_emojis))
    duration = duration_emojis.index(reaction.emoji) + 2

    insert_query(ctx.author.name, place['name'], adventure_type, duration)

    await ctx.send(f"Traveling to {place['name']}!")

    nearby_places = {place_type: await get_nearby_places(place_type, place['latitude'], place['longitude']) for place_type in PLACES_TYPES}
    #TO DO: Add further error handling
    
    try:
        gemmini_output = generate_text(place['name'], adventure_type, duration, nearby_places)
        for i in range(0, len(gemmini_output), 1800):
            await ctx.send(gemmini_output[i:i+1800])
    except discord.HTTPException as e:
        await ctx.send("Sorry something went wrong (HTTP bad request)")
        logger.error(f"An error occurred: {e}")

bot.run(TOKEN)
