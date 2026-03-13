<h1 align="center">
    <img src="../images/ralsei.png" alt="Ralsei Bot">
</h1>

# Ralsei Bot
Ralsei bot (or RB for short) is a fun Discord bot written in Python. It’s a small multi-use bot made for mostly experimentation. It has some basic features like a counting game, a simple EXP system, etc 

# Requirements 
if you wanna use Ralsei bot as a sort of template, you need the following:
* Python 3.8 or greater,
* And a Discord bot token which you can get at the [Discord Dev Portal](https://discord.com/developers/applications) 

Make sure the your bot has permission to read messages, send, and manage interactions in the guild.

# Project layout
This is the entire project layout (if you don't count the pycache)
```
ralsei-bot/
    |
    |
    main.py (The main file where the bot runs)
    |
    |
    |db/
    | |
    | |
    | __init__.py (Makes db/ a package so it cogs can connect to it)
    | |
    | |
    | setup.sql (Where it creates the Database tables)
    | |
    | |
    | connection.py (The place where the cogs connect to the DB)
    |
    |cogs/
    | |
    | |
    | ... (Usually where all the cogs are stored like ai.py, count.py, etc)
    |
    |docs/
    | |
    | |
    | |
    | ... (Beuh do you need to see this -_-)
    |
    |
    |images/
      ... (Contains all media needed for docs or a dashboard. Currently only having ralsei.png)
    |
    |
    /

```

# Installation
To install Ralsei bot, you must clone the repo and install it's dependencies 
```bash
git clone https://github.com/theoriginalralsei/ralsei-bot.git
cd ralsei-bot
pip install discord asyncio dotenv aiosqlite torch 
```

Then do the following:
1. Create a `.env` file
2. Add a `TOKEN` key in that file containing your bot token

# Setup
After installation, configure the bot for your server:

1. **Invite the bot** to your server with the required permissions (read messages, send messages, manage interactions)
2. **Set up the counting channel** (optional):
   - Add a row to the `server` table with your `guild_id` and `counting_channel` ID
3. **Start the bot**:
   ```bash
   python main.py
   ```

# Features
Ralsei Bot includes the following features:

- **Counting Game**: A server-wide counting game with math expression support
- **EXP System**: Earn experience by sending messages, with level-ups and leaderboards
- **Currency System**: Gamble with coins using games like coinflip and dice
- **AI Text Generation**: Generate text using GPT-2 ( I know it's only GPT-2 but c'mon- )
- **Fun Commands**: 8ball, scream, speak, and more
- **Actions**: Hug, kiss, headpat, and slap other users
- **User Stats**: View your EXP and currency balance
- **Admin Tools**: Moderation commands (purge, kick, ban)

# Commands

## General
| Command | Description | Aliases |
|---------|-------------|---------|
| `r:stats` | View your EXP and currency | - |
| `r:leaderboard` | View server EXP leaderboard | - |
| `/8ball <question>` | Ask Ralsei a question | Slash command |
| `r:scream` | Scream really loud | `s`, `scream` |
| `r:speak <message>` | Make Ralsei speak | `sp`, `speak` |


> [!CAUTION]
> 8Ball's responses are broken since the UTDR Text Box Generator's Hotlinks are disabled temporarily

## Currency
| Command | Description | Aliases |
|---------|-------------|---------|
| `r:coinflip <bet>` | Bet on heads or tails | `cf` |
| `r:dice <bet> <guess>` | Guess a number 1-6 | `di` |
| `r:daily` | Claim daily reward (10-90 currency) | - |

## Actions (Slash Commands)
| Command | Description |
|---------|-------------|
| `/action hug <member>` | Hug someone |
| `/action kiss <member>` | Kiss someone |
| `/action headpat <member>` | Headpat someone |
| `/action slap <member>` | Slap someone |

## AI
| Command | Description |
|---------|-------------|
| `/ai <prompt>` | Generate text with AI (max 1000 chars) |

## Admin (Moderator Only)
| Command | Description |
|---------|-------------|
| `r:show_members` | List all server members |
| `r:purge <amount>` | Delete messages |
| `r:kick <member> [reason]` | Kick a member |
| `r:ban <member> [reason]` | Ban a member |


# To-do
Currently trying to work on:

    - [ ] An Inventory system for currency

    - [ ] A dashboard/website

    - [ ] Idk maybe you'll give me ideas

# Contributing
Contributions Guidelines can be found [here](docs/CONTRIBUING.md)

# License
This project is under the [MIT License](docs/LICENSE.md)

## Note: 
Ralsei bot is not affiliated with Toby Fox. Ralsei is not my OC.
