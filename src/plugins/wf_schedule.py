import json

# import os
# import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
# import time
import datetime
# from datetime import datetime


def readFileJson(file_name):
    # 包一下读取json
    with open(file_name, "r", encoding="UTF-8") as f:
        data = json.load(f)
    return data


def spliceLayer(layer1: Image, layer2: Image, box: tuple[int, int, int, int]) -> Image:
    img = Image.new('RGBA', layer1.size, (255, 255, 255, 0))
    img.paste(layer1, (0, 0), layer1)
    img.paste(layer2, box, layer2)
    return img


def spliceLayerT(layer1: Image, layer2: Image, box: tuple[int, int, int, int]) -> Image:
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
unit_day_height = 144

# 总的pick up安排
boss_battle_multi_pickup_event = readFileJson(
    r"data/wf_schedule/boss_battle_multi_pickup_event.json")
# 每次pick up的详细安排
boss_battle_multi_pickup_event_schedule = readFileJson(
    r"data/wf_schedule/boss_battle_multi_pickup_event_schedule.json")

# 读取当前时间
current_time = datetime.datetime.now()

for item in boss_battle_multi_pickup_event:
    # 我也不知道有啥用, 姑且作为底图的名字吧
    code_name = boss_battle_multi_pickup_event[item][0]

    # 掉落倍率(加算)
    multiplier = boss_battle_multi_pickup_event[item][3]

    # 文件里储存的是str, 要转成datetime
    start_time = datetime.datetime.strptime(
        boss_battle_multi_pickup_event[item][6], '%Y-%m-%d %H:%M:%S')
    end_time = datetime.datetime.strptime(
        boss_battle_multi_pickup_event[item][7], '%Y-%m-%d %H:%M:%S')

    # 找到当前时间对应的pick up内容
    if (current_time >= start_time) and (current_time <= end_time):
        pu_number = item
        break

text = [f"{start_time.strftime('%Y年%m月%d日%H:%M')}~{end_time.strftime('%Y年%m月%d日%H:%M')}",
        "活动期间以协力战斗挑战特选对象领主",
        f"可获得的领主币、经验值和玛纳将变为{multiplier}倍!"]
duration = (end_time-start_time).days + 2  # 活动持续时间

background_layer = Image.new(
    'RGBA', (1170, 470 + unit_day_height * duration), (255, 255, 255, 0))

head_img = Image.open(r'data/wf_schedule/sprite_sheet/head.png')
body_img = Image.open(r'data/wf_schedule/sprite_sheet/body.png')
body_img = body_img.resize((1170, -42 + unit_day_height * duration))
foot_img = Image.open(r'data/wf_schedule/sprite_sheet/foot.png')

background_layer.paste(head_img, (0, 0),)
background_layer.paste(body_img, (0, 256),)
background_layer.paste(foot_img, (0, 214 + unit_day_height * duration))

draw = ImageDraw.Draw(background_layer)
ft = ImageFont.truetype(r"data/wf_schedule/SY.ttf", 37)
ft2 = ImageFont.truetype(r"data/wf_schedule/SY.ttf", 33)
draw.text((96, 256), text[0], font=ft, fill="#525252")
draw.text((96, 320), text[1], font=ft, fill="#525252")
draw.text((96, 368), text[2], font=ft, fill="#525252")
draw.text((291, 320), text[1][5:9], font=ft, fill="#FF9933")
draw.text((252, 368), text[2][4:-2], font=ft, fill="#FF9933")


line_img = Image.open(
    r"data/wf_schedule/sprite_sheet/line.png").convert('RGBA')
drawDate = start_time

for i in range(0, duration + 1):
    if i < duration - 1:
        background_layer.paste(
            line_img, (57, 570 + unit_day_height*i), line_img)
    draw.text((56, 466 + unit_day_height*i),
              drawDate.strftime('%m月%d日'), font=ft2, fill="#525252")
    drawDate += datetime.timedelta(days=1)

decoration_white_img = Image.open(
    r'data/wf_schedule/sprite_sheet/bottom_right_decoration_white.png').convert('RGBA')
decoration_purple_img = Image.open(
    r'data/wf_schedule/sprite_sheet/bottom_right_decoration_purple.png').convert('RGBA')
decoration_red_img = Image.open(
    r'data/wf_schedule/sprite_sheet/bottom_right_decoration_red.png').convert('RGBA')

blank_layer = Image.new('RGBA', background_layer.size, (255, 255, 255, 0))
foreground_layer = blank_layer.copy()
decoration_layer = blank_layer.copy()
draw = ImageDraw.Draw(foreground_layer)

for item in boss_battle_multi_pickup_event_schedule[pu_number]:
    # boss的编号, 这个有用, 要拿去提审thumbnail
    boss_number = boss_battle_multi_pickup_event_schedule[pu_number][item][1]

    # 同上, 每个小方块对应的起止时间, 从str转换成datetime
    start_time_son = datetime.datetime.strptime(
        boss_battle_multi_pickup_event_schedule[pu_number][item][6], '%Y-%m-%d %H:%M:%S')
    end_time_son = datetime.datetime.strptime(
        boss_battle_multi_pickup_event_schedule[pu_number][item][7], '%Y-%m-%d %H:%M:%S')

    if (current_time >= start_time_son) and (current_time <= end_time_son):
        decoration_img = decoration_purple_img
        fill_color = '#6E196F'
        outline_color = '#841E85'
    else:
        decoration_img = decoration_white_img
        fill_color = '#FAFAFA'
        outline_color = '#FFFFFF'

    # 不知道怎么筛选, 干脆固定不取第一个好了
    # 不对啊那普通的pick up怎么办
    if (item != "1"):
        draw.rounded_rectangle((218, 498 + int(int((start_time_son - start_time).total_seconds())/(24*60*60/unit_day_height)), 1103, 490 + int(
            int((end_time_son - start_time).total_seconds())/(24*60*60/unit_day_height))), radius=24, fill=fill_color, outline=outline_color, width=5)
        decoration_layer.paste(decoration_img, (836, 333 + int(int((end_time_son -
                               start_time).total_seconds())/(24*60*60/unit_day_height))), decoration_img)

blank_layer.paste(decoration_layer, (0, 0), foreground_layer)
decoration_layer = blank_layer.copy()
blank_layer = Image.new('RGBA', background_layer.size, (255, 255, 255, 0))

shadow_layer = Image.new('RGB', background_layer.size, (200, 200, 200))
blank_layer.paste(shadow_layer, (0, 0), foreground_layer)
shadow_layer = blank_layer.copy()
blank_layer = Image.new('RGBA', background_layer.size, (255, 255, 255, 0))
shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(6))

background_layer.paste(shadow_layer, (0, 0), shadow_layer)
background_layer.paste(foreground_layer, (0, 0), foreground_layer)
background_layer.paste(decoration_layer, (0, 0), decoration_layer)

background_layer = background_layer.convert('RGB')
background_layer.save(r"data/wf_schedule/test2.png")
background_layer.show()
