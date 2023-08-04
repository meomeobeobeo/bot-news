from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from getnews import getNewsVNEXPRESS
from getnews import getNewsDANTRI
import logging
import logging
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from getnews import getNewsVNEXPRESS, getNewsDANTRI

# Configure logging to save errors to a file with timestamp
logging.basicConfig(
    filename='log.txt',
    level=logging.ERROR
)

# Create a custom logging formatter to include the timestamp
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Create a FileHandler with the custom formatter
file_handler = logging.FileHandler('log.txt')
file_handler.setFormatter(formatter)

# Add the FileHandler to the root logger
logging.getLogger().addHandler(file_handler)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text(f'Xin chào {update.effective_user.first_name}')
    except Exception as e:
        logging.error(f"Error in 'hello' command: {str(e)}")


async def vnex(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        listNews = getNewsVNEXPRESS()
        print(listNews)
        countNews = f'Có tổng cộng là {len(listNews)} tin mới \n\n'
        tittleNews = ''

        for news in listNews:
            tittleNews += news["tittle"] + "\n" + news["link"] + "\n"
        await update.message.reply_text(f'{countNews}')
        await update.message.reply_text(f'{tittleNews}')
    except Exception as e:
        logging.error(f"Error in '/vnex' command: {str(e)}")


####

maxCount = 20
count = 0


async def dantri(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        global maxCount, count
        listNews = getNewsDANTRI()
        print(listNews)
        countNews = f'Có tổng cộng là {len(listNews)} tin mới \n\n'
        tittleNews = ''
        listNewsRes = listNews[count:maxCount]

        for news in listNewsRes:
            tittleNews += news["tittle"] + "\n" + "https://dantri.com.vn/" + news["link"] + "\n"

        await update.message.reply_text(f'{countNews}')
        await update.message.reply_text(f'tin thứ {count} đến thứ {maxCount}')
        await update.message.reply_text(f'{tittleNews}')
    except Exception as e:
        logging.error(f"Error in '/dantri' command: {str(e)}")


async def dantriPL(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global maxCount, count
    maxCount += 20
    count += 20
    await dantri(update, context)


async def dantriINIT(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        global maxCount, count
        maxCount = 20
        count = 0
        await dantri(update, context)
    except Exception as e:
        logging.error(f"Error in 'hello' command: {str(e)}")


async def dantriMINUS(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        global maxCount, count
        if count == 0:
            await dantri(update, context)
            return
        maxCount = maxCount - 20
        count = count - 20
        await dantri(update, context)
    except Exception as e:
        logging.error(f"Error in 'dantriMINUS' command: {str(e)}")


app = ApplicationBuilder().token("6594398907:AAGvqo74y9p5BIEmBG6fcwDPanJnGWsLwps").build()
# run function /:command
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("vnex", vnex))
app.add_handler(CommandHandler("dantri", dantri))
app.add_handler(CommandHandler("dantriPL", dantriPL))
app.add_handler(CommandHandler("dantriINIT", dantriINIT))
app.add_handler(CommandHandler("dantriMINUS", dantriMINUS))

app.run_polling()
