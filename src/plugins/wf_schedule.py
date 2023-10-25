import json
# import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
# import time
import datetime
# from datetime import datetime


def readFileJson(file_name):
    # 包一下读取json
    with open(file_name, "r", encoding="UTF-8") as f:
        data = json.load(f)
    return data


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
# boss列表
boss_battle_quest = readFileJson(
    r"data/wf_schedule/boss_battle_quest.json")
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
    # if (current_time >= start_time) and (current_time <= end_time):
    #     pu_number = item
    #     break
    if item == "16":
        pu_number = item
        break


description_text = [
    f"{start_time.strftime('%Y年%m月%d日%H:%M')}~{end_time.strftime('%Y年%m月%d日%H:%M')}",
    "活动期间以协力战斗挑战特选对象领主",
    f"可获得的领主币、经验值和玛纳将变为{multiplier}倍!"]

duration = (end_time.date() - start_time.date()).days + 1  # 活动持续时间
print(duration)

background_layer = Image.new('RGBA', (1170, 470 + unit_day_height * duration), (255, 255, 255, 0))

head_img = Image.open(r'data/wf_schedule/sprite_sheet/head.png')
body_img = Image.open(r'data/wf_schedule/sprite_sheet/body.png')
body_img = body_img.resize((1170, -42 + unit_day_height * duration))
foot_img = Image.open(r'data/wf_schedule/sprite_sheet/foot.png')

background_layer.paste(head_img, (0, 0),)
background_layer.paste(body_img, (0, 256),)
background_layer.paste(foot_img, (0, 214 + unit_day_height * duration))

draw_background = ImageDraw.Draw(background_layer)
ft37 = ImageFont.truetype(r"data/wf_schedule/SY.ttf", 37)
ft33 = ImageFont.truetype(r"data/wf_schedule/SY.ttf", 33)
gray_color = "#525252"
orange_color = "#FF9933"
draw_background.text((96, 256), description_text[0], font=ft37, fill=gray_color)
draw_background.text((96, 320), description_text[1], font=ft37, fill=gray_color)
draw_background.text((96, 368), description_text[2], font=ft37, fill=gray_color)
draw_background.text((291, 320), description_text[1][5:9], font=ft37, fill=orange_color)
draw_background.text((252, 368), description_text[2][4:-1], font=ft37, fill=orange_color)


line_img = Image.open(r"data/wf_schedule/sprite_sheet/line.png").convert('RGBA')
drawDate = start_time

for i in range(0, duration):
    if i < duration - 1:
        background_layer.paste(line_img, (57, 570 + unit_day_height*i), line_img)
    draw_background.text((56, 466 + unit_day_height*i), drawDate.strftime('%m月%d日'), font=ft33, fill=gray_color)
    drawDate += datetime.timedelta(days=1)

decoration_white_img = Image.open(
    r'data/wf_schedule/sprite_sheet/bottom_right_decoration_white.png').convert('RGBA')
decoration_purple_img = Image.open(
    r'data/wf_schedule/sprite_sheet/bottom_right_decoration_purple.png').convert('RGBA')
decoration_red_img = Image.open(
    r'data/wf_schedule/sprite_sheet/bottom_right_decoration_red.png').convert('RGBA')
line_white = Image.open(
    r'data/wf_schedule/sprite_sheet/line_white.png').convert('RGBA')
line_purple = Image.open(
    r'data/wf_schedule/sprite_sheet/line_purple.png').convert('RGBA')
line_red = Image.open(
    r'data/wf_schedule/sprite_sheet/line_red.png').convert('RGBA')

blank_layer = Image.new('RGBA', background_layer.size, (255, 255, 255, 0))
foreground_layer = blank_layer.copy()
decoration_layer = blank_layer.copy()
line_layer = blank_layer.copy()
boss_mask_layer = blank_layer.copy()
boss_layer = blank_layer.copy()
text_layer = blank_layer.copy()
draw_foreground = ImageDraw.Draw(foreground_layer)
draw_boss_mask = ImageDraw.Draw(boss_mask_layer)
draw_text = ImageDraw.Draw(text_layer)
whole_boss_img = Image.new('RGBA', (8, 8), (255, 255, 255, 0))
whole_boss_name = ""
count_leftrigt = 0
step_length = 1
for item in boss_battle_multi_pickup_event_schedule[pu_number]:
    # boss的编号, 用于提审thumbnail
    boss_number = boss_battle_multi_pickup_event_schedule[pu_number][item][1]

    # 同上, 每个小方块对应的起止时间, 从str转换成datetime
    start_time_son = datetime.datetime.strptime(
        boss_battle_multi_pickup_event_schedule[pu_number][item][6], '%Y-%m-%d %H:%M:%S')
    end_time_son = datetime.datetime.strptime(
        boss_battle_multi_pickup_event_schedule[pu_number][item][7], '%Y-%m-%d %H:%M:%S')
    # 提审thumbnail
    boss_name = boss_battle_quest["1"][boss_number]["1"][2].split()[0]
    boss_img_filename = boss_battle_quest["1"][boss_number]["1"][3]
    boss_img = Image.open(f"data/{boss_img_filename}.png")

    # 将当前时间的pickup加紫
    if (current_time >= start_time_son) and (current_time <= end_time_son):
        decoration_img = decoration_purple_img
        line_img = line_purple
        fill_color = '#6E196F'
        outline_color = '#841E85'
        text_color = '#FFFFFF'
    else:
        decoration_img = decoration_white_img
        line_img = line_white
        fill_color = '#FAFAFA'
        outline_color = '#FFFFFF'
        text_color = gray_color
    # 如果是全程up的内容
    if (start_time_son == start_time) and (end_time_son == end_time):
        whole_boss_img = boss_img.copy()
        whole_boss_name = boss_name
        count_leftrigt += 1
        step_length = 2
    else:
        y1 = int(int((start_time_son - start_time).total_seconds())/(24*60*60/unit_day_height))
        y2 = int(int((end_time_son - start_time).total_seconds())/(24*60*60/unit_day_height))

        # 画每个小圆角矩形、角落魔法阵、中间横线
        draw_foreground.rounded_rectangle((217, 500+y1, 1104, 500+y2-6), radius=24, fill=fill_color, outline=outline_color, width=5)
        if (y2-6-y1) < 158:
            decoration_img = decoration_img.crop((0, 158-(y2-5-y1), 268, 158))
            decoration_layer.paste(decoration_img, (217+620, 500+y1), decoration_img)
        else:
            decoration_layer.paste(decoration_img, (217+620, 500+y2-6-157), decoration_img)
        # ↑根据decoration_img的尺寸粘贴, 如何让元组相加减?或者以size.img[0]的方式?
        line_layer.paste(line_img, (569, 500 + int((y1+y2)/2)-3), )
        draw_boss_mask.rounded_rectangle((217+8, 500+y1+8, 217+8+159, 500+y2-6-8), radius=16, fill=fill_color)
        whole_boss_img_copy = whole_boss_img.crop((0, int(0.5*(304+y1-y2)), 160, int(0.5*(274-y1+y2))))
        boss_layer.paste(whole_boss_img_copy, (217+8, 500+y1+8), whole_boss_img_copy)
        draw_text.text((620, 500 + int((y1+y2)/2)-3-54), whole_boss_name, font=ft37, fill=text_color)
        if count_leftrigt % 2 == 0:
            boss_img_copy = boss_img.crop((0, int(0.5*(304+y1-y2)), 160, int(0.5*(274-y1+y2))))
            boss_layer.paste(boss_img_copy, (217+8, 500+y1+8), boss_img_copy)
        else:
            draw_boss_mask.rounded_rectangle((217+8+168, 500+y1+8, 217+8+159+168, 500+y2-6-8), radius=16, fill=fill_color)
            boss_img_copy = boss_img.crop((0, int(0.5*(304+y1-y2)), 160, int(0.5*(274-y1+y2))))
            boss_layer.paste(boss_img_copy, (217+8+168, 500+y1+8), boss_img_copy)

    count_leftrigt += step_length

blank_layer.paste(decoration_layer, (0, 0), foreground_layer)
decoration_layer = blank_layer.copy()
blank_layer = Image.new('RGBA', background_layer.size, (255, 255, 255, 0))
shadow_layer = Image.new('RGB', background_layer.size, '#000000')
blank_layer.paste(shadow_layer, (0, 0), foreground_layer)
shadow_layer = blank_layer.copy()
blank_layer = Image.new('RGBA', background_layer.size, (255, 255, 255, 0))
shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(4))

background_layer.paste(shadow_layer, (0, 0), shadow_layer)
background_layer.paste(foreground_layer, (0, 0), foreground_layer)
background_layer.paste(decoration_layer, (0, 0), decoration_layer)
background_layer.paste(line_layer, (0, 0), line_layer)
background_layer.paste(boss_layer, (0, 0), boss_mask_layer)
background_layer.paste(text_layer, (0, 0), text_layer)

background_layer = background_layer.convert('RGB')
background_layer.save(r"data/wf_schedule/test2.png")
shadow_layer.save(r"data/wf_schedule/shadow_layer.png")
foreground_layer.save(r"data/wf_schedule/foreground_layer.png")
boss_mask_layer.save(r"data/wf_schedule/boss_mask_layer.png")
boss_layer.save(r"data/wf_schedule/boss_layer.png")
text_layer.save(r"data/wf_schedule/text_layer.png")
background_layer.show()
