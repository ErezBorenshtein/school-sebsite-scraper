import csv
import datetime
import json

import discord
import constants
from discord.ext import tasks

import scraper_trigger as scraper


def get_empty_rooms(csv_file, json_file, day="Sunday", hour=1):
    hour = int(hour)

    # Parse JSON file to get all possible rooms
    with open(json_file, 'r') as file:
        possible_rooms = json.load(file)

    # Create a dictionary mapping day strings to their respective column indices
    day_mapping = {
        "Sunday": 1,
        "Monday": 2,
        "Tuesday": 3,
        "Wednesday": 4,
        "Thursday": 5,
        "Friday": 6
    }

    # Parse CSV file to get used rooms for the specified day and hour
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if int(row[0]) == hour:
                day_index = day_mapping[day]
                used_rooms = set(row[day_index].split(',')) if row[day_index] else set()
                break
        else:
            # If no data found for the specified day and hour, return all possible rooms
            return possible_rooms

    # Find rooms that are not used
    empty_rooms = [room for room in possible_rooms if room not in used_rooms]
    return empty_rooms


def get_day():
    current_date_israel = datetime.datetime.now(constants.ISRAEL_TIMEZONE)
    day_of_week_str = current_date_israel.strftime('%A')
    return day_of_week_str


def get_hour():
    # Get current time in Israel
    current_time_israel = datetime.datetime.now(constants.ISRAEL_TIMEZONE)
    current_time = current_time_israel.time()

    # Find the current hour in the school schedule
    for hour, (start_time, end_time) in constants.SCHOOL_SCHEDULE.items():
        if start_time <= current_time <= end_time:
            return hour

    # If current time is not within any scheduled hour, find the closest hour
    min_difference = float('inf')
    closest_hour = None
    for hour, (start_time, _) in constants.SCHOOL_SCHEDULE.items():
        difference = abs((start_time.hour * 60 + start_time.minute) - (current_time.hour * 60 + current_time.minute))
        if difference < min_difference:
            min_difference = difference
            closest_hour = hour

    return closest_hour


client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    scrape.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!help"):
        embed = discord.Embed(
            title="Commands: ",
            description="!help\n2. !empty classes [Day] [hour]\n3. !empty classes today [hour]\n4. !empty classes",
            color=discord.Color.blue()
        )

        channel = client.get_channel(constants.CHANNEL_ID)
        await channel.send(embed=embed)

    if message.content.startswith('!empty classes'):
        new_message = message.content.split(" ")
        if len(new_message) > 2 and new_message[2].lower() != "today":  # *empty classes [Day] [hour]
            classes = get_empty_rooms("schedule.csv", "available_classes_ironih.json", new_message[2], new_message[3])

            embed = discord.Embed(
                title=f"The empty rooms in {new_message[2]} at hour {new_message[3]} are:",
                description=', '.join(classes),
                color=discord.Color.blue())

            channel = client.get_channel(constants.CHANNEL_ID)
            await channel.send(embed=embed)

        else:
            if len(new_message) == 4:  # *empty classes today [hour]
                classes = get_empty_rooms("schedule.csv", "available_classes_ironih.json", get_day(), new_message[3])
                embed = discord.Embed(
                    title=f"The empty rooms today({get_day()}) at hour {new_message[3]} are:",
                    description=', '.join(classes),
                    color=discord.Color.blue())

                channel = client.get_channel(constants.CHANNEL_ID)
                await channel.send(embed=embed)
            else:
                closest_hour = get_hour()
                if closest_hour is not None and get_day() != "Saturday":
                    classes = get_empty_rooms("schedule.csv", "available_classes_ironih.json", get_day(), closest_hour)
                    embed = discord.Embed(
                        title=f"The empty rooms today({get_day()}) at hour {closest_hour} are:",
                        description=', '.join(classes),
                        color=discord.Color.blue()
                    )
                    channel = client.get_channel(constants.CHANNEL_ID)
                    await channel.send(embed=embed)
                else:
                    await message.channel.send("school has finished today")


@tasks.loop(hours=24)
async def scrape():
    print("scraping...")
    scraper.start()


TOKEN = open('token.txt').read()

client.run(TOKEN)
