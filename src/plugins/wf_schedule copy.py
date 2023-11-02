import json
# import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import datetime


def readFileJson(file_name):
    # 包一下读取json
    with open(file_name, "r", encoding="UTF-8") as f:
        data = json.load(f)
    return data


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
    if item == "20":
        pu_number = item
        break


description_text = [
    f"{start_time.strftime('%Y年%m月%d日%H:%M')}~{end_time.strftime('%Y年%m月%d日%H:%M')}",
    "活动期间以协力战斗挑战特选对象领主",
    f"可获得的领主币、经验值和玛纳将变为{multiplier}倍!"]

duration = (end_time.date() - start_time.date()).days + 1  # 活动持续时间

background_layer = Image.new('RGBA', (1170, 470 + unit_day_height * duration), (255, 255, 255, 0))

head_img = Image.open(r'data/wf_schedule/sprite_sheet/head.png')
body_img = Image.open(r'data/wf_schedule/sprite_sheet/body.png').resize((1170, -42 + unit_day_height * duration))
foot_img = Image.open(r'data/wf_schedule/sprite_sheet/foot.png')

background_layer.paste(head_img, (0, 0),)
background_layer.paste(body_img, (0, 256),)
background_layer.paste(foot_img, (0, 214 + unit_day_height * duration))

draw_background = ImageDraw.Draw(background_layer)
ft37 = ImageFont.truetype(r"data/wf_schedule/SY.ttf", 37)
ft36 = ImageFont.truetype(r"data/wf_schedule/SY.ttf", 36)
ft33 = ImageFont.truetype(r"data/wf_schedule/SY.ttf", 33)
ft30 = ImageFont.truetype(r"data/wf_schedule/SY.ttf", 30)
gray_color = "#525252"
orange_color = "#FF9933"
draw_background.text((96, 256), description_text[0], font=ft37, fill=gray_color)
draw_background.text((96, 320), description_text[1], font=ft37, fill=gray_color)
draw_background.text((96, 368), description_text[2], font=ft37, fill=gray_color)
draw_background.text((291, 320), description_text[1][5:9], font=ft37, fill=orange_color)
draw_background.text((252, 368), description_text[2][4:-1], font=ft37, fill=orange_color)


line_img = Image.open(r"data/wf_schedule/sprite_sheet/line.png").convert('RGBA')
draw_start_time = start_time

for i in range(0, duration):
    if i < duration - 1:
        background_layer.paste(line_img, (57, 570 + unit_day_height*i), line_img)
    draw_background.text((56, 466 + unit_day_height*i), draw_start_time.strftime('%m月%d日'), font=ft33, fill=gray_color)
    draw_start_time += datetime.timedelta(days=1)

decoration_white_img = Image.open(
    r'data/wf_schedule/sprite_sheet/bottom_right_decoration_white.png').convert('RGBA')
decoration_purple_img = Image.open(
    r'data/wf_schedule/sprite_sheet/bottom_right_decoration_purple.png').convert('RGBA')
line_white = Image.open(
    r'data/wf_schedule/sprite_sheet/line_white.png').convert('RGBA')
line_purple = Image.open(
    r'data/wf_schedule/sprite_sheet/line_purple.png').convert('RGBA')

blank_layer = Image.new('RGBA', background_layer.size, (255, 255, 255, 0))
shadow_layer = Image.new('RGB', background_layer.size, '#000000')
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
time_origin_list = []
time_distinct_list = []
time_list = []
for item in boss_battle_multi_pickup_event_schedule[pu_number]:
    start_time_son = datetime.datetime.strptime(boss_battle_multi_pickup_event_schedule[pu_number][item][6], '%Y-%m-%d %H:%M:%S')
    end_time_son_plus = datetime.datetime.strptime(boss_battle_multi_pickup_event_schedule[pu_number][item][7], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds=1)
    time_origin_list.append(start_time_son)
    time_origin_list.append(end_time_son_plus)
[time_distinct_list.append(x) for x in time_origin_list if x not in time_distinct_list]
time_list = sorted(time_distinct_list)
for i in range(0, len(time_list)-1):
    if (current_time >= time_list[i]) and (current_time <= time_list[i+1]-datetime.timedelta(seconds=1)):
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
    y1 = int((time_list[i] - start_time).total_seconds()/(24*60*60/unit_day_height))
    y2 = int((time_list[i+1] - start_time).total_seconds()/(24*60*60/unit_day_height)) - 8
    # 画每个小圆角矩形、boss图蒙版、角落魔法阵、中间横线、日期
    draw_foreground.rounded_rectangle((217, 500+y1, 1104, 500+y2), radius=24, fill=fill_color, outline=outline_color, width=5)
    draw_boss_mask.rounded_rectangle((217+8, 500+y1+8, 217+8+159, 500+y2-8), radius=16, fill=fill_color)
    draw_boss_mask.rounded_rectangle((217+8+159+8, 500+y1+8, 217+8+159+159+8, 500+y2-8), radius=16, fill=fill_color)
    if (y2-y1) < 158:
        decoration_img = decoration_img.crop((0, 157-(y2-y1), 268, 159))
        decoration_layer.paste(decoration_img, (217+620, 500+y1), decoration_img)
    else:
        decoration_layer.paste(decoration_img, (217+620, 500+y2-157), decoration_img)
    line_layer.paste(line_img, (565, 500+int((y1+y2)/2)), )
    draw_text.text((569, 489+int((11*y1+13*y2)/24)), f"{time_list[i].strftime('%m月%d日%H:%M')} ~ {(time_list[i+1]-datetime.timedelta(seconds=1)).strftime('%m月%d日%H:%M')}", font=ft30, fill=text_color)

left_list = [0]*(len(time_list)-1)
bossimg_delta_abscissa = 0
for item in boss_battle_multi_pickup_event_schedule[pu_number]:
    # 提审thumbnail
    boss_number = boss_battle_multi_pickup_event_schedule[pu_number][item][1]
    boss_name = boss_battle_quest["1"][boss_number]["1"][2].split()[0]
    print(boss_name)
    boss_img_filename = boss_battle_quest["1"][boss_number]["1"][3]
    boss_img = Image.open(f"data/{boss_img_filename}.png")
    # 提取时间
    start_time_son = datetime.datetime.strptime(boss_battle_multi_pickup_event_schedule[pu_number][item][6], '%Y-%m-%d %H:%M:%S')
    end_time_son = datetime.datetime.strptime(boss_battle_multi_pickup_event_schedule[pu_number][item][7], '%Y-%m-%d %H:%M:%S')

    for j in range(0, len(time_list)-1):
        y1 = int((time_list[j] - start_time).total_seconds()/(24*60*60/unit_day_height))
        y2 = int((time_list[j+1] - start_time).total_seconds()/(24*60*60/unit_day_height)) - 8

        if (start_time_son <= time_list[j]) and (end_time_son >= time_list[j+1]-datetime.timedelta(seconds=1)):
            if left_list[j] == 0:
                bossimg_delta_abscissa = 0
                bossname_delta_abscissa = 0
                left_list[j] = 1
            elif left_list[j] == 1:
                bossimg_delta_abscissa = 160 + 8
                bossname_delta_abscissa = 250
                left_list[j] = 2
            elif left_list[j] == 2:
                print(f"太酷了, 在{time_list[j]}到{time_list[j+1]}这段时间有3个up")
            boss_img_copy = boss_img.crop((0, int((304+y1-y2)/2), 160, int((274-y1+y2)/2)))
            boss_layer.paste(boss_img_copy, (217+8+bossimg_delta_abscissa, 500+y1+8), boss_img_copy)
            draw_text.text((570+bossname_delta_abscissa, 446+int((13*y1+11*y2)/24)), boss_name, font=ft36, fill=text_color)


blank_layer.paste(decoration_layer, (0, 0), foreground_layer)
decoration_layer = blank_layer.copy()
blank_layer = Image.new('RGBA', background_layer.size, (255, 255, 255, 0))
blank_layer.paste(shadow_layer, (0, 0), foreground_layer)
shadow_layer = blank_layer.copy()
blank_layer = Image.new('RGBA', background_layer.size, (255, 255, 255, 0))
shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(4))

background_layer.paste(shadow_layer, (0, 0), shadow_layer)
background_layer.paste(foreground_layer, (0, 0), foreground_layer)
background_layer.paste(decoration_layer, (0, 0), decoration_layer)
background_layer.paste(line_layer, (0, 0), line_layer)
background_layer.paste(boss_mask_layer, (0, 0), boss_mask_layer)
background_layer.paste(boss_layer, (0, 0), boss_mask_layer)
background_layer.paste(text_layer, (0, 0), text_layer)

background_layer = background_layer.convert('RGB')
background_layer.save(f"data/wf_schedule/{code_name}.png")
shadow_layer.save(r"data/wf_schedule/layer/shadow_layer.png")
foreground_layer.save(r"data/wf_schedule/layer/foreground_layer.png")
boss_mask_layer.save(r"data/wf_schedule/layer/boss_mask_layer.png")
boss_layer.save(r"data/wf_schedule/layer/boss_layer.png")
text_layer.save(r"data/wf_schedule/layer/text_layer.png")
background_layer.show()
