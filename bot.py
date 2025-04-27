from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ইউজার ভাষা এবং মেসেজ আইডি ট্র্যাকিং
USER_LANGUAGE = {}
USER_MESSAGE_ID = {}

TOKEN = '8147124086:AAF8RnTlyUBARkNMnwxMWktgm1JF8gVZTUY'  # <-- এখানে তোমার BotFather টোকেন বসাও

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.first_name
    USER_LANGUAGE[user_id] = 'en'  # ডিফল্ট ভাষা ইংরেজি

    welcome_text = f"👋🏻 **Hello {username}!**\n\nWelcome to Developer Swygen Help Bot.\nPlease select your language to continue:"  
    keyboard = [  
        [InlineKeyboardButton("🇧🇩 বাংলা", callback_data='set_lang_bn')],  
        [InlineKeyboardButton("🇬🇧 English", callback_data='set_lang_en')],  
    ]  
    sent_message = await update.message.reply_text(  
        welcome_text,  
        reply_markup=InlineKeyboardMarkup(keyboard),  
        parse_mode='Markdown'  
    )  
    USER_MESSAGE_ID[user_id] = sent_message.message_id

# ভাষা সিলেকশন হ্যান্ডলার
async def language_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == 'set_lang_bn':  
        USER_LANGUAGE[user_id] = 'bn'  
    else:  
        USER_LANGUAGE[user_id] = 'en'  

    await send_main_menu(update, context, edit=True)

# মেনু পাঠানো ফাংশন
async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, edit=False):
    user_id = update.effective_user.id
    lang = USER_LANGUAGE.get(user_id, 'en')

    text = "🏡 **Main Menu**\n\nChoose what you want to explore:" if lang == 'en' else "🏡 **প্রধান মেনু**\n\nআপনি কী জানতে চান?"  

    keyboard = [  
        [InlineKeyboardButton("👤 About Me", callback_data='about')],  
        [InlineKeyboardButton("🛠️ Skills", callback_data='skills')],  
        [InlineKeyboardButton("🌐 Website", callback_data='website')],  
        [InlineKeyboardButton("📞 Contact", callback_data='contact')],  
        [InlineKeyboardButton("🗂️ Projects", callback_data='projects')],  
        [InlineKeyboardButton("📜 Privacy Policy", callback_data='privacy')],  
        [InlineKeyboardButton("👨‍💻 Developer", callback_data='developer')],  
        [InlineKeyboardButton("🇧🇩 বাংলা", callback_data='set_lang_bn'),  
         InlineKeyboardButton("🇬🇧 English", callback_data='set_lang_en')],  
    ]  

    if edit:  
        await context.bot.edit_message_text(  
            chat_id=user_id,  
            message_id=USER_MESSAGE_ID[user_id],  
            text=text,  
            reply_markup=InlineKeyboardMarkup(keyboard),  
            parse_mode='Markdown'  
        )  
    else:  
        sent_message = await context.bot.send_message(  
            chat_id=user_id,  
            text=text,  
            reply_markup=InlineKeyboardMarkup(keyboard),  
            parse_mode='Markdown'  
        )  
        USER_MESSAGE_ID[user_id] = sent_message.message_id

# মেনু অপশন হ্যান্ডলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = USER_LANGUAGE.get(user_id, 'en')

    back_button = InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')  

    if query.data == 'about':  
        text = "👤 **About Me**\n\nHi, I'm Ayman Hasan Shaan, passionate about Web Development and Automation." if lang == 'en' else "👤 **আমার সম্পর্কে**\n\nআমি আয়মান হাসান শান, ওয়েব ডেভেলপমেন্ট এবং অটোমেশন নিয়ে কাজ করি।"  

    elif query.data == 'skills':  
        text = "🛠️ **Skills**\n\n- Python\n- HTML, CSS, JS\n- Telegram Bots\n- Automation Scripts\n- PHP\n- Node.js\n- React" if lang == 'en' else "🛠️ **স্কিলস**\n\n- পাইথন\n- এইচটিএমএল, সিএসএস, জাভাস্ক্রিপ্ট\n- টেলিগ্রাম বটস\n- অটোমেশন স্ক্রিপ্টস\n- পিএইচপি\n- নোড.জেএস\n- রিয়েক্ট"  

    elif query.data == 'website':  
        text = "🌐 Visit my website: [Click Here](https://swygen.netlify.app/)"  

    elif query.data == 'contact':  
        text = "📞 **Contact Info**\n\n- Email: swygenofficial@gmail.com\n- Telegram: @Swygen_bd" if lang == 'en' else "📞 **যোগাযোগের তথ্য**\n\n- ইমেইল: swygenofficial@gmail.com\n- টেলিগ্রাম: @Swygen_bd"  

    elif query.data == 'privacy':  
        text = "📜 [Read our Privacy Policy](https://swygen.netlify.app/police)"  

    elif query.data == 'developer':  
        text = "👨‍💻 **Developer**\n\nBot developed by Swygen Official."  

    elif query.data == 'projects':  
        await send_projects_menu(update, context)  
        return  

    elif query.data == 'back_to_menu':  
        await send_main_menu(update, context, edit=True)  
        return  

    await context.bot.edit_message_text(  
        chat_id=user_id,  
        message_id=USER_MESSAGE_ID[user_id],  
        text=text,  
        reply_markup=InlineKeyboardMarkup([back_button]),  
        parse_mode='Markdown'  
    )

# প্রজেক্ট মেনু পাঠানোর ফাংশন
async def send_projects_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    keyboard = [  
        [InlineKeyboardButton("🌐 Website Developer", callback_data='project_website')],  
        [InlineKeyboardButton("📱 App Developer", callback_data='project_app')],  
        [InlineKeyboardButton("🎨 UI/UX Designer", callback_data='project_uiux')],  
        [InlineKeyboardButton("🤖 Chat Bot Developer", callback_data='project_chatbot')],  
        [InlineKeyboardButton("☎️ Customer Support", callback_data='project_support')],  
        [InlineKeyboardButton("👨‍💻 Programming", callback_data='project_programming')],  
        [InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')],  
    ]  

    text = "🗂️ **My Projects**\n\nChoose a project to explore:"  

    await context.bot.edit_message_text(  
        chat_id=user_id,  
        message_id=USER_MESSAGE_ID[user_id],  
        text=text,  
        reply_markup=InlineKeyboardMarkup(keyboard),  
        parse_mode='Markdown'  
    )

# নির্দিষ্ট প্রজেক্ট ডিটেইল পাঠানোর ফাংশন
async def send_project_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    project_photos = {  
        'project_website': ("🌐 **Website Development**", "https://assets.onecompiler.app/43ea4pg72/43fr339cx/web-development-flat-landing-page-creative-team-designers-developers-work-together-illustration-full-stack-development-software-engineering-web-page-composition-with-people-characters_9209-3545.webp"),  
        'project_app': ("📱 **App Development**", "https://i.postimg.cc/JnRTm9fF/app-development-banner-33099-1720.webp"),  
        'project_uiux': ("🎨 **UI/UX Design**", "https://i.postimg.cc/QCySQVFL/realistic-ui-ux-background-23-2149046824.webp"),  
        'project_chatbot': ("🤖 **Chat Bot**", "https://i.postimg.cc/YSHRf5CS/chat-bot-concept-illustration-114360-5223.webp"),  
        'project_support': ("☎️ **Customer Support**", "https://i.postimg.cc/sxv4gywT/organic-flat-design-customer-support-23-2148887076.webp"),  
        'project_programming': ("👨‍💻 **Programming**", "https://i.postimg.cc/VvpBSThm/flat-composition-with-programmer-testing-programs-illustration-1284-55908.webp"),  
    }  

    title, photo_url = project_photos.get(query.data, ("Project", ""))  

    back_button = InlineKeyboardButton("🔙 Back", callback_data='projects')  

    await context.bot.send_photo(  
        chat_id=user_id,  
        photo=photo_url,  
        caption=title,  
        reply_markup=InlineKeyboardMarkup([back_button]),  
        parse_mode='Markdown'  
    )

# /help কমান্ড
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /start to restart the bot.")

# মেইন এপ রুন করা
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))  
    app.add_handler(CommandHandler('help', help_command))  
    app.add_handler(CallbackQueryHandler(language_selected, pattern='^set_lang_'))  
    app.add_handler(CallbackQueryHandler(button_handler))  

    app.run_polling()
