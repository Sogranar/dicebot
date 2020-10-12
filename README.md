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

Also !card command allow to post images of almost all game cards. 

It's support partial name search, e.g '!card shadow dragon*' will post images of both shadow dragon cards from act1 and act2

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

### Available card categories:

- Heroes

- Class cards

- Items

- Relics

- Monsters

- OL and Plot decks

- Lieutenants and Agents

- Allies and their skills

- Familiars

- Rumors and Advanced quests

- Conditions

- Travel and City events decks

- Search and Secret rooms decks

- Tainted cards

- Corrupted citizens

## To do list:

- [ ] Add unhide and re-roll options

- [ ] Add support for separate defense rolls in one message

- [ ] Some code optimization

## Special thanks

@Kisho (and all other members) from Descent: Journeys in the Dark discord server for ideas, testing and help

d2e (https://github.com/any2cards/d2e) repo creator and contributors for all the cards images
