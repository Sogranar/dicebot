import discord
import random
import pickle as pkl
import numpy as np
import os
#import requests
import glob

from dotenv import load_dotenv
#from bs4 import BeautifulSoup

load_dotenv(verbose=True)

client = discord.Client()

# каждый кубик атаки и силы представляет собой список из 6 массивов, каждый из которых отражает одну грань, где первое значение массива - дальность, второе - урон, третье - заряды
blue = [[0,0,0],[2,2,1],[3,2,0],[4,2,0],[5,1,0],[6,1,1],'blue']

green = [[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[1,1,1],'green']
yellow = [[1,1,0],[1,0,1],[2,1,0],[0,2,0],[0,1,1],[0,2,1],'yellow']
red = [[0,1,0],[0,2,0],[0,2,0],[0,2,0],[0,3,0],[0,3,1],'red']

brown = [0,0,0,1,1,2]
gray = [0,1,1,1,2,3]
black = [0,2,2,2,3,4]

# файл статистики содержит список из 7 массивов, каждый из которых относится к одному из кубиков в порядке того, как они перечислены выше (т.е синий, зеленый и т.д)
# отдельные элементы каждого массива показывают количество бросков соответствующих им граней кубика, также в том порядке, как эти грани перечислены для каждого кубика выше
# таким образом значение списка stat[2][5] отражает общее количество бросков шестой грани для желтого кубика
stat_input = open('stat.pkl', 'rb')
stat = pkl.load(stat_input)
stat_input.close()

##to do throw and message as a separate class
def roll(dice):
    corner = random.randint(0,5)
    text = ':{}_square: {}: {} :archery: + {} :heart: + {} :zap:'.format(dice[6],dice[6][0].upper(),dice[corner][0],dice[corner][1],dice[corner][2])
    return corner,text

def att_sum(sum, dice, corner):
    i = 0
    while i < 3:
        sum[i] += dice[corner][i]
        i += 1
    return sum

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


#@client.event
#async def on_message(message):
#
#    command = message.content
#    command = command.split(' ')
#    if (command[0] == '!item') :
#        req = requests.get('https://descent2e.fandom.com/wiki/{}'.format(command[1]))
#        parse = BeautifulSoup(req.text, 'html.parser')
#        image = parse.find("meta", property="og:image").get("content")
#        await message.channel.send(image)
#    else : return



@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #if message.channel.name != 'bots':
    #    return

    global stat
    stat_output = open('stat.pkl', 'wb')
    att_total = [0,0,0]
    def_total = 0
    blue_count = 0
    blue_error = 0
    die_pool = message.content
    die_pool = die_pool.split(' ')
    command = die_pool

    if (command[0] == '!card') :
        i = 2
        img_name = command[1].lower()
        while i < len(command) :
            img_name += '-' + command[i].lower()
            i += 1
        path = './cards/**/{}.*'.format(img_name)
        if (glob.glob(path)) == [] : await message.channel.send('Nothing found')
        img_path = glob.glob(path)
        for img in [0, 1, 2, 3, 4]:
            if ((img_path[img] == './cards/lieutenants/baron-zachareth-act1.jpg') | (img_path[img] == './cards/agents/baron-zachareth-agent-act1.jpg')) : await message.channel.send('This is not even my final form!')
            if ((img_path[img] == './cards/lieutenants/baron-zachareth-act2.jpg') | (img_path[img] == './cards/agents/baron-zachareth-agent-act2.jpg')) : await message.channel.send('Tremble before me, pityfull heroes!')
            await message.channel.send(file=discord.File(img_path[img]))
        if (len(img_path) > 5): await message.channel.send('Too many results')

    if message.channel.name != 'bots': return

    for dice in die_pool:
        if ((dice == 'blue') | (dice == 'b') | (dice == 'с')):
            if (blue_count == 1) :
                if (blue_error == 0) : await message.channel.send(':exclamation: You can only use one blue die in a single throw!')
                blue_error += 1
                continue
            else : blue_count += 1
            corner, text = roll(blue)
            stat[0][corner] += 1
            if (corner == 0) : await message.channel.send(':regional_indicator_x: (miss)')
            elif (die_pool[0] != 'hide') : await message.channel.send(text)
            att_total = att_sum(att_total, blue, corner)
            continue

        elif ((dice == 'green') | (dice == 'g') | (dice == 'з')):
            corner, text = roll(green)
            stat[1][corner] += 1
            if (die_pool[0] != 'hide') : await message.channel.send(text)
            att_total = att_sum(att_total, green, corner)
            continue

        elif ((dice == 'yellow') | (dice == 'y') | (dice == 'ж')):
            corner, text = roll(yellow)
            stat[2][corner] += 1
            if (die_pool[0] != 'hide') : await message.channel.send(text)
            att_total = att_sum(att_total, yellow, corner)
            continue

        elif ((dice == 'red') | (dice == 'r') | (dice == 'к')):
            corner, text = roll(red)
            stat[3][corner] += 1
            if (die_pool[0] != 'hide') : await message.channel.send(text)
            att_total = att_sum(att_total, red, corner)
            continue

        elif ((dice == 'brown') | (dice == 'br') | (dice == 'зк')):
            d = random.randint(0,5)
            stat[4][d] += 1
            if (die_pool[0] != 'hide') : await message.channel.send(':brown_square: Br: {} :shield:'.format(brown[d]))
            def_total += brown[d]
            continue

        elif ((dice == 'gray') | (dice == 'gr') | (dice == 'зс')):
            d = random.randint(0,5)
            stat[5][d] += 1
            if (die_pool[0] != 'hide') : await message.channel.send(':white_large_square: Gr: {} :shield:'.format(gray[d]))
            def_total += gray[d]
            continue

        elif ((dice == 'black') | (dice == 'bl') | (dice == 'зч')):
           d = random.randint(0,5)
           stat[6][d] += 1
           if (die_pool[0] != 'hide') : await message.channel.send(':black_large_square: Bl: {} :shield:'.format(black[d]))
           def_total += black[d]
           continue

        elif ((dice == 'check') | (dice == 't') | (dice == 'т')):
           d = random.randint(0,5)
           stat[5][d] += 1
           if (die_pool[0] != 'hide') : await message.channel.send(':white_large_square: Gr: {} :shield:'.format(gray[d]))
           def_total += gray[d]
           d = random.randint(0,5)
           stat[6][d] += 1
           if (die_pool[0] != 'hide') : await message.channel.send(':black_large_square: Bl: {} :shield:'.format(black[d]))
           def_total += black[d]
           continue

        elif (dice == 'blue-stat'):
           i = 0
           await message.channel.send(':blue_square: Blue dice total - {} throws:'.format(np.sum(stat[0])))
           while i < 6:
               if i == 0 : await message.channel.send(':regional_indicator_x: (miss) - {} throws ({}% from total)'.format(stat[0][i],round(stat[0][i]/np.sum(stat[0])*100, 3)))
               else: await message.channel.send('{} :archery: + {} :heart: + {} :zap: - {} throws ({}% from total)'.format(blue[i][0],blue[i][1],blue[i][2],stat[0][i],round(stat[0][i]/np.sum(stat[0])*100, 3)))
               i += 1

        elif (dice == 'green-stat'):
           i = 0
           await message.channel.send(':green_square: Green dice total - {} throws:'.format(np.sum(stat[1])))
           while i < 6:
               await message.channel.send('{} :archery: + {} :heart: + {} :zap: - {} throws ({}% from total)'.format(green[i][0],green[i][1],green[i][2],stat[1][i],round(stat[1][i]/np.sum(stat[1])*100, 3)))
               i += 1

        elif (dice == 'yellow-stat'):
           i = 0
           await message.channel.send(':yellow_square: Yellow dice total - {} throws:'.format(np.sum(stat[2])))
           while i < 6:
               await message.channel.send('{} :archery: + {} :heart: + {} :zap: - {} throws ({}% from total)'.format(yellow[i][0],yellow[i][1],yellow[i][2],stat[2][i],round(stat[2][i]/np.sum(stat[2])*100, 3)))
               i += 1

        elif (dice == 'red-stat'):
           i = 0
           await message.channel.send(':red_square: Red dice total - {} throws:'.format(np.sum(stat[3])))
           while i < 6:
               await message.channel.send('{} :archery: + {} :heart: + {} :zap: - {} throws ({}% from total)'.format(red[i][0],red[i][1],red[i][2],stat[3][i],round(stat[3][i]/np.sum(stat[3])*100, 3)))
               i += 1

        elif (dice == 'brown-stat'):
           i = 0
           await message.channel.send(':brown_square: Brown dice total - {} throws:'.format(np.sum(stat[4])))
           while i < 6:
               await message.channel.send('{} :shield: - {} throws ({}% from total)'.format(brown[i],stat[4][i],round(stat[4][i]/np.sum(stat[4])*100, 3)))
               i += 1

        elif (dice == 'gray-stat'):
           i = 0
           await message.channel.send(':white_large_square: Gray dice total - {} throws:'.format(np.sum(stat[5])))
           while i < 6:
               await message.channel.send('{} :shield: - {} throws ({}% from total)'.format(gray[i],stat[5][i],round(stat[5][i]/np.sum(stat[5])*100, 3)))
               i += 1

        elif (dice == 'black-stat'):
           i = 0
           await message.channel.send(':black_large_square: Black dice total - {} throws:'.format(np.sum(stat[6])))
           while i < 6:
               await message.channel.send('{} :shield: - {} throws ({}% from total)'.format(black[i],stat[6][i],round(stat[6][i]/np.sum(stat[6])*100, 3)))
               i += 1

        if (dice == 'stat-wipe'):
           if message.author.name != 'Хаёши': await message.channel.send('No-no-no, you are not the Master!')
           else :
               #stat = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
               await message.channel.send('All statistics succesfully wiped!')

    if att_total != [0,0,0]: await message.channel.send('Total: {} :archery: + {} :heart: + {} :zap:'.format(att_total[0],att_total[1],att_total[2]))
    if def_total != 0 : await message.channel.send('Total: {} :shield:'.format(def_total))

    pkl.dump(stat, stat_output, 2)
    stat_output.close()



client.run(os.getenv("DISCORD_CLIENT_KEY"))
