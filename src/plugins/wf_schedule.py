import json

# import os
# import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
# import time
import datetime
# from datetime import datetime


def readFileJson(fileName):
    # 包一下读取json
    with open(fileName, "r", encoding="UTF-8") as f:
        data = json.load(f)
    return data


def spliceLayer(layer1, layer2, box):
    img = Image.new('RGBA', layer1.size, (255, 255, 255, 0))
    img.paste(layer1, (0, 0), layer1)
    img.paste(layer2, box, layer2)
    return img


def spliceLayerT(layer1, layer2, box):
    img = Image.new('RGBA', layer2.size, (255, 255, 255, 0))
    img.paste(layer1, box, layer1)
    img.paste(layer2, (0, 0), layer2)
    return img


def nineSliceUi(img: Image, box: tuple[int, int, int, int], size: tuple[int, int]) -> Image:
    x1, y1, x2, y2 = box
    x3, y3 = img.size
    x0, y0 = size

    w1 = x1
    w3 = x3-x2
    w4 = x0-w1-w3
    h1 = y1
    h3 = y3-y2
    h4 = y0-h1-h3

    img1 = img.crop((0, 0, x1, y1))
    img2 = img.crop((x1, 0, x2, y1))
    img3 = img.crop((x2, 0, x3, y1))
    img4 = img.crop((0, y1, x1, y2))
    img5 = img.crop((x1, y1, x2, y2))
    img6 = img.crop((x2, y1, x3, y2))
    img7 = img.crop((0, y2, x1, y3))
    img8 = img.crop((x1, y2, x2, y3))
    img9 = img.crop((x2, y2, x3, y3))

    img2 = img2.resize((w4, h1))
    img4 = img4.resize((w1, h4))
    img5 = img5.resize((w4, h4))
    img6 = img6.resize((w3, h4))
    img8 = img8.resize((w4, h3))

    img = Image.new('RGBA', size, (255, 255, 255, 0))
    img.paste(img1, (0, 0), img1)
    img.paste(img2, (w1, 0), img2)
    img.paste(img3, (w1+w4, 0), img3)
    img.paste(img4, (0, h1), img4)
    img.paste(img5, (w1, h1), img5)
    img.paste(img6, (w1+w4, h1), img6)
    img.paste(img7, (0, h1+h4), img7)
    img.paste(img8, (w1, h1+h4), img8)
    img.paste(img9, (w1+w4, h1+h4), img9)
    return img


# 这张图的1天有多少px
unitDayHeight = 144

# 总的pick up安排
boss_battle_multi_pickup_event = readFileJson(r"data/wf_schedule/boss_battle_multi_pickup_event.json")
# 每次pick up的详细安排
boss_battle_multi_pickup_event_schedule = readFileJson(r"data/wf_schedule/boss_battle_multi_pickup_event_schedule.json")

# 读取当前时间
currentTime = datetime.datetime.now()

for item in boss_battle_multi_pickup_event:
    # 我也不知道有啥用, 姑且作为底图的名字吧
    codeName = boss_battle_multi_pickup_event[item][0]

    # 掉落倍率(加算)
    multiplier = boss_battle_multi_pickup_event[item][3]

    # 文件里储存的是str, 要转成datetime
    startTime = datetime.datetime.strptime(boss_battle_multi_pickup_event[item][6], '%Y-%m-%d %H:%M:%S')
    endTime = datetime.datetime.strptime(boss_battle_multi_pickup_event[item][7], '%Y-%m-%d %H:%M:%S')

    # 找到当前时间对应的pick up内容
    if (currentTime >= startTime) and (currentTime <= endTime):
        puNumber = item
        break

text = [f"{startTime.strftime('%Y年%m月%d日%H:%M')}~{endTime.strftime('%Y年%m月%d日%H:%M')}",
        "活动期间以协力战斗挑战特选对象领主",
        f"可获得的领主币、经验值和玛纳将变为{multiplier}倍!"]
duration = (endTime-startTime).days + 2  # 活动持续时间

backgroundLayer = Image.new('RGBA', (1170, 470 + unitDayHeight * duration), (255, 255, 255, 0))

headImg = Image.open(r'data/wf_schedule/sprite_sheet/head.png')
bodyImg = Image.open(r'data/wf_schedule/sprite_sheet/body.png')
bodyImg = bodyImg.resize((1170, -42 + unitDayHeight * duration))
footImg = Image.open(r'data/wf_schedule/sprite_sheet/foot.png')

backgroundLayer.paste(headImg, (0, 0),)
backgroundLayer.paste(bodyImg, (0, 256),)
backgroundLayer.paste(footImg, (0, 214 + unitDayHeight * duration))

draw = ImageDraw.Draw(backgroundLayer)
ft = ImageFont.truetype(r"data/wf_schedule/SY.ttf", 37)
ft2 = ImageFont.truetype(r"data/wf_schedule/SY.ttf", 33)
draw.text((96, 256), text[0], font=ft, fill="#525252")
draw.text((96, 320), text[1], font=ft, fill="#525252")
draw.text((96, 368), text[2], font=ft, fill="#525252")
draw.text((291, 320), text[1][5:9], font=ft, fill="#FF9933")
draw.text((252, 368), text[2][4:-2], font=ft, fill="#FF9933")


lineImg = Image.open(r"data/wf_schedule/sprite_sheet/line.png").convert('RGBA')
drawDate = startTime

for i in range(0, duration + 1):
    if i < duration - 1:
        backgroundLayer.paste(lineImg, (57, 570 + unitDayHeight*i), lineImg)
    draw.text((56, 466 + unitDayHeight*i), drawDate.strftime('%m月%d日'), font=ft2, fill="#525252")
    drawDate += datetime.timedelta(days=1)

whiteDecoration = Image.open(r'data/wf_schedule/sprite_sheet/bottom_right_decoration_white.png').convert('RGBA')
purpleDecoration = Image.open(r'data/wf_schedule/sprite_sheet/bottom_right_decoration_purple.png').convert('RGBA')
redDecoration = Image.open(r'data/wf_schedule/sprite_sheet/bottom_right_decoration_red.png').convert('RGBA')

foregroundLayer = Image.new('RGBA', backgroundLayer.size, (255, 255, 255, 0))
decorationLayer = Image.new('RGBA', backgroundLayer.size, (255, 255, 255, 0))
draw = ImageDraw.Draw(foregroundLayer)

for item in boss_battle_multi_pickup_event_schedule[puNumber]:
    # boss的编号, 这个有用, 要拿去提审thumbnail
    bossNumber = boss_battle_multi_pickup_event_schedule[puNumber][item][1]

    # 同上, 每个小方块对应的起止时间, 从str转换成datetime
    startTimeSon = datetime.datetime.strptime(boss_battle_multi_pickup_event_schedule[puNumber][item][6], '%Y-%m-%d %H:%M:%S')
    endTimeSon = datetime.datetime.strptime(boss_battle_multi_pickup_event_schedule[puNumber][item][7], '%Y-%m-%d %H:%M:%S')

    if (currentTime >= startTimeSon) and (currentTime <= endTimeSon):
        decorationImg = purpleDecoration
        fillColor = '#6E196F'
        outlineColor = '#841E85'
    else:
        decorationImg = whiteDecoration
        fillColor = '#FAFAFA'
        outlineColor = '#FFFFFF'

    if (item != "1"):
        draw.rounded_rectangle((218, 498 + int(int((startTimeSon - startTime).total_seconds())/(24*60*60/unitDayHeight)), 1103, 490 + int(int((endTimeSon - startTime).total_seconds())/(24*60*60/unitDayHeight))), radius=24, fill=fillColor, outline=outlineColor, width=5)
        decorationLayer.paste(decorationImg, (836, 333 + int(int((endTimeSon - startTime).total_seconds())/(24*60*60/unitDayHeight))), decorationImg)

shadowImage = Image.new('RGB', backgroundLayer.size, (200, 200, 200))
foregroundLayer1 = foregroundLayer.copy()
foregroundLayer2 = foregroundLayer.copy()
foregroundLayer.paste(decorationLayer, (0, 0), foregroundLayer)
foregroundLayer1.paste(shadowImage, (0, 0), foregroundLayer1)
shadowImage = foregroundLayer1.filter(ImageFilter.GaussianBlur(6))
backgroundLayer.paste(shadowImage, (0, 0), shadowImage)
backgroundLayer.paste(foregroundLayer2, (0, 0), foregroundLayer2)
backgroundLayer.paste(foregroundLayer, (0, 0), foregroundLayer)
# backgroundLayer.paste(decorationLayer, (0, 0), foregroundLayer)


backgroundLayer = backgroundLayer.convert('RGB')
backgroundLayer.save(r"data/wf_schedule/test2.png")
backgroundLayer.show()
