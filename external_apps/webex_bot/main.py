"""

Hello! Getting this webex bot up-and-running just requires a few steps: 

1) Retrieve your WebEx API Dev Token and paste it into `dev_token` (line 46)
    - This can be found at: https://developer.webex.com/docs/getting-started

2) Install the ncessary packages: 
    - pip install webex_bot
    - pip install webexteamssdk

    * elasticsearch 7.13.4 was used, which worked well * 
    * other version of elasticsearch have NOT been tested * 

    - Other requirements: pandas, tqdm, transformers, torch, huggingface-hub

3) Create a WebEx Bot by first navigating to https://developer.webex.com/docs/bots
    - Next, click on the blue button titled "Create a Bot"
    - Enter a unique Bot name, username, icon, and description 
    - Continue by clicking the blue button at the bottom of the page
    - Copy the "Bot access token" that is shown and paste into `bot_token` (line 43)

4) Ensure Elasticsearch 7.13.4 is running on your system 

5) Run `python main.py` 

5) Navigate to WebEx, and find your bot (using its unique name)

6) Type "help" to see a list of supported commands 

7) Experiment with commands such as "snapshot, search <query>, answer <query> and summarize"

* AS OF NOW, THIS BOT WILL ONLY BE ABLE TO ACCESS TRANSCRIPTS WITHIN THE LAST 5 DAYS * 
* CURRENTLY, HAS ONLY BEEN TESTED WITH 6 DIFFERENT TRANSCRIPTS, EACH ROUGHLY 2 - 3 MIN LONG * 
  (Unsure as to how this will scale with more/longer transcripts --> please keep in mind!)


"""

from webex_bot.webex_bot import WebexBot
from cmds import  SummarAcross,  EmptySpace, SearchAcross, ListTranscripts, Actionables, Panoptica
from help import LoadTranscripts, InitilizeTranscripts
from external_apps.panoptica_utils.panoptica_utils import RunFunction, InitilizeSwaggerFunctions, GetAPIKeys

from constants import CONSTANTS
import requests


# THIS LINE WILL NEED TO CHANGE BASED ON YOUR URL SERVER HOSTED!
config = requests.get('http://localhost:3000/config').json().get("response")
bot_token = config.get("WEBEX_BOT_TOKEN")
print(bot_token)

transcriptsFileName = "webex_transcripts.json"
InitilizeTranscripts(transcriptsFileName)
functions = InitilizeSwaggerFunctions()
bot = WebexBot(bot_token)

bot.add_command(EmptySpace())
bot.add_command(ListTranscripts())
bot.add_command(SummarAcross(transcriptsFileName))
bot.add_command(SearchAcross(transcriptsFileName))
bot.add_command(Actionables(transcriptsFileName))
bot.add_command(Panoptica(functions))


bot.run() 