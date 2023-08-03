from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from getnews import getNewsVNEXPRESS
from getnews import getNewsDANTRI






async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Xin chao {update.effective_user.first_name}')

async def vnex(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    listNews = getNewsVNEXPRESS()
    print(listNews)
    countNews = f'Có tổng cộng là {len(listNews)} tin mới \n\n'
    tittleNews = ''

    for news in listNews:
        tittleNews += news["tittle"] + "\n" + news["link"] + "\n"
    await update.message.reply_text(f'{countNews}')
    await update.message.reply_text(f'{tittleNews}')
####
async def dantri(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    listNews = getNewsDANTRI()
    print(listNews)
    countNews = f'Có tổng cộng là {len(listNews)} tin mới \n\n'
    tittleNews = ''
    maxCount = 20
    count = 0
    for news in listNews:
        tittleNews += news["tittle"] + "\n" + "https://dantri.com.vn/"+news["link"] + "\n"
        count = count + 1
        if count > maxCount:
            break

    await update.message.reply_text(f'{countNews}')
    await update.message.reply_text(f'{tittleNews}')



app = ApplicationBuilder().token("6594398907:AAGvqo74y9p5BIEmBG6fcwDPanJnGWsLwps").build()


#run function hello /hello
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("vnex", vnex))
app.add_handler(CommandHandler("dantri", dantri))


app.run_polling()