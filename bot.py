from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Start / Main Menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("বাংলা", callback_data='lang_bn')],
        [InlineKeyboardButton("English", callback_data='lang_en')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('ভাষা নির্বাচন করুন / Choose your language:', reply_markup=reply_markup)

# Menu Generator
def get_menu(language):
    if language == 'bn':
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("আমার সম্পর্কে", callback_data='about_bn')],
            [InlineKeyboardButton("আমার দক্ষতা", callback_data='skills_bn')],
            [InlineKeyboardButton("আমার প্রোজেক্ট", callback_data='projects_bn')],
            [InlineKeyboardButton("যোগাযোগ", callback_data='contact_bn')],
        ])
    else:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("About Me", callback_data='about_en')],
            [InlineKeyboardButton("My Skills", callback_data='skills_en')],
            [InlineKeyboardButton("My Projects", callback_data='projects_en')],
            [InlineKeyboardButton("Contact Info", callback_data='contact_en')],
        ])

# Button Handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ভাষা নির্বাচন
    if data == 'lang_bn':
        await query.message.delete()
        await query.message.reply_text('একটি অপশন নির্বাচন করুন:', reply_markup=get_menu('bn'))

    elif data == 'lang_en':
        await query.message.delete()
        await query.message.reply_text('Please choose an option:', reply_markup=get_menu('en'))

    # বাংলা অপশন হ্যান্ডলিং
    elif data.endswith('_bn'):
        await query.message.delete()
        if data == 'about_bn':
            text = (
                "**আমার সম্পর্কে**\n\n"
                "আমি আয়মান হাসান শান (Swygen), ময়মনসিংহ, বাংলাদেশ থেকে। "
                "আমি ওয়েব ডেভেলপার, অ্যাপ ডেভেলপার, ডিজাইনার এবং কাস্টমার সাপোর্ট এজেন্ট।"
            )
        elif data == 'skills_bn':
            text = (
                "**আমার দক্ষতা**\n\n"
                "- ওয়েব ডেভেলপমেন্ট\n"
                "- অ্যাপ ডেভেলপমেন্ট\n"
                "- গ্রাফিক ডিজাইন\n"
                "- বট ডেভেলপমেন্ট\n"
                "- UI/UX ডিজাইন\n"
                "- ডিজিটাল মার্কেটিং"
            )
        elif data == 'projects_bn':
            text = (
                "**আমার প্রোজেক্ট**\n\n"
                "- Ludo BD Premium\n"
                "- King of Ludo Bot\n"
                "- Premium Service Website"
            )
        else:  # contact_bn
            text = (
                "**যোগাযোগ**\n\n"
                "ইমেইল: swygenofficial@gmail.com\n"
                "ফোন: 01621439840\n"
                "টেলিগ্রাম: @SwygenOfficial"
            )

        back_keyboard = InlineKeyboardButton("Back", callback_data='lang_bn')
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(back_keyboard))

    # English অপশন হ্যান্ডলিং
    elif data.endswith('_en'):
        await query.message.delete()
        if data == 'about_en':
            text = (
                "**About Me**\n\n"
                "I am Ayman Hasan Shaan (Swygen), from Mymensingh, Bangladesh. "
                "I am a web developer, app developer, designer, and customer support agent."
            )
        elif data == 'skills_en':
            text = (
                "**My Skills**\n\n"
                "- Web Development\n"
                "- App Development\n"
                "- Graphic Design\n"
                "- Bot Development\n"
                "- UI/UX Design\n"
                "- Digital Marketing"
            )
        elif data == 'projects_en':
            text = (
                "**My Projects**\n\n"
                "- Ludo BD Premium\n"
                "- King of Ludo Bot\n"
                "- Premium Service Website"
            )
        else:  # contact_en
            text = (
                "**Contact Info**\n\n"
                "Email: swygenofficial@gmail.com\n"
                "Phone: 01621439834\n"
                "Telegram: @SwygenOfficial"
            )

        back_keyboard = InlineKeyboardButton("Back", callback_data='lang_en')
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(back_keyboard))

# Main function
def main():
    application = Application.builder().token('8147124086:AAF8RnTlyUBARkNMnwxMWktgm1JF8gVZTUY').build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
