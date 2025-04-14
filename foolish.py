import discord
from discord.ext import commands

import random
import os
import json
from dotenv import load_dotenv

# .env 파일에서 토큰 로드
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


# 인텐트 설정
intents = discord.Intents.default()
intents.message_content = True


# commands.Bot만 사용
bot = commands.Bot(command_prefix="!", intents=intents)

with open("tarot.json", "r", encoding="utf-8") as f:
    TAROT_CARDS = json.load(f)

with open("food.json", "r", encoding="utf-8") as f:
    FOOD_MENU = json.load(f)

with open("bullshit.json", "r", encoding="utf-8") as f:
    BULLSHIT = json.load(f)

COIN = [
    {
        "name":"앞면",
        "url":"https://c.tenor.com/IrW2J8NTd2UAAAAC/tenor.gif"
    },
    {
        "name":"뒷면",
        "url":"https://c.tenor.com/Lg-6d1Ruke4AAAAC/tenor.gif"
    }
]


@bot.event
async def on_ready():
    print(f'✅ 봇 로그인 완료: {bot.user}')


@bot.command(name="도움")
async def help(ctx):
    embed = discord.Embed(
        title="현재 사용 가능한 명령어 목록입니다.",
        description="타로카드\n동전\n점메추\n선택\n여담\n주사위\n"
    )
    embed.set_image(url="https://t1.daumcdn.net/news/202105/25/ppss/20210525045052409gkal.jpg")
    await ctx.send(embed=embed)


@bot.command(name="타로카드")
async def tarot(ctx):
    selected = random.choice(TAROT_CARDS)
    name = selected["name"]
    path = selected["path"]

    file = discord.File(path, filename="tarot.png")
    embed = discord.Embed(
        title=f"{name}",
        color=0x6A5ACD
    )
    embed.set_image(url="attachment://tarot.png")
    await ctx.send(file=file, embed=embed)


@bot.command(name="동전")
async def coin(ctx):
    result = random.choice(COIN)
    name = result["name"]
    embed = discord.Embed(
        title=f"{name}",
        color=0x00008B
    )
    embed.set_image(url=result["url"])
    await ctx.send(embed=embed)


@bot.command(name="점메추")
async def lunch(ctx):
    lunch = random.choice(FOOD_MENU)
    embed = discord.Embed(
        title=f"{lunch['name']}",
        color=0x00008B
    )
    embed.set_image(url=lunch["url"])
    await ctx.send(embed=embed)


@bot.command(name="여담")
async def easter(ctx):
    egg = random.choice(BULLSHIT)
    await ctx.send(f'{egg["say"]}')


@bot.command(name="선택")
async def choose(ctx, *choices):
    if len(choices) < 2:
        await ctx.send("두 개 이상의 선택지를 입력해주세요.")
        return

    selected = random.choice(choices)
    await ctx.send(f"제 선택은 {selected}입니다.")


@bot.command(name="주사위")
async def dice(ctx, number: int = 6):
    if number < 1:
        await ctx.send("1 이상의 숫자를 입력해주세요.")
        return

    result = random.randint(1, number)
    await ctx.send(f"주사위 결과는: {result}")


bot.run(TOKEN)