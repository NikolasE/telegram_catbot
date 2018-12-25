# Telegram Bot

This demo uses python-telegram-bot with python3 to create a simple chatbot that stores some information abouts its 
usage in a postgresql-Database. It is primarily meant as a playground to explore new technologies and contains notes
for info I found while developing the demo. 

The bot can be found at [CatBot2000_bot](t.me/CatBot2000_bot).



It's a showcase for several features:

### Features

**Ask user for Location**

Only works on smartphone, bot gets lng/lat via GPS (after user clicked on button)


**Let user select one of multiple Options**

Use customized buttons to let user select one from multiple options

**Send image**

Send an image to user user (e.g. a rendered map or a cat image)

**Store information in a Database**

Use django as a database-interface to store some data (currently first names of users).

**Deploy on Heroku**

The catbot can be deployed on Heroku and uses Webhooks to receive messages.

**Send a cat image**

Most likely the most important capability of the app. It uses the [CatAPI](https://thecatapi.com/) from 
[That Api Guy: Aden Forshaw](https://thatapiguy.com/the-cat-api/). 


## Installation

run install.sh to install library to .local/ with pip3

## Run

App can be run locally with polling or on a server (e.g. [Heroku](http://heroku.com))


### Demo Program

To be found at [scripts/tele_bot.py](scripts/tele_bot.py):

**Commands**

- /help
- /options
- /location
- /cat

## TODO:
- Emoji: https://apps.timwhitlock.info/emoji/tables/unicode
- Inline-Modus
- add Flask 


### Telegram-Bot

Talk to the [Bot-Father](https://core.telegram.org/bots) to create your own chatbot and create a new token. Put this token
in a newly created file secret_chat_key.py so that the file looks like 

```TELEGRAM_TOKEN= '7970:AAGPbRtXlyShF...'```
or put it into an environment variable. 


### Django ###
- django-admin startproject django_cat_project
- python3 manage.py startapp django_cat_app
- Add Models in [django_cat_app/models.py](django_cat_app/models.py)
- ```DJANGO_SETTINGS_MODULE=django_cat_project.settings```, Add directory to ```$PYTHONPATH```
- Configure DB for local and remove usage:
    - check [django_cat_project/settings.py](django_cat_project/settings.py):
        - replace sqlite with postgresql
        - set database name (e.g. cat_db)
        - createdb cat_db (make sure that there is a psql-user with your login-name)
        - add to end of file: 
            ```STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
            STATIC_URL = "/static/"
            import django_heroku
            django_heroku.settings(locals()) ```
        - normal db stuff:
            ```manage.py makemigrations && manage.py migrate```
        - use pgadmin3 or similar to check local db
    

### Install on Heroku

[Setup Heroku for python](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)

- activate CLI, add new app, add new remote (e.g. heroku master) for local git

- git push heroku master
- set environment variables on heroku (e.g. telegram_token): [Heroku Config-Vars](https://devcenter.heroku.com/articles/config-vars)

   ```heroku config:set WITH_HOOK=1 DJANGO_SETTINGS_MODULE=django_cat_project.settings TELEGRAM_TOKEN=797....```

- These [CLI-commands](https://devcenter.heroku.com/articles/heroku-cli-commands)
 work locally in the project-directory, elsewhere, add '--app your_app_name'. 
    - Start dyno: ```heroku ps:scale web=1```
    - Restart dyno: ```heroku dyno:restart```
    - Logs: ```heroku logs --tail```
    - ssh into dyno: ```heroku ps:exec```
