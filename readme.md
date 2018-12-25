# Telegram Bot

This demo uses python-telegram-bot with python3 to create a simple chatbot with the following features:

### Features

**Ask user for Location**

Only works on smartphone, bot gets lng/lat via GPS (after user clicked on button)


**Let user select one of multiple Options**

Use customized buttons to let user select one from multiple options

**Send image**

Send an image to user user (e.g. a rendered map or a cat image)


## Installation

run install.sh to install library to .local/ with pip3

## Run

App can be run locally with polling or on server (with_webhoks=True)


### Demo Program

To be found at KreathonBot

**Commands**

- /start
- /help
- /options
- /location
- /cat

django-admin startproject django_cat_project
## TODO:
- Emoji: https://apps.timwhitlock.info/emoji/tables/unicode
- Inline-Modus

# Heroku

The app can be deployed on [Heroku](heroku.com):

### Install Heroku

[Setup Heroku for python](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)

- https://devcenter.heroku.com/articles/config-vars
- heroku ps:scale web=1

- heroku config:set WITH_HOOK=1 DJANGO_SETTINGS_MODULE=DJANGO_SETTINGS_MODULE TELEGRAM_TOKEN=797....
- heroku dyno:restart

#### Heroku-CLI
[All CLI-commands](https://devcenter.heroku.com/articles/heroku-cli-commands)

## Postgresql-Database

django-admin startproject django_cat_project

        
