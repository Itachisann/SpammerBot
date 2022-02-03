# Spammer Userbot

Fully async userbot built using the basics of [TG-Userbot][tguserbot] based on [Telethon][telethon] library

# 

## Requirements:

* Python 3.7.3 or above.
* Optional Telegram [API Key][tg-apps] (App ID and App Hash).

## How to install:

Clone the repository on your self host and open the new directory.

```sh
$ git clone https://github.com/Itachisann/SpammerBot && cd SpammerBot
```

> (Optional) Edit the config.ini using Nano or a text Editor and put your APP ID and APP HASH.
```sh
$ nano config.ini
```

Install all the requirements using pip.

```sh
$ pip3 install --user -r requirements.txt
```

Run the userbot and have fun!

```sh
$ python3 -m userbot
```
# 

## Developing
* You need to have an account or VoIP, and set ChatID of these groups in [Spam.py][spam]

# 
## Inspiration and Credits:

* [TG-Userbot][tguserbot]
* [Telethon][telethon]
* [ThunderUserbot](https://github.com/Thundergang)

## Copyright & License

- Copyright (C) 2021 [Itachisann](https://github.com/Itachisann).
- Licensed under the terms of the [GNU General Public License v3.0 or later (GPLv3+)](LICENSE).


































[//]: # (Comment)
   [telethon]: <https://github.com/LonamiWebs/Telethon/>
   [tguserbot]: <https://github.com/TG-UserBot/TG-UserBot>
   [tg-apps]: <https://my.telegram.org/apps>
   [spam]: <https://github.com/Itachisann/SpammerBot/blob/main/userbot/plugins/spam.py#:~:text=spam_val%20%3D%20False-,array_groups_id,-%3D%20%5B%2D1001488898663%2C%20%2D1001230649113%2C%20%2D1001189316065>
