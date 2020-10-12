# dicebot
Discord Descent utility bot v0.1

## Installation:

Rename .env.template -> .env

Then add your bot client key to .env

Rename stat.pkl.template -> stat.pkl

It is where throw statistics will be stored 

Now you can run the bot with *python dice-bot.py*

## Usage:

Bot can roll dice, reacting to any messages with keywords in **#bots** channel. 

Keywords can be separated with spaces for throwing multiple dice. Bot also supports cirillic

### Keyword list:

- blue/b/с - blue die

- green/g/з - green die

- yellow/y/ж - yellow die

- red/r/к - red die

- brown/br/зк - brown die

- gray/gr/зс - gray die

- black/bl/зч - black die

- check/t/т - attribute test (gray+black)

- hide - must be at start of a message, shows only total of entire throw

- blue-stat/green-stat/yellow-stat/etc - shows throw statistics of particular die


## To do list:

- [ ] Add unhide and re-roll options

- [ ] Add support for separate defense rolls in one message

- [ ] Some code optimization
