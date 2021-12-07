# GroupmeBot

This is the GroupmeBot. Once added to a group it allows allows people to interact with it through messages.

## Setup

To function you need to create a .env file in the main directory and set the following variables:

- BIBLE_API_KEY=var1
- ESPN_leagueID=var2
- ESPN_SWID=var3
- ESPN_S2=var4
- GROUPME_TOKEN=var5
- MAIN_GROUP_ID=var6
- MAIN_GROUP_BOT=var7
- TEST_GROUP_ID=var8
- TEST_GROUP_BOT=var9
- SQLALCHEMY_DATABASE_URI=var10

var1: Go to https://docs.api.bible/ and create an application. Enter the key as var1

Then go to ESPN and and go to the overview page for the leage you want to use for the bot. From there get the following variables:
- var2: Look at the url for the current page. This value is the number after '?leagueId='

Before getting the next two variables go to inspect element and then select console. In the browser console paste the following code: function getCookie(name) {const value = `; ${document.cookie}`;const parts = value.split(`; ${name}=`);if (parts.length === 2) return parts.pop().split(';').shift();}
- var 3: Enter getCookie("SWID") into the console. Include the '{}'
- var 4: Enter getCookie("espn_s2") into the console

Next go to https://dev.groupme.com/ and create an account.
- var5: click on the 'Access Token' button on the top of your account

Create the main bot at: https://dev.groupme.com/bots/new, then navigate to: https://dev.groupme.com/bots
- var6: The Group ID column
- var7: The Bot ID column

If you want a second bot to test commands before using them in the main chat create another bot.
- var8: The Group ID column
- var9: The Bot ID column

var10: This is the URI for the database. Either copy and paste the Heroku database URI or use: sqlite:////tmp/test.db for local development

## Running Server
This program uses Flask. To start the app type `flask run`
**Note**: To always start the flask run in development run add `FLASK_ENV=development1` to your .env file

To apply any changes made to your database run `flask db upgrade`

## Testing
To use Pytest run `pytest tests/`

If you would like to see a coverage report use the following steps:
1. Run `coverage run -m pytest`
2. Run `coverage html`
3. Go to htmlcov/index.html and open the file
