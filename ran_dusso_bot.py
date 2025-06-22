import os
import asyncio
import random
import discord
from dotenv import load_dotenv
import requests
import datetime
from random import SystemRandom
import time
import schedule

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client(intents=discord.Intents.all())  

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    client.loop.create_task(task())
    
@client.event
async def on_message(message):
    # If it was the bot that posted then ignore
    if message.author == client.user:
        return

    # Print latest message
    try:
      print(message.content())
    except:
      print("New Message: ", message.content)

    # Respond with this if anyone @s Ran_Dusso
    if message.content.find("@1021989181142085693")>-1:
        print("Responding...")
        response = 'Haha! Business!'
        await message.channel.send(response)

    # Respond with 'wifi' if anyone says wifi
    if message.content.find("wifi")>-1 or message.content.find("Wifi")>-1:
        await message.channel.send("'wifi'")

# Cross word link stuff
def get_url():
    current_time = datetime.datetime.now()
    month = current_time.strftime("%B")
    day   = current_time.day
    year = current_time.year
    current_date = month + ' ' + str(day)
    file = open('./last_date.txt','r')
    file_data = file.readlines()
    last_date_posted = file_data[0]
    file.close()
    NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=1)

    if last_date_posted == current_date:
        print('Already posted this link')
        final_url = ''
        return
    url = 'https://api.foracross.com/api/puzzle_list?page=0&pageSize=50&filter[nameOrTitleFilter]=ny%20times&filter[sizeFilter][Mini]=true&filter[sizeFilter][Standard]=true'
    try:
        r = requests.get(url)
    except:
        return
    jsonData = r.json()
    for data in jsonData["puzzles"]:
        title = data["content"]["info"]["title"]
        if title.find(current_date) > -1 and title.find(str(year)) > -1:
            print('Current Date: ', current_date)
            print('last date_posted: ', last_date_posted)
            pid = data["pid"]
            print('title: ', title)
            cryptogen = SystemRandom()
            ss = ''
            for j in range(7):
                ss += str(cryptogen.randrange(8)+1)
            p = {'gid':ss+'-butt','pid':pid}
            post_url = 'https://api.foracross.com/api/game'
            rp = requests.post(post_url,json=p)
            if rp.status_code == 200:
                final_url = 'https://downforacross.com/beta/game/' + ss + '-butt'
                print(final_url)
                with open('./last_date.txt','w') as f:
                    f.write(current_date)
                print("Got url for ", current_date)
                with open('url2send.txt','w') as f:
                    f.write(current_date+' '+final_url)
                return
    print('No puzzle found for ' + current_date)

    # Try looking for "New York Times" instead of "NY Times"
    url = 'https://api.foracross.com/api/puzzle_list?page=0&pageSize=50&filter[nameOrTitleFilter]=new%20york%20times&filter[sizeFilter][Mini]=true&filter[sizeFilter][Standard]=true'
    try:
      r = requests.get(url)
    except:
      return
    jsonData = r.json()
    for data in jsonData["puzzles"]:
        title = data["content"]["info"]["title"]
        print('this title: ',title)
        if title.find(current_date) > -1:
            print('Current Date: ', current_date)
            print('last date_posted: ', last_date_posted)
            pid = data["pid"]
            print('pid: ', pid)
            cryptogen = SystemRandom()
            ss = ''
            for j in range(7):
                ss += str(cryptogen.randrange(8)+1)
            p = {'gid':ss+'-butt','pid':pid}
            post_url = 'https://api.foracross.com/api/game'
            rp = requests.post(post_url,json=p)
            if rp.status_code == 200:
                final_url = 'https://downforacross.com/beta/game/' + ss + '-butt'
                print(final_url)
                print("Got url for ", current_date)
                with open('url2send.txt','w') as f:
                    f.write(current_time.strftime('%A')+'  '+current_date+' '+final_url + ' haha business')
                with open('./last_date.txt','w') as f:
                    f.write(current_date)
                return
    print('No "New York Times" puzzle found for ' + current_date)

    # Try to find yesterdays
    #one_day = datetime.timedelta(days=1)
    #yesterday = datetime.date.today() - one_day

async def task():
    while True:
      # Check if we have already posted todays puzzle     
      #current_time = datetime.datetime.now()
      #month = current_time.strftime("%B")
      #day   = current_time.day
      #current_date = month + ' ' + str(day)
      #file = open('./last_date.txt','r')
      #file_data = file.readlines()
      #last_date_posted = file_data[0]
      #file.close()

      # Get day after last date posted
      #next_date = datetime.datetime.today() + datetime.timedelta(days=1)
      #next_date_month = next_date.strftime("%B")
      #next_date_day = next_date.day
      #next_date = next_date_month + ' ' + str(next_date_day)
                                       
      get_url()

      # Open file, check for url, close file
      file = open('url2send.txt','r')
      file_data = file.readlines()
      if len(file_data)>0:
        url_to_send = file_data[0] # get url stored in txt file
        channel_id = 1019039957186265218 # crossword channel id in disc
        file.close()
        channel = client.get_channel(channel_id)
        await channel.send(url_to_send) #  Sends message to channel
        with open('url2send.txt','w') as f:
          f.write('') # delete url stored in txt file
      else:
        file.close()

      print("Sleeping...")
      await asyncio.sleep(3600)

client.run(TOKEN)