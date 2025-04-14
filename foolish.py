import discord
from discord.ext import commands

import random
import os
import json

# .env 파일에서 토큰 로드
TOKEN = '당신의 Discord Bot Token을 여기에 입력하세요'


# 인텐트 설정
intents = discord.Intents.default()
intents.message_content = True


# commands.Bot만 사용
bot = commands.Bot(command_prefix="!", intents=intents)

# 타로카드
with open("tarot.json", "r", encoding="utf-8") as f:
    TAROT_CARDS = json.load(f)

# 점메추
with open("food.json", "r", encoding="utf-8") as f:
    FOOD_MENU = json.load(f)

# 여담
with open("bullshit.json", "r", encoding="utf-8") as f:
    BULLSHIT = json.load(f)

# 동전
with open("coin.json", "r", encoding="utf-8") as f:
    COIN = json.load(f)

# 호모
with open("homo.json", "r", encoding="utf-8") as f:
    HOMO = json.load(f)


@bot.event
async def on_ready():
    print(f'✅ 봇 로그인 완료: {bot.user}')


@bot.command(name="도움")
async def help(ctx):
    embed = discord.Embed(
        title="현재 사용 가능한 명령어 목록입니다.",
        description="타로카드\n동전\n점메추\n선택\n여담\n주사위\n호모\n"
    )
    embed.set_image(url="https://file.retrotv.me/u/mBvP9w.jpg")
    await ctx.send(embed=embed)


@bot.command(name="타로카드")
async def tarot(ctx):
    selected = random.choice(TAROT_CARDS)
    name = selected["name"]
    url = selected["url"]

    embed = discord.Embed(
        title=f"{name}",
        color=0x6A5ACD
    )
    embed.set_image(url=url)
    await ctx.send(embed=embed)


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


@bot.command(name="호모")
async def homo(ctx):

    # 이미지 데이터 로드
    image_data = HOMO
    if not image_data:
        embed = discord.Embed(
            title="호모! 이미지가 없어요!",
            color=0x00008B
        )

        await ctx.send(embed=embed)
        return

    # 랜덤으로 이미지 선택
    image_info = random.choice(image_data)

    # 임베드 생성
    embed = discord.Embed(
        title="호모",
        description="당신은 이제 호모입니다.",
        color=0x00008B
    )

    # 이미지 파일 경로가 있는 경우
    file_name = image_info.get("file_name")
    url = image_info.get("url")

    if file_name:
        image_path = os.path.join("images", file_name)
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                file = discord.File(f, filename=file_name)
                embed.set_image(url=f"attachment://{file_name}")
                await ctx.send(embed=embed, file=file)

                return

    # 이미지 URL이 있는 경우
    elif url:
        embed.set_image(url=url)
        await ctx.send(embed=embed)

        return

    # 파일 경로와 URL이 모두 없는 경우
    embed = discord.Embed(
        title="호모! 이미지가 없어요!",
        color=0x00008B
    )

    await ctx.send(embed=embed)


bot.run(TOKEN)
