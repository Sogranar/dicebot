import discord
import random
import pickle as pkl
import numpy as np
import os
from dotenv import load_dotenv


load_dotenv(verbose=True)



client = discord.Client()

# каждый кубик атаки и силы представляет собой список из 6 массивов, каждый из которых отражает одну грань, где первое значение массива - дальность, второе - урон, третье - заряды
blue = [[0,0,0],[2,2,1],[3,2,0],[4,2,0],[5,1,0],[6,1,1]]

green = [[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[1,1,1]]
yellow = [[1,1,0],[1,0,1],[2,1,0],[0,2,0],[0,1,1],[0,2,1]]
red = [[0,1,0],[0,2,0],[0,2,0],[0,2,0],[0,3,0],[0,3,1]]

brown = [0,0,0,1,1,2]
gray = [0,1,1,1,2,3]
black = [0,2,2,2,3,4]

# файл статистики содержит список из 7 массивов, каждый из которых относится к одному из кубиков в порядке того, как они перечислены выше (т.е синий, зеленый и т.д)
# отдельные элементы каждого массива показывают количество бросков соответствующих им граней кубика, также в том порядке, как эти грани перечислены для каждого кубика выше
# таким образом значение списка stat[2][5] отражает общее количество бросков шестой грани для желтого кубика
stat_input = open('stat.pkl', 'rb')
stat = pkl.load(stat_input)
stat_input.close()


#def result_print(color, color_text, stat_number, mess):
#    i = 0
#    d = random.randint(0,5)
#    if np.sum(color[d]) == 0 : await mess.channel.send(':regional_indicator_x: (miss)')
#    await mess.channel.send(':{}_square: B: {} :archery: + {} :heart: + {} :zap:'.format(color_text,color[d][0],color[d][1],color[d][2]))

def att_sum(sum, dice, corner):
    i = 0
    while i < 3:
        sum[i] += dice[corner][i]
        i += 1
    return sum

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.name != 'bots':
        return

#    if message.author.name == 'Хаёши':
#        await message.channel.send('Hello, creator!')

    global stat
    stat_output = open('stat.pkl', 'wb')
    att_total = [0,0,0]
    def_total = 0
    blue_count = 0
    blue_error = 0
    die_pool = message.content
    die_pool = die_pool.split(' ')
    for dice in die_pool:
        if ((dice == 'blue') | (dice == 'b') | (dice == 'с')):
            i = 0
            if (blue_count == 1) :
                if (blue_error == 0) : await message.channel.send(':exclamation: You can only use one blue die in a single throw!')
                blue_error += 1
                continue
            blue_count += 1
            d = random.randint(0,5)
            stat[0][d] += 1
            if (d == 0) : await message.channel.send(':regional_indicator_x: (miss)')
            elif (die_pool[0] != 'hide') : await message.channel.send(':blue_square: B: {} :archery: + {} :heart: + {} :zap:'.format(blue[d][0],blue[d][1],blue[d][2]))
            att_total = att_sum(att_total, blue, d)
            continue

        elif ((dice == 'green') | (dice == 'g') | (dice == 'з')):
            i = 0
            d = random.randint(0,5)
            stat[1][d] += 1
            if (die_pool[0] != 'hide') : await message.channel.send(':green_square: G: {} :archery: + {} :heart: + {} :zap:'.format(green[d][0],green[d][1],green[d][2]))
            att_total = att_sum(att_total, green, d)
            continue

        elif ((dice == 'yellow') | (dice == 'y') | (dice == 'ж')):
            i = 0
            d = random.randint(0,5)
            stat[2][d] += 1
            if (die_pool[0] != 'hide') : await message.channel.send(':yellow_square: Y: {} :archery: + {} :heart: + {} :zap:'.format(yellow[d][0],yellow[d][1],yellow[d][2]))
            att_total = att_sum(att_total, yellow, d)
            continue

        elif ((dice == 'red') | (dice == 'r') | (dice == 'к')):
            i = 0
            d = random.randint(0,5)
            stat[3][d] += 1
            if (die_pool[0] != 'hide') : await message.channel.send(':red_square: R: {} :archery: + {} :heart: + {} :zap:'.format(red[d][0],red[d][1],red[d][2]))
            att_total = att_sum(att_total, red, d)
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
               stat = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
               #pkl.dump(stat, stat_output, 2)
               #stat_output.close()
               await message.channel.send('All statistics succesfully wiped!')

    if att_total != [0,0,0]: await message.channel.send('Total: {} :archery: + {} :heart: + {} :zap:'.format(att_total[0],att_total[1],att_total[2]))
    if def_total != 0 : await message.channel.send('Total: {} :shield:'.format(def_total))

    pkl.dump(stat, stat_output, 2)
    stat_output.close()

client.run(os.getenv("DISCORD_CLIENT_KEY"))
