from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import json
import socket
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    a=((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])
    update.message.reply_text(a)
    
def echo(bot, update): 
    ID = str(update.message.text)
    token = "Your token"
    a  = "curl -X GET --header 'Accept: application/json' --header"+ ' "authorization: Bearer '+token+ "\" 'https://api.clashofclans.com/v1/clanwarleagues/wars/%s'"%("%23"+ID)
    a = os.popen(a).readlines()
    a = a[0]
    a = json.loads(a)
    response = ""
    response += ("Status: "+a["state"]+"\n")
    response += ("clan name: "+a["clan"]["name"]+"\n")
    response += ("attacks: "+str(a["clan"]["attacks"])+"\n")
    response += ("stars:"+str(a["clan"]["stars"])+"\n")
    response += ("Destruction percentage "+str(a["clan"]["destructionPercentage"])+"\n")
    for i in a["clan"]["members"]:
        response += "\n"
        response += ("attacker: "+i["name"]+"\n")
        try:
            for j in i["attacks"]:
                for k in j:
                    if k == "attackerTag" or k == "defenderTag" or k=="order":
                        continue
                    response += (k+": "+str(j[k])+"\n")
        except KeyError:
            response += "Not in war or has not attacked yet\n"
            continue
    update.message.reply_text(response)

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Send the war tag to get current war info')

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("Event handler token")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
