from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ইউজার ভাষা ও মেসেজ আইডি ট্র্যাকিং
USER_LANGUAGE = {}
USER_MESSAGE_ID = {}

TOKEN = '8147124086:AAF8RnTlyUBARkNMnwxMWktgm1JF8gVZTUY'  # <-- এখানে তোমার BotFather থেকে নেয়া টোকেন বসাও

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.first_name
    USER_LANGUAGE[user_id] = 'en'  # ডিফল্ট ভাষা ইংরেজি

    welcome_text = f"✨ **Hello {username}!**\n\nWelcome to **Swygen Official Bot**.\nPlease select your language to continue:"  
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

# ভাষা সিলেক্ট হ্যান্ডলার
async def language_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == 'set_lang_bn':
        USER_LANGUAGE[user_id] = 'bn'
    else:
        USER_LANGUAGE[user_id] = 'en'

    await send_main_menu(update, context, edit=True)

# মেনু পাঠানোর ফাংশন
async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, edit=False):
    user_id = update.effective_user.id
    lang = USER_LANGUAGE.get(user_id, 'en')

    text = "🏠 **Main Menu**\n\nSelect an option below:" if lang == 'en' else "🏠 **প্রধান মেনু**\n\nনিচের অপশন থেকে বেছে নিন:"

    keyboard = [
        [InlineKeyboardButton("👤 About Me", callback_data='about')],
        [InlineKeyboardButton("🛠️ Skills", callback_data='skills')],
        [InlineKeyboardButton("🌐 Website", callback_data='website')],
        [InlineKeyboardButton("📞 Contact", callback_data='contact')],
        [InlineKeyboardButton("🗂️ Projects", callback_data='projects')],
        [InlineKeyboardButton("📜 Privacy Policy", callback_data='privacy')],
        [InlineKeyboardButton("👨‍💻 Developer", callback_data='developer')],
        [InlineKeyboardButton("🌐 Change Language", callback_data='change_language')],
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

    back_button = [ [InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')] ]

    if query.data == 'about':
        text = ("👤 **About Me**\n\n"
                "Hi, I'm **Ayman Hasan Shaan** a.k.a. **Swygen**.\n"
                "A passionate Web Developer & Automation Expert.") if lang == 'en' else (
                "👤 **আমার সম্পর্কে**\n\n"
                "আমি **আয়মান হাসান শান** ওরফে **Swygen**।\n"
                "আমি একজন ওয়েব ডেভেলপার এবং অটোমেশন বিশেষজ্ঞ।")

    elif query.data == 'skills':
        text = ("🛠️ **Skills**\n\n"
                "- Web Development\n"
                "- App Development\n"
                "- Graphic Design\n"
                "- Bot Development\n"
                "- UI/UX Design\n"
                "- Digital Marketing") if lang == 'en' else (
                "🛠️ **দক্ষতা**\n\n"
                "- ওয়েব ডেভেলপমেন্ট\n"
                "- অ্যাপ ডেভেলপমেন্ট\n"
                "- গ্রাফিক ডিজাইন\n"
                "- বট ডেভেলপমেন্ট\n"
                "- ইউআই/ইউএক্স ডিজাইন\n"
                "- ডিজিটাল মার্কেটিং")

    elif query.data == 'website':
        text = "🌐 Visit my website: [Click Here](https://swygen.netlify.app/)"

    elif query.data == 'contact':
        text = ("📞 **Contact Info**\n\n"
                "- Email: swygenofficial@gmail.com\n"
                "- Phone: 01621439834\n"
                "- Whatsapp: [Message](https://wa.me/message/BQ77IMY2MHW6E1)") if lang == 'en' else (
                "📞 **যোগাযোগের তথ্য**\n\n"
                "- ইমেইল: swygenofficial@gmail.com\n"
                "- ফোন: 01621439834\n"
                "- হোয়াটসঅ্যাপ: [মেসেজ করুন](https://wa.me/message/BQ77IMY2MHW6E1)")

    elif query.data == 'privacy':
        text = "📜 [Read our Privacy Policy](https://swygen.netlify.app/police)"

    elif query.data == 'developer':
        text = ("👨‍💻 **Developer Info**\n\n"
                "Bot Developed by **Swygen Official**.") if lang == 'en' else (
                "👨‍💻 **ডেভেলপার তথ্য**\n\n"
                "**Swygen Official** কর্তৃক নির্মিত।")

    elif query.data == 'projects':
        await send_projects_menu(update, context)
        return

    elif query.data == 'change_language':
        await start(update, context)
        return

    elif query.data == 'back_to_menu':
        await send_main_menu(update, context, edit=True)
        return

    await context.bot.edit_message_text(
        chat_id=user_id,
        message_id=USER_MESSAGE_ID[user_id],
        text=text,
        reply_markup=InlineKeyboardMarkup(back_button),
        parse_mode='Markdown'
    )

# প্রজেক্ট মেনু
async def send_projects_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    text = "🗂️ **Projects**\n\nSelect a project to explore:"

    keyboard = [
        [InlineKeyboardButton("🌐 Website Development", callback_data='project_website')],
        [InlineKeyboardButton("📱 App Development", callback_data='project_app')],
        [InlineKeyboardButton("🎨 UI/UX Design", callback_data='project_uiux')],
        [InlineKeyboardButton("🤖 Chatbot Development", callback_data='project_chatbot')],
        [InlineKeyboardButton("☎️ Customer Support", callback_data='project_support')],
        [InlineKeyboardButton("👨‍💻 Programming", callback_data='project_programming')],
        [InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')],
    ]

    await context.bot.edit_message_text(
        chat_id=user_id,
        message_id=USER_MESSAGE_ID[user_id],
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# নির্দিষ্ট প্রজেক্ট ডিটেইলস
async def send_project_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    project_texts = {
        'project_website': "🌐 **Website Development**\n\nCustom websites for businesses and individuals.",
        'project_app': "📱 **App Development**\n\nModern and user-friendly mobile apps.",
        'project_uiux': "🎨 **UI/UX Design**\n\nStunning interfaces and experiences.",
        'project_chatbot': "🤖 **Chatbot Development**\n\nAutomated bots for business communication.",
        'project_support': "☎️ **Customer Support**\n\nProfessional customer service solutions.",
        'project_programming': "👨‍💻 **Programming**\n\nEfficient and scalable coding solutions.",
    }

    text = project_texts.get(query.data, "No details available.")

    back_button = [ [InlineKeyboardButton("🔙 Back", callback_data='projects')] ]

    await context.bot.edit_message_text(
        chat_id=user_id,
        message_id=USER_MESSAGE_ID[user_id],
        text=text,
        reply_markup=InlineKeyboardMarkup(back_button),
        parse_mode='Markdown'
    )

# অ্যাপ্লিকেশন রান
async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(language_selected, pattern='^set_lang_'))
    application.add_handler(CallbackQueryHandler(button_handler, pattern='^(about|skills|website|contact|privacy|developer|projects|change_language|back_to_menu)$'))
    application.add_handler(CallbackQueryHandler(send_project_details, pattern='^project_'))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
