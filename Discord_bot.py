from discord.ext import commands
from lyricsgenius import Genius
from bs4 import BeautifulSoup
from googlesearch import search
import requests
import youtube_dl


youtube_dl.utils.bug_reports_message = lambda: ''
# Load .env file using:
from dotenv import load_dotenv
load_dotenv()

# Use the variable with:
import os
os.getenv("ACCESS_KEY")
def getTitle(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")
    title = soup.find(["title"]).text
    return title


def getSongs(url):
    print("CALLING")
    output = ""
    title = getTitle("https://www.youtube.com/watch?v=GRpN9ZxNf9M")
    query = "songs like " + title
    newURLs = search(query)
    output += ("You Might Also Like: " + title + "\n\n")
    for i in range(1, 6):
        output += (str(i) + ": " + getTitle(newURLs[i]) + "\n")
    return output


class values:
    saved = ''


genius = Genius("7oL0KKwrqlGfnTnNFDXSI8bSocT_N6XLL0Hsvwq1nqAi2DYKtdApvWX87XOk_Dzu")

bot = commands.Bot(command_prefix='!')

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

def endSong(guild, path):
    os.remove(path)


@bot.event
async def on_ready():
    print("Bot's up")


@bot.command()
async def hello(ctx):
    await ctx.send("hello")


@bot.command()
async def say(ctx, string):
    await ctx.send(string)


@bot.command()
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        if (not ctx.voice_client):
            await channel.connect()
        else:
            await ctx.voice_client.move_to(channel)
    else:
        await ctx.send("User is not in a voice channel")


@bot.command()
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I have left")
    else:
        await ctx.send("I am not in voice channel")


@bot.command()
async def hellothere(ctx):
    await ctx.send("General Kenobi! \nYou are a bold one")


@bot.command()
async def artist(ctx, arg):
    artist = genius.search_artist(arg, max_songs=5, sort="popularity")
    for i in artist.songs:
        await ctx.send(i)


@bot.command()
async def lyrics(ctx, *args):
    arg = ''
    for i in args:
        arg = arg + i + " "
    song = genius.search_song(arg)
    await ctx.send(song.lyrics)


@bot.command()
async def lsearch(ctx, *args):
    arg = ''
    for i in args:
        arg = arg + i + " "
    song = genius.search_lyrics(arg, per_page=1)
    print(song)


@bot.command()
async def echo(ctx, *arg, num):
    for i in range(int(num)):
        await ctx.send(arg)


@bot.command()
async def save(ctx, *args):
    values.saved = ''
    for arg in args:
        values.saved = values.saved + arg + " "

    await ctx.send("saved: " + values.saved)

@bot.command()
async def load(ctx):
    await ctx.send(values.saved)

@bot.command()
async def recommend(ctx, url):
    await ctx.send(getSongs(url))

@bot.command()
async def tourDates(ctx, arg):
    query0 = "ticketmaster ", arg, "tour dates"
    newURL = search(query0)[0]
    page = requests.get(newURL).text
    soup = BeautifulSoup(page, "lxml")
    ctx.send(soup)
  

bot.run("ODg2NDExNDk5MzM2MjQ5MzU0.YT1NCg.VNecWvFgkm6nC27se0dXN1KUQ8g")  # generate key for bot
