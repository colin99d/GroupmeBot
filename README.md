# GroupmeBot

This is the GroupmeBot. Once added to a group it allows allows people to interact with it through messages.

To function you need to create a .env file in the main directory and set the following variables:

BIBLE_API_KEY=var1
ESPN_leagueID=var2
ESPN_SWID=var3
ESPN_S2=var4
GROUPME_TOKEN=var5
MAIN_GROUP_ID=var6
MAIN_GROUP_BOT=var7
TEST_GROUP_ID=var8
TEST_GROUP_BOT=var9

var1: Go to https://docs.api.bible/ and create an application. Enter the key as var1

Then go to ESPN and and go to the overview page for the leage you want to use for the bot. From there get the following variables:
var2: Look at the url for the current page. This value is the number after '?leagueId='

Before getting the next two variables go to inspect element and then select console. In the browser console paste the following code: function getCookie(name) {const value = `; ${document.cookie}`;const parts = value.split(`; ${name}=`);if (parts.length === 2) return parts.pop().split(';').shift();}
var 3: Enter getCookie("SWID") into the console. Include the '{}'
var 4: Enter getCookie("espn_s2") into the console

Next go to https://dev.groupme.com/ and create an account.
var5: click on the 'Access Token' button on the top of your account

Create the main bot at: https://dev.groupme.com/bots/new, then navigate to: https://dev.groupme.com/bots
var6: The Group ID column
var7: The Bot ID column

If you want a second bot to test commands before using them in the main chat create another bot.
var8: The Group ID column
var9: The Bot ID column
