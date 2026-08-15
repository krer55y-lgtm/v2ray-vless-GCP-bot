import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8213423103:AAGOroWULpNQeUaXwJQDnvTkmaleBzKJTP0"

# قائمة السيرفرات بالأكواد المعدلة الجديدة
VLESS_SERVERS = {
    "vless_1": {
        "name": "سيرفر VLESS الأول 🚀",
        "code": "Vless://e5cc16a6-ea42-46b2-82ae-ad2157e1641b@172.67.185.178:443?path=%2F&security=tls&encryption=none&host=hhlfy.twiladaphne.ndjp.net&type=ws&sni=hhlfy.twiladaphne.ndjp.net#%F0%9D%94%B9%F0%9D%95%90%20%3A-%20%F0%9D%95%82%F0%9D%94%B8%E2%84%9D%E2%84%9D%F0%9D%94%B8%E2%84%9D"
    },
    "vless_2": {
        "name": "سيرفر VLESS الثاني ⚡",
        "code": "vless://77777777-8a3e-6666-b6d1-a9c5f0e8b3a2@cf.9999669.xyz:443?path=%2F&security=tls&encryption=none&host=faxf32gkfzoxqv.fx6hsv0.ccwu.cc&fp=chrome&type=ws&sni=faxf32gkfzoxqv.fx6hsv0.ccwu.cc#%F0%9D%94%B9%F0%9D%95%90%20%3A-%20%F0%9D%95%82%F0%9D%94%B8%E2%84%9D%E2%84%9D%F0%9D%94%B8%E2%84%9D"
    },
    "vless_3": {
        "name": "سيرفر VLESS الثالث 🌐",
        "code": "vless://77777777-8a3e-6666-b6d1-a9c5f0e8b3a2@mfa.gov.ua:2087?path=%2F&security=tls&encryption=none&host=fx3l5i2wdfxln0.fx6hsv0.ccwu.cc&fp=chrome&type=ws&sni=fx3l5i2wdfxln0.fx6hsv0.ccwu.cc#%F0%9D%94%B9%F0%9D%95%90%20%3A-%20%F0%9D%95%82%F0%9D%94%B8%E2%84%9D%E2%84%9D%F0%9D%94%B8%E2%84%9D"
    }
}

# تم ترك القيمة فارغة لتضع كود Google Cloud هنا لاحقاً
GCP_CODE = ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("سيرفرات VLESS 🚀", callback_data='vless_menu')],
        [InlineKeyboardButton("سيرفر Google Cloud (GCP) ☁️", callback_data='get_gcp')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("أهلاً بك! اختر نوع السيرفر الذي تريد الحصول عليه:", reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'vless_menu':
        keyboard = []
        for key, server in VLESS_SERVERS.items():
            keyboard.append([InlineKeyboardButton(f"🟢 {server['name']}", callback_data=key)])
        keyboard.append([InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data='main_menu')])
        await query.message.edit_text("اختر السيرفر المناسب لك:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data in VLESS_SERVERS:
        server = VLESS_SERVERS[query.data]
        text = f"إليك كود {server['name']} (اضغط للنسخ):\n\n<code>{server['code']}</code>"
        await query.message.reply_text(text, parse_mode='HTML')

    elif query.data == 'get_gcp':
        if GCP_CODE:
            text = f"إليك سيرفر Google Cloud GCP (اضغط للنسخ):\n\n<code>{GCP_CODE}</code>"
            await query.message.reply_text(text, parse_mode='HTML')
        else:
            await query.message.reply_text("عذراً، سيرفر Google Cloud غير متوفر حالياً 🔴")

    elif query.data == 'main_menu':
        keyboard = [
            [InlineKeyboardButton("سيرفرات VLESS 🚀", callback_data='vless_menu')],
            [InlineKeyboardButton("سيرفر Google Cloud (GCP) ☁️", callback_data='get_gcp')]
        ]
        await query.message.edit_text("أهلاً بك! اختر نوع السيرفر الذي تريد الحصول عليه:", reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    
    print("البوت يعمل الآن...")
    app.run_polling()
