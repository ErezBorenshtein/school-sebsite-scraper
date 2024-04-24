import json
import csv
import discord
from discord.ext import tasks
import datetime
from scrape import create_csv
import pytz
import os


def get_empty_rooms(csv_file, json_file, day="Sunday", hour=1):
    hour = int(hour)

    # Parse JSON file to get all possible rooms
    with open(json_file, 'r') as f:
        possible_rooms = json.load(f)

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
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
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
    israel_tz = pytz.timezone('Israel')
    
    current_date_israel = datetime.datetime.now(israel_tz)
    #print("current_date_israel:", current_date_israel)
    
    day_of_week_int = current_date_israel.weekday() + 1  #! I dont know why the +1 is needed
    #print("day_of_week_int:", day_of_week_int)
    
    day_of_week_str = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"][day_of_week_int]
    
    return day_of_week_str

def get_hour():
    israel_tz = pytz.timezone('Israel')
    current_time_israel = datetime.datetime.now(israel_tz)
    current_time = current_time_israel.time()

    # Define the school schedule hours
    school_schedule = {
        1: (datetime.time(8, 15), datetime.time(9, 0)),
        2: (datetime.time(9, 0), datetime.time(9, 50)),
        3: (datetime.time(10, 10), datetime.time(10, 55)),
        4: (datetime.time(11, 0), datetime.time(11, 45)),
        5: (datetime.time(11, 50), datetime.time(12, 35)),
        6: (datetime.time(12, 55), datetime.time(13, 35)),
        7: (datetime.time(13, 40), datetime.time(14, 25)),
        8: (datetime.time(14, 30), datetime.time(15, 15)),
        9: (datetime.time(15, 15), datetime.time(16, 0)),
        10: (datetime.time(16, 0), datetime.time(16, 45)),
        11: (datetime.time(16, 45), datetime.time(17, 30)),
  }

    # Find the closest hour in the school schedule
    closest_hour = None
    min_difference = float('inf')
    try:
        for hour, (start_time, end_time) in school_schedule.items():
            if start_time <= current_time <= end_time:
                return hour
            else:
                difference = abs((start_time.hour * 60 + start_time.minute) -(current_time.hour * 60 + current_time.minute))
                if difference < min_difference:
                    min_difference = difference
                    closest_hour = hour

    except Exception as e:
        print(f"Error occurred: {e}")
        return closest_hour

    return closest_hour


client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    print(1)
    scrape.start()
    print(2)



@client.event
async def on_message(message):
    channel_id = 1229734808507256835 #My server channel id
    if message.author == client.user:
        return

    if message.content.startswith("!help"):
      
        embed = discord.Embed(
            title= "Commands: " ,
            description="!help\n2. !empty classes [Day] [hour]\n3. !empty classes today [hour]\n4. !empty classes",
            color=discord.Color.blue()
        )

        channel = client.get_channel(channel_id)
        await channel.send(embed=embed)


    if message.content.startswith('!empty classes'):
        new_message = message.content.split(" ")
        if len(new_message) > 2 and new_message[2].lower() != "today": #*empty classes [Day] [hour]
            classes = get_empty_rooms("schedule.csv", "available_classes_ironih.json", new_message[2], new_message[3])

            embed = discord.Embed(
                title= f"The empty rooms in {new_message[2]} at hour {new_message[3]} are:",
                description=', '.join(classes),
                color=discord.Color.blue())

            channel = client.get_channel(channel_id)
            await channel.send(embed=embed)

        else:
            if len(new_message) == 4:  #*empty classes today [hour]
                classes = get_empty_rooms("schedule.csv", "available_classes_ironih.json", get_day(), new_message[3])
                embed = discord.Embed(
                    title= f"The empty rooms today({get_day()}) at hour {new_message[3]} are:",
                    description=', '.join(classes),
                    color=discord.Color.blue())

                channel = client.get_channel(channel_id)
                await channel.send(embed=embed)
            else:
                closest_hour = get_hour()
                if closest_hour is not None and get_day() != "Saturday":
                    classes = get_empty_rooms("schedule.csv", "available_classes_ironih.json", get_day(), closest_hour)
                    embed = discord.Embed(
                        title= f"The empty rooms today({get_day()}) at hour {closest_hour} are:",
                        description=', '.join(classes),
                        color=discord.Color.blue()
                    )
                    channel = client.get_channel(channel_id)
                    await channel.send(embed=embed)
                else:
                    await message.channel.send("school has finished today")

@tasks.loop(hours=24)
async def scrape():
    print("scraping...")
    try:
        create_csv()
    except Exception as e:
        print(f"Error occurred during scraping: {e}")
        return

#TOKEN = os.environ['TOKEN'] #! For my replit server
with open("token.txt", "r") as f:
    TOKEN = f.read()
#keep_alive() #! To keep the bot alive
client.run(TOKEN)
