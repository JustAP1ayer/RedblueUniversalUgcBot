
import discord
from discord.ext import commands
from discord import app_commands
import requests
import datetime
import iso8601
import random
import re
import json
import traceback
import os

with open("settings.json", "r") as config_file:
    config = json.load(config_file)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config["command_prefix"], intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print('Guilds:')
    total_members = 0
    for guild in bot.guilds:
        print(guild.name)
        total_members += len(guild.members)
    print(f'Total members: {total_members}')
    print(f'Total guilds: {len(bot.guilds)}')
    
    synced = await bot.tree.sync()
    print(f"{len(synced)} Slash commands synced")

def calculate_percentages(value, total):
    if total != 0:
        given_percentage = (value / total) * 100
        remaining_percentage = 100 - given_percentage
        return given_percentage, remaining_percentage
def uwu_converter(message):
    uwu_message = (
        re.sub(r'(r|l)', 'w', message, flags=re.IGNORECASE)
        .replace('n([aeiou])', 'ny$1')
        .replace('N([aeiou])', 'Ny$1')
        .replace('N', 'Ny')
        .replace('n', 'ny')
        .replace(r'([.!?])\s', r'\1~')
        .replace(r'([.!?])\n', r'\1~\n')
    )

    uwu_emojis = [":3", ";3", ":3", ";3", ":3", ";3", "OwO", "UwU", "OvO", "ÒwÓ", "0v0", "ÕwÕ", "0w0", "~v~", "~w~"]
    random_emoji = random.choice(uwu_emojis)

    uwu_message += f'~ {random_emoji}'
    return uwu_message

assettypes = {
    1: "Image",
    2: "T-Shirt",
    3: "Audio",
    4: "Mesh",
    5: "Lua",
    6: "HTML",
    7: "Text",
    8: "Hat",
    9: "Place",
    10: "Model",
    11: "Shirt",
    12: "Pants",
    13: "Decal",
    # 14: "Unknown",  # * "VideoClip", "VideoOverlay"
    # 15: "Unknown",  # * "Article", "Widget"
    16: "Avatar",
    17: "Head",
    18: "Face",
    19: "Gear",
    # 20: "Unknown",  # * "Subscription", "PluginEmulator"
    21: "Badge",
    22: "Group Emblem",
    # 23: "Unknown",  # * "Bundle"
    24: "Animation",
    25: "Arms",
    26: "Legs",
    27: "Torso",
    28: "Right Arm",
    29: "Left Arm",
    30: "Left Leg",
    31: "Right Leg",
    32: "Package",
    33: "YouTube Video",
    34: "GamePass",
    35: "App",
    # 36: "Unknown",  # * "Game"
    37: "Code",
    38: "Plugin",
    39: "Solid Model",
    40: "Mesh Part",
    41: "Hair Accessory",
    42: "Face Accessory",
    43: "Neck Accessory",
    44: "Shoulder Accessory",
    45: "Front Accessory",
    46: "Back Accessory",
    47: "Waist Accessory",
    48: "Climb Animation",
    49: "Death Animation",
    50: "Fall Animation",
    51: "Idle Animation",
    52: "Jump Animation",
    53: "Run Animation",
    54: "Swim Animation",
    55: "Walk Animation",
    56: "Pose Animation",
    57: "Ear Accessory",
    58: "Eye Accessory",
    59: "Localization Table Manifest",
    60: "Localization Table Translation",
    61: "Emote Animation",
    62: "Video",
    63: "Texture Pack",
    64: "T-Shirt Accessory",
    65: "Shirt Accessory",
    66: "Pants Accessory",
    67: "Jacket Accessory",
    68: "Sweater Accessory",
    69: "Shorts Accessory",
    70: "Left Shoe Accessory",
    71: "Right Shoe Accessory",
    72: "Dress Skirt Accessory",
    73: "Font Family",
    74: "Font Face",
    75: "Mesh Hidden Surface Removal",
    76: "Eyebrow Accessory",
    77: "Eyelash Accessory",
    78: "Mood Animation",
    79: "Dynamic Head",
    80: "Code Snippet",
}

session = requests.session()
session.cookies['.ROBLOSECURITY'] = config["cookie"] 

@bot.hybrid_command()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@commands.cooldown(1, 14, commands.BucketType.user)
async def info(ctx, *, item_id1: str):
    print(f"{ctx.message.author} used the command: Info with {item_id1}")
    try:
        not_item = False
        item_id1 = item_id1.replace("fxroblox", "roblox")
        if "catalog/" in item_id1:
            item_id = item_id1.split("/catalog/")[1].split("/")[0]
        elif "item/" in item_id1:
            item_id = item_id1.split("/item/")[1].split("/")[0]
        elif "games/" in item_id1:
            item_id = item_id1.split("/games/")[1].split("/")[0]
            not_item = True
        else:
            item_id = item_id1

        if not item_id:
            await ctx.reply("⚠️ Please add an item link or item ID", mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False))
            return

        details_url = f"https://economy.roblox.com/v2/assets/{item_id}/details"
        details_response = session.get(details_url)

        if details_response.status_code == 200:
            details_data = details_response.json()

            name = details_data.get("Name")
            creator = details_data.get("Creator", {}).get("Name")
            creatortype = details_data.get("Creator", {}).get("CreatorType")
            price_in_robux = details_data.get("PriceInRobux")
            descriptionitem = details_data.get("Description")
            
            creation = details_data.get("Created")
            dt_objectcreation = iso8601.parse_date(creation)
            creationdiscord_timestampTR = f"<t:{int(dt_objectcreation.timestamp())}:R>"
            creationdiscord_timestampT = f"<t:{int(dt_objectcreation.timestamp())}>"
            update = details_data.get("Updated")
            dt_objectupdate = iso8601.parse_date(update)
            updatediscord_timestampTR = f"<t:{int(dt_objectupdate.timestamp())}:R>"
            updatediscord_timestampT = f"<t:{int(dt_objectupdate.timestamp())}>"
            
            if details_data.get("CollectiblesItemDetails", {}):
                total_quantity = details_data.get("CollectiblesItemDetails", {}).get("TotalQuantity", 0)
            remaining = details_data.get("Remaining")
            game_links = []
            game_names = []
            universe_ids = ""
            if details_data.get("SaleLocation", {}) and details_data.get("SaleLocation", {}).get("UniverseIds", []):
                sale_location = details_data.get("SaleLocation", {})
                universe_ids = sale_location.get("UniverseIds", [])
                for game_id in universe_ids:
                    gameuniverse_url = f"https://games.roblox.com/v1/games?universeIds={game_id}"
                    gameuniverse_response = requests.get(gameuniverse_url)
                    if gameuniverse_response.status_code == 200:
                        game_data = gameuniverse_response.json()
                        real_game_id = game_data['data'][0]['rootPlaceId']
                        real_game_name = game_data['data'][0]['name']
                        game_names.append(real_game_name)
                        game_idlink = f"{real_game_id}"
                        game_links.append(game_idlink)

            if details_data.get('CollectiblesItemDetails', {}):
                if details_data.get('CollectiblesItemDetails', {}).get('CollectibleQuantityLimitPerUser', 0) is not None:
                    quantity_limit = details_data.get('CollectiblesItemDetails', {}).get('CollectibleQuantityLimitPerUser', 0)
                else:
                    quantity_limit = 'None'
            else:
                quantity_limit = None

            description = f"# [{name}](https://www.roblox.com/catalog/{item_id}/)\n**👤 Creator:** {creator}"
            if creatortype is not None:
                description += f"\n``ᴸ``👥 **Creator Type:** {creatortype}\n"
            if details_data.get("IsForSale") is not None:
                description += "\n💰 **On Sale**: " + str(details_data.get("IsForSale"))
            if assettypes.get(details_data.get('AssetTypeId')):
                description += f"\n🔖 **Accessory Type:** {str(assettypes[details_data.get('AssetTypeId')])}"

            description += f"\n\n📝 **Description:**\n ```{descriptionitem} ```"

            if quantity_limit is not None:
                description += f"\n🔢 **Quantity Limit:** {quantity_limit} Per User"

            thumbnail_url = f"https://thumbnails.roblox.com/v1/assets?assetIds={item_id}&returnPolicy=PlaceHolder&size=150x150&format=Png"
            thumbnail_response = session.get(thumbnail_url)
            if thumbnail_response.status_code == 200:
                thumbnail_data = thumbnail_response.json()
                image_url = thumbnail_data["data"][0]["imageUrl"]
                if thumbnail_data["data"][0]["state"] is not None:
                    description += f"\n🔄 **Asset State:** {thumbnail_data['data'][0]['state']}"
            else:
                image_url = ""

            embed = discord.Embed(description=description)
            embed.set_thumbnail(url=image_url)
            embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
            embed.set_footer(text='nyaa~w redblue was here ^~^', icon_url="https://i.imgur.com/hWCLhIZ.png")
            embed.add_field(
                name="__💸 Price Information__",
                value=f"> **Original Price**: {price_in_robux}" + (f"\n> **Lowest Resale Price**: {details_data.get('CollectiblesItemDetails', {}).get('CollectibleLowestResalePrice', 0)}" if details_data.get('CollectiblesItemDetails', {}) is not None and details_data.get('CollectiblesItemDetails', {}).get('CollectibleLowestResalePrice', 0) is not None and details_data.get('CollectiblesItemDetails', {}).get('CollectibleLowestResalePrice', 0) != 0 else ''),
                inline=False
            )
            embed.add_field(
                name="__⏰ Time Information__",
                value=f"> **Created**: {creationdiscord_timestampTR} | {creationdiscord_timestampT}\n> **Last Updated**: {updatediscord_timestampTR} | {updatediscord_timestampT}",
                inline=False
            )

            if str(assettypes[details_data.get('AssetTypeId')]) == "Place":
                not_item = True
            if remaining is not None and total_quantity is not None and total_quantity != 0:
                given_percent, remaining_percent = calculate_percentages(remaining, total_quantity)
            else:
                given_percent = None
                remaining_percent = None
            if remaining is not None and total_quantity is not None and total_quantity != 0:
                embed.add_field(
                    name="__📦 Stock Info__",
                    value=(f"> **Remaining:** {remaining}/{total_quantity}\n" if remaining is not None and total_quantity is not None else '') +
                            (f"> **Percentage Left:** {given_percent:.1f}% | ({str(remaining)} left)\n" if given_percent is not None else '') +
                            (f"> **Percentage Sold:** {remaining_percent:.1f}% | ({str(total_quantity-remaining)} sold)" if remaining_percent is not None else ''),
                    inline=False
                )
            if details_data.get("SaleLocation", {}) and details_data.get("SaleLocation", {}).get("UniverseIds", []):
                if details_data.get("SaleLocation", {}).get("SaleLocationType") == 6 :
                    for idx, game_name in enumerate(game_names, start=1):
                        embed.add_field(name=f"〘{idx}〙 {game_name}", value=f"- **[Game Link](https://www.roblox.com/games/{str(game_links[idx-1])}/Redblue)**  ``|-|``  **[Join Game](https://www.roblox.com/games/start?launchData=redbluewashere&placeId={str(game_links[idx-1])})**", inline=False)
            else:
                if not_item == False and details_data.get("IsForSale") == True:
                    embed.add_field(name="__🌐 Website Item!!__", value=f"> **[Redblue Link](https://www.roblox.com/games/15765003674)**  ``|-|``  **[Join Redblue](https://www.roblox.com/games/start?launchData=redbluewashere&placeId=15765003674)**\n> **[Rolimons Link](https://www.roblox.com/games/14056754882)**  ``|-|``  **[Join Rolimons](https://www.roblox.com/games/start?launchData=redbluewashere&placeId=14056754882)**", inline=False)
            await ctx.reply(str(item_id), mention_author=False,embed=embed, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False))
        else:
            await ctx.reply("❌ Failed to retrieve item details.", mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False))
    except Exception as e:
        traceback.print_exc()
        await ctx.reply("⚠️ Error occurred or invalid item ID.", mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False))



@bot.hybrid_command()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@commands.cooldown(1, 14, commands.BucketType.user)
async def stock(ctx, *, item_id1: str):
    print(f"{ctx.message.author} used the command: Stock with {item_id1}")
    try:
        item_id1 = item_id1.replace("fxroblox", "roblox")
        if "catalog/" in item_id1:
            item_id = item_id1.split("/catalog/")[1].split("/")[0]
        elif "item/" in item_id1:
            item_id = item_id1.split("/item/")[1].split("/")[0]
        else:
            item_id = item_id1
        
        if item_id:
            details_url = f"https://economy.roblox.com/v2/assets/{item_id}/details"
            details_response = session.get(details_url)

            if details_response.status_code == 200:
                details_data = details_response.json()
                name = details_data.get("Name")
                creator = details_data.get("Creator", {}).get("Name")
                total_quantity = 0
                if details_data.get("CollectiblesItemDetails") and details_data.get("CollectiblesItemDetails").get("TotalQuantity"):
                    total_quantity = details_data.get("CollectiblesItemDetails").get("TotalQuantity", 0)
                else:
                    total_quantity = None
                    
                remaining = details_data.get("Remaining", 0)

                embed = discord.Embed(
                    description=f"# [{name}](https://www.roblox.com/catalog/{item_id}/)\n👤 **Creator:** {creator}"
                )
                embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
                embed.set_footer(text='nyaa~w redblue was here ^~^', icon_url="https://i.imgur.com/hWCLhIZ.png")
                
                if total_quantity != 0 and total_quantity is not None:
                    if remaining is not None and total_quantity is not None:
                        given_percent, remaining_percent = calculate_percentages(remaining, total_quantity)
                    else:
                        given_percent = None
                        remaining_percent = None
                    embed.add_field(
                        name="📊 __Stock Info__",
                        value=f"> **Remaining:** {remaining}/{total_quantity}\n" +
                        (f"> **Percentage Left:** {given_percent:.1f}% | ({str(remaining)} left)\n" if given_percent is not None else '') +
                        (f"> **Percentage Sold:** {remaining_percent:.1f}% | ({str(total_quantity - remaining)} sold)" if remaining_percent is not None else ''),
                        inline=False
                    )

                await ctx.reply(str(item_id), mention_author=False, embed=embed, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False))
            else:
                await ctx.reply("⚠️ Failed to retrieve item details.", mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False))
        
        if item_id1 is None:
            await ctx.reply("⚠️ Please add an item link or item ID", mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False))
    
    except Exception as e:
        print(e)
        await ctx.reply("❌ Error occurred or invalid item ID.", mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False))


@stock.error
async def stock_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.now(datetime.timezone.utc)
        em.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.reply(embed=em, mention_author=False)

@bot.hybrid_command()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@commands.cooldown(1, 14, commands.BucketType.user)

async def item2universe(ctx, item_id1: str):
    print(f"{ctx.message.author} used the command: item2universe with {item_id1}")
    try:
        item_id1 = item_id1.replace("fxroblox", "roblox")
        if "catalog/" in item_id1:
            item_id = item_id1.split("/catalog/")[1].split("/")[0]
        elif "item/" in item_id1:
            item_id = item_id1.split("/item/")[1].split("/")[0]
        else:
            item_id = item_id1
        url = f"https://economy.roblox.com/v2/assets/{item_id}/details"
        response = session.get(url)
        if response.status_code == 200:
            data = response.json()
            sale_location = data.get("SaleLocation", {})
            universe_ids = sale_location.get("UniverseIds", [])

            if universe_ids:
                message = f"**```Universe ID(s):```**\n > " + '\n > '.join(str(id) for id in universe_ids) + "."

                await ctx.reply(message, mention_author=False)
            else:
                await ctx.reply("No universe IDs found for this item.", mention_author=False)
        else:
            await ctx.reply("Failed to retrieve item details.", mention_author=False)
        if item_id1 is None: 
            await ctx.reply("Please add an item link or item ID", mention_author=False)
    except Exception as e:
        print(e)
        await ctx.reply("An error occurred while fetching the sale universes.", mention_author=False)
@item2universe.error
async def item2universe_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.now(datetime.timezone.utc)
        em.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.reply(embed=em, mention_author=False)

@bot.hybrid_command()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@commands.cooldown(1, 14, commands.BucketType.user)
async def item2game(ctx, item_id1: str):
    print(f"{ctx.message.author} used the command: item2game with {item_id1}")
    try:
        item_id1 = item_id1.replace("fxroblox", "roblox")
        if "catalog/" in item_id1:
            item_id = item_id1.split("/catalog/")[1].split("/")[0]
        elif "item/" in item_id1:
            item_id = item_id1.split("/item/")[1].split("/")[0]
        else:
            item_id = item_id1
        response = session.get(f'https://economy.roblox.com/v2/assets/{item_id}/details')
        if response.status_code == 200:
            data = response.json()
            sale_location = data.get('SaleLocation', {})
            universe_ids = sale_location.get('UniverseIds', [])
            if universe_ids:
                root_place_ids = []  
                root_place_names = []  
                for universe_id in universe_ids:
                    game_response = session.get(f'https://games.roblox.com/v1/games?universeIds={universe_id}')
        
                    if game_response.status_code == 200:
                        game_data = game_response.json()
                        root_place_id = game_data['data'][0]['rootPlaceId']
                        root_place_ids.append(root_place_id)
                        root_place_name = game_data['data'][0]['name'].replace('\n', ' ')
                        root_place_names.append(root_place_name)
                    else:
                        await ctx.reply(f"Error: Unable to fetch data {universe_id}. Status code: {game_response.status_code}", mention_author=False)
                modified_ids = ['\n\n> **``{}``**\n> [{}](<https://www.roblox.com/games/{}/Redblue>)'.format(gamena, id, id) for gamena, id in zip(root_place_names, root_place_ids)]
                message = f"**```Root Game(s):```**\n{', '.join(modified_ids)}"
                await ctx.reply(message, mention_author=False)
            else:
                await ctx.reply(f"Error: Unable to fetch data. Status code: {response.status_code}", mention_author=False)
        else:
            await ctx.reply("No universe IDs found for this item.", mention_author=False)
        if item_id1 is None: 
            await ctx.reply("Please add an item link or item ID", mention_author=False)
    except Exception as e:
        print(e)
        await ctx.reply("An error occurred while fetching the sale universes.", mention_author=False)
        
@item2game.error
async def item2game_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.now(datetime.timezone.utc)
        em.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.reply(embed=em, mention_author=False)
@bot.hybrid_command()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@commands.cooldown(1, 14, commands.BucketType.user)

async def item2places(ctx, item_id1: str):
    print(f"{ctx.message.author} used the command: item2places with {item_id1}")
    try:
        item_id1 = item_id1.replace("fxroblox", "roblox")
        if "catalog/" in item_id1:
            item_id = item_id1.split("/catalog/")[1].split("/")[0]
        elif "item/" in item_id1:
            item_id = item_id1.split("/item/")[1].split("/")[0]
        else:
            item_id = item_id1
        response = session.get(f'https://economy.roblox.com/v2/assets/{str(item_id)}/details')

        if response.status_code == 200:
            data = response.json()
            sale_location = data.get('SaleLocation', {})
            universe_ids = sale_location.get('UniverseIds', [])
            if universe_ids:
                place_ids = []  
                place_names = []  

                for universe_id in universe_ids:
                    game_response = session.get(f'https://develop.roblox.com/v1/universes/{str(universe_id)}/places?isUniverseCreation=false&limit=100&sortOrder=Asc')

                    if game_response.status_code == 200:
                        game_data = game_response.json()
                        place_ids.extend([place['id'] for place in game_data['data']])
                        place_names.extend([place['name'].replace('\n', ' ') for place in game_data['data']])

                    else:
                        await ctx.reply(f"Error: Unable to fetch data {universe_id}. Status code: {game_response.status_code}", mention_author=False)
        
                modified_ids = ['\n > {}\nhttps://www.roblox.com/games/{}/Redblue'.format(gamena, id) for gamena, id in zip(place_names, place_ids)] 
        
                message = f"Place(s): {', '.join(modified_ids)}"
                with open("places2.txt", "w", encoding='utf-8', errors='ignore') as f:
                    f.write(message)
                await ctx.reply(file=discord.File("places2.txt"), mention_author=False)
                os.remove("places2.txt")
            else:
                await ctx.reply("No universe IDs found for this item.", mention_author=False)
        else:
            await ctx.reply(f"Error: Unable to fetch data. Status code: {response.status_code}", mention_author=False)
        if item_id1 is None: 
            await ctx.reply("Please add an item link or item ID", mention_author=False)
    except Exception as e:
        traceback.print_exc()
        await ctx.reply("An error occurred while fetching the sale universes.", mention_author=False)


@item2places.error
async def item2places_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.now(datetime.timezone.utc)
        em.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.reply(embed=em, mention_author=False)
@bot.hybrid_command()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@commands.cooldown(1, 14, commands.BucketType.user)

async def game2universe(ctx, game_id1: str):
    print(f"{ctx.message.author} used the command: game2universe with {game_id1}")
    try:
        game_id1 = game_id1.replace("fxroblox", "roblox")
        if "games/" in game_id1:
            game_id = game_id1.split("/games/")[1].split("/")[0]
        else:
            game_id = game_id1
        response = session.get(f'https://apis.roblox.com/universes/v1/places/{str(game_id)}/universe')
        if response.status_code == 200:
            data = response.json()
            universe_ids = data.get('universeId')
            await ctx.reply(f"```{universe_ids}```", mention_author=False)
    except Exception as e:
        print(e)
        await ctx.reply("An error occurred while fetching the sale universes.", mention_author=False)
@game2universe.error
async def game2universe_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.now(datetime.timezone.utc)
        em.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.reply(embed=em, mention_author=False)
@bot.hybrid_command()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@commands.cooldown(1, 14, commands.BucketType.user)
async def game2places(ctx, game_id1: str):
    print(f"{ctx.message.author} used the command: game2places with {game_id1}")
    try:
        game_id1 = game_id1.replace("fxroblox", "roblox")
        if "games/" in game_id1:
            game_id = game_id1.split("/games/")[1].split("/")[0]
        else:
            game_id = game_id1
        response = session.get(f'https://apis.roblox.com/universes/v1/places/{int(game_id)}/universe')

        if response.status_code == 200:
            data = response.json()
            universe_ids = data.get('universeId')
            if universe_ids:
                place_ids1 = []
                place_names1 = []

                for universe_id in [universe_ids]:
                    game_response = session.get(f'https://develop.roblox.com/v1/universes/{universe_id}/places?isUniverseCreation=false&limit=100&sortOrder=Asc')

                    if game_response.status_code == 200:
                        game_data = game_response.json()

                        if isinstance(game_data['data'], list):
                            place_ids1.extend([str(place['id']) for place in game_data['data']])
                            place_names1.extend([str(place['name'].replace('\n', ' ')) for place in game_data['data']])
                        else:
                            await ctx.reply(f"Error: Unexpected data format for universe_id {universe_id}", mention_author=False)
                    else:
                        await ctx.reply(f"Error: Unable to fetch data {universe_id}. Status code: {game_response.status_code}", mention_author=False)

                modified_ids = ['\n > {}\nhttps://www.roblox.com/games/{}/Redblue'.format(gamena1, id1) for gamena1, id1 in zip(place_names1, place_ids1)]

                message = f"Place(s): {', '.join(modified_ids)}"
                with open("places.txt", "w", encoding='utf-8', errors='ignore') as f:
                    f.write(message)
                await ctx.reply(file=discord.File("places.txt"), mention_author=False)
                os.remove("places.txt")
            else:
                await ctx.reply("No universe IDs found for this item.", mention_author=False)
        else:
            await ctx.reply(f"Error: Unable to fetch data. Status code: {response.status_code}", mention_author=False)
        if game_id1 is None: 
            await ctx.reply("Please add a game link or game ID", mention_author=False)
    except Exception as e:
        print(e)
        await ctx.reply("An error occurred while fetching the sale universes.", mention_author=False)

@game2places.error
async def game2places_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.now(datetime.timezone.utc)
        em.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.reply(embed=em, mention_author=False)

@bot.hybrid_command()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@commands.cooldown(1, 14, commands.BucketType.user)
async def ping(ctx):
    print(f"{ctx.message.author} used the command: Ping")
    await ctx.reply(f'{round(bot.latency * 1000)} ms', mention_author=False)


@ping.error
async def ping_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.now(datetime.timezone.utc)
        em.set_footer(text='nyaa~w redblue was here ^~^', icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.reply(embed=em, mention_author=False)

@bot.hybrid_command()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@commands.cooldown(1, 14, commands.BucketType.user)
async def support(ctx):
    print(f"{ctx.message.author} used the command: Support")
    await ctx.reply(f' > [**Keep the Bot Running!**](<https://bot-hosting.net/?aff=1013590472255619103?)\n > [**My Discord**](<https://discord.gg/AynQT7rEy8>)\n > [**UGC Discord**](https://discord.gg/ugcleaks)\n > ****Cashapp - JustAPlayer****\n > [**Robux Donation**](<https://www.roblox.com/catalog/11733073941>)\n > [**Linkvertise**](https://direct-link.net/611550/donation)', mention_author=False)

@support.error
async def support_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.now(datetime.timezone.utc)
        em.set_footer(text='nyaa~w redblue was here ^~^', icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.reply(embed=em, mention_author=False)

@bot.hybrid_command()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@commands.cooldown(1, 14, commands.BucketType.user)
async def convertvip(ctx, vip_link: str):
    vip_link = vip_link.replace("fxroblox", "roblox")
    print(f"{ctx.message.author} used the command: convertvip with {vip_link}")
    url = str(vip_link)
    response = session.get(url)
    await ctx.reply("(For Mobile Players)\n``Your Final Link for The vip is`` [**this**](" + str(response.url) + ")\n(<" + response.url + ">)", mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
    if vip_link is None: 
        await ctx.reply("Please put a VIP Link with the new format.", mention_author=False)
@convertvip.error
async def convertvip_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.now(datetime.timezone.utc)
        em.set_footer(text='nyaa~w redblue was here ^~^', icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.reply(embed=em, mention_author=False)
@bot.hybrid_command()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@commands.cooldown(1, 14, commands.BucketType.user)
async def redblue(ctx):
    print(f"{ctx.message.author} used the command: redblue")
    try:
        url = 'https://api.github.com/repos/JustAP1ayer/redblue/contents/'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            random_file = random.choice(data)
            embed = discord.Embed(title=f"meooow :3 redblue wife generated (Powered by Bing AI)", description=f"nyaaaaaaaaaw", color=10181046)
            embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
            embed.set_image(url=str(random_file['download_url']))
            embed.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
            await ctx.reply(embed=embed, mention_author=False) 
        else:
            await ctx.reply('Error: ' + str(response.status_code), mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
    except Exception as e:
        print(e)
        await ctx.reply("no waifus ;c", mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))

@redblue.error
async def redblue_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down! (i love redblue too <3)", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.now(datetime.timezone.utc)
        em.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.reply(embed=em, mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))


@bot.hybrid_command()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def uwuify(ctx,*, message : str):
    print(f"{ctx.message.author} used the command: uwuify")
    try:
        embed = discord.Embed(title=f"uwuified text made ^~^", description=f"```{uwu_converter(message)}```", color=7419530)
        embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
        embed.set_thumbnail(url="https://staticdelivery.nexusmods.com/mods/2861/images/thumbnails/243/243-1691911373-110081999.png")

        await ctx.reply(embed=embed, mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
    except Exception as e:
        print(e)
        await ctx.reply("smth went wrong", mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
@uwuify.error
async def uwuify_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.now(datetime.timezone.utc)
        em.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.reply(embed=em, mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))


@bot.hybrid_command()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@commands.cooldown(1, 14, commands.BucketType.user)
async def uploader(ctx, item_id1: str):
    print(f"{ctx.message.author} used the command: uploader with {item_id1}")
    try:
        item_id1 = item_id1.replace("fxroblox", "roblox")
        if "catalog/" in item_id1:
            item_id = item_id1.split("/catalog/")[1].split("/")[0]
        elif "item/" in item_id1:
            item_id = item_id1.split("/item/")[1].split("/")[0]
        else:
            item_id = item_id1
        url = "https://assetdelivery.roblox.com/v1/asset/"
        params = {
            "id": item_id,
            "version": "0"
        }

        response = session.get(url, params=params)

        if response.status_code == 200:
            pattern = r'rbxassetid://(\d+)'
            match = re.search(pattern, response.text)

            if match:
                asset_id = match.group(1)
                details_url = f"https://economy.roblox.com/v2/assets/{str(asset_id)}/details"
                details_response = session.get(details_url)
                details_data = details_response.json()
                if details_data.get("Creator", {}).get("CreatorType") == "User":
                    creatorname = details_data.get("Creator", {}).get("Name")
                    creatorid = details_data.get("Creator", {}).get("Id")
                    em = discord.Embed(title="🎉 Asset Uploader Found!")
                    em.add_field(name=f"🔖  Item Id: {item_id}", value=f"https://www.roblox.com/catalog/{item_id}/Redblue", inline=False)
                    player_url = f"https://users.roblox.com/v1/users/{str(creatorid)}"
                    player_response = session.get(player_url)
                    thumbnail_url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={str(creatorid)}&size=352x352&format=Png&isCircular=false"
                    thumbnail_response = session.get(thumbnail_url)
                    em.add_field(name=f"🆔 Creator ID: {creatorid}", value=f"https://www.roblox.com/users/{str(creatorid)}/profile", inline=False)
                    em.timestamp = datetime.datetime.now(datetime.timezone.utc)
                    em.set_footer(text='nyaa~w redblue was here ^~^', icon_url="https://i.imgur.com/hWCLhIZ.png")
                    if thumbnail_response.status_code == 200:
                        thumbnail_data = thumbnail_response.json()
                        em.set_thumbnail(url=str(thumbnail_data["data"][0]["imageUrl"]))
                    if player_response.status_code == 200:
                        player_response_data = player_response.json()
                        em.add_field(name=f"👤 Creator Name: {creatorname}", value=f"👥 **Creator Display Name: {player_response_data.get('displayName')}**", inline=False)
                    await ctx.reply(embed=em, mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
                else:
                    creatorname = details_data.get("Creator", {}).get("Name")
                    creatorid = details_data.get("Creator", {}).get("CreatorTargetId")
                    em = discord.Embed(title="🎉 Asset Uploader Found!")
                    em.add_field(name=f"🔖  Item Id: {item_id}", value=f"https://www.roblox.com/catalog/{item_id}/Redblue", inline=False)
                    player_url = f"https://groups.roblox.com/v2/groups?groupIds={str(creatorid)}"
                    print(player_url)
                    player_response = session.get(player_url)
                    thumbnail_url = f"https://thumbnails.roblox.com/v1/groups/icons?groupIds={str(creatorid)}&size=420x420&format=Png&isCircular=false"
                    thumbnail_response = session.get(thumbnail_url)
                    em.add_field(name=f"👤 Group ID: {creatorid}", value=f"https://www.roblox.com/groups/{str(creatorid)}/profile", inline=False)
                    em.timestamp = datetime.datetime.now(datetime.timezone.utc)
                    em.set_footer(text='nyaa~w redblue was here ^~^', icon_url="https://i.imgur.com/hWCLhIZ.png")
                    if thumbnail_response.status_code == 200:
                        thumbnail_data = thumbnail_response.json()
                        em.set_thumbnail(url=str(thumbnail_data["data"][0]["imageUrl"]))
                    if player_response.status_code == 200:
                        player_response_data = player_response.json()
                        print(player_response_data)
                        userid = player_response_data['data'][0]['owner']['id']
                        if userid and userid is not None:
                            em.add_field(name=f"👥 Group Name: {creatorname}", value=f"**🆔 Group Owner ID: {userid}** \n **🔗 Link:** https://www.roblox.com/users/{str(userid)}/profile", inline=False)
                    await ctx.reply(embed=em, mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
            else:
                await ctx.reply("❌ Error Finding the Uploader!", mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
        else:
            await ctx.reply(f"❌ Error: {response.status_code}", mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
        if item_id1 is None: 
            await ctx.reply("⚠️ Please add an item link or an item id", mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))
    except Exception as e:
        traceback.print_exc()
        await ctx.reply("⚠️ An error occurred (are you sure it was an accessory?)", mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))


@uploader.error
async def uploader_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.now(datetime.timezone.utc)
        em.set_footer(text='nyaa~w redblue was here ^~^', icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.reply(embed=em, mention_author=False, allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,users=False))

'''@bot.event
async def on_message(message):
    await bot.process_commands(message)
    try:
        if message.content == ":3" or message.content == ";3":
            random_number = random.random()
            if random_number < 0.07:
                response = requests.get('https://g.tenor.com/v1/search?q=Boykisser&key=LIVDSRZULELA')
                random_gif = random.choice(response.json()['results'])
                preview_url = random_gif['media'][0]['gif']['preview']
                embed = discord.Embed(title=f"meooow :3 boykisser easter egg found", description=f"nyaaaaaaaaaw", color=10181046)
                embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
                embed.set_image(url=str(preview_url))
                embed.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
                await message.channel.send(embed=embed) 
        if message.content == "<@1013590472255619103>" or message.content == "<@1013590472255619103> ":
            random_number = random.random()
            if random_number < 0.25:
                await message.channel.send("https://cdn.discordapp.com/attachments/1028098087480205344/1178823457744621608/dGA7oggFcD6SzfKp.mp4?ex=65778be5&is=656516e5&hm=a9775d6add67709ac6085a61a3362e02db576c73eaad2397ea96793ce2b9e858&") 
    except Exception as e:
        print(e)'''



if config["suggestive_commands"]  == True:
    @bot.hybrid_command()
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 14, commands.BucketType.user)
    async def waifu(ctx):
        print(f"{ctx.message.author} used the command: Waifu")
        try:
            response = requests.get(f'https://api.waifu.im/search?is_nsfw=false')
            if ctx.author.id != 662339610411532319 and  response.status_code == 200:
                waifu_json = response.json()
                waifu_image = waifu_json.get("images")[0]
                if waifu_image:
                    waifu_url = waifu_image.get("url")
                    embed = discord.Embed(title=f"meooow :3 waifu generated", description=f"nyaaaaaaaaaw", color=10181046)
                    if waifu_image.get("source") is not None:
                        embed.add_field(name=f"Source:", value=str(waifu_image.get("source")), inline=False)
                    if waifu_image.get("artist") is not None:
                        embed.add_field(name=f"Artist:", value=str(waifu_image.get('artist').get('name')), inline=False)
                        if waifu_image.get("artist").get("pixiv") is not None:
                            embed.add_field(name=f"Artist's Pixiv:", value=str(waifu_image.get('artist').get('pixiv')), inline=False)
                        if waifu_image.get("artist").get("twitter") is not None:
                            embed.add_field(name=f"Artist's Twitter:", value=str(waifu_image.get('artist').get('twitter')), inline=False)
                    if waifu_url:
                        embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
                        embed.set_image(url=str(waifu_url))
                        embed.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
                        await ctx.reply(embed=embed, mention_author=False) 
                    else:
                        await ctx.reply("no waifus ;c", mention_author=False)
                else:
                    await ctx.reply("no waifus ;c", mention_author=False)
            else:
                await ctx.reply("no waifus ;c", mention_author=False)
        except Exception as e:
            print(e)
            await ctx.reply("no waifus ;c", mention_author=False)

    @waifu.error
    async def waifu_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow down! (u weird asf tho)", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
            em.timestamp = datetime.datetime.now(datetime.timezone.utc)
            em.set_footer(text='redblue is disgusted, redblue better',icon_url="https://i.imgur.com/hWCLhIZ.png")
            await ctx.reply(embed=em, mention_author=False)
    @bot.hybrid_command()
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @commands.cooldown(1, 18, commands.BucketType.user)
    async def neko(ctx, content_type="safe"):
        print(f"{ctx.message.author} used the command: neko {content_type}" )
        try:
            if content_type == "safe":
                response = requests.get(f'https://api.nekosapi.com/v3/images/random?limit=1&rating={content_type}')
            elif content_type in ["explicit", "borderline", "suggestive"] : 
                if ctx.guild is None or ctx.channel.is_nsfw():
                    response = requests.get(f'https://api.nekosapi.com/v3/images/random?limit=1&rating={content_type}')
            if ctx.author.id != 662339610411532319 and content_type and response.status_code == 200:
                waifu_json = response.json()
                waifu_image = waifu_json.get("items")[0]
                if waifu_image:
                    waifu_url = waifu_image.get("image_url")
                    embed = discord.Embed(title=f"meooow :3 waifu generated", description=f"nyaaaaaaaaaw", color=10181046)
                    if waifu_image.get("artist") is not None:
                        if waifu_image.get("artist").get("name") is not None:
                            embed.add_field(name=f"artist:", value=str(waifu_image.get("artist").get("name")), inline=False)
                        if waifu_image.get("artist").get("links") is not None:
                            embed.add_field(name=f"links:", value=str(waifu_image.get("artist").get("links")), inline=False)
                    if waifu_url:
                        embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
                        embed.set_image(url=str(waifu_url))
                        embed.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
                        await ctx.reply(embed=embed, mention_author=False) 
                    else:
                        await ctx.reply("no waifus ;c", mention_author=False)
                else:
                    await ctx.reply("no waifus ;c", mention_author=False)
            else:
                await ctx.reply("no waifus ;c ", mention_author=False)
        except Exception as e:
            print(e)
            await ctx.reply("no waifus ;c (NSFW Channel or wrong age rating or error)", mention_author=False)
    @neko.error
    async def neko_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow down! (u weird asf tho)", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
            em.timestamp = datetime.datetime.now(datetime.timezone.utc)
            em.set_footer(text='redblue is disgusted, redblue better',icon_url="https://i.imgur.com/hWCLhIZ.png")
            await ctx.reply(embed=em, mention_author=False)

bot.run(config["token"])

