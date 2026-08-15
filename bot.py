import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- سيرفر وهمي لإبقاء البوت شغالاً ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def keep_alive():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    t = threading.Thread(target=server.serve_forever)
    t.daemon = True
    t.start()

keep_alive()
# ------------------------------------

TOKEN = "8213423103:AAG8IwsqQK4TcxsNOsNrguxPufd6yx03PZk"
ADMIN_ID = 5577104159 

REQUIRED_CHANNELS = ["@KingsNet_Free", "@Free_Net_Arab"]

VLESS_SERVERS = {
    "vless_1": {"name": "سيرفر VLESS الأول 🚀", "code": "Vless://e5cc16a6-ea42-46b2-82ae-ad2157e1641b@172.67.185.178:443?path=%2F&security=tls&encryption=none&host=hhlfy.twiladaphne.ndjp.net&type=ws&sni=hhlfy.twiladaphne.ndjp.net#%F0%9D%94%B9%F0%9D%95%90%20%3A-%20%F0%9D%95%82%F0%9D%94%B8%E2%84%9D%E2%84%9D%F0%9D%94%B8%E2%84%9D"},
    "vless_2": {"name": "سيرفر VLESS الثاني ⚡", "code": "vless://77777777-8a3e-6666-b6d1-a9c5f0e8b3a2@cf.9999669.xyz:443?path=%2F&security=tls&encryption=none&host=faxf32gkfzoxqv.fx6hsv0.ccwu.cc&fp=chrome&type=ws&sni=faxf32gkfzoxqv.fx6hsv0.ccwu.cc#%F0%9D%94%B9%F0%9D%95%90%20%3A-%20%F0%9D%95%82%F0%9D%94%B8%E2%84%9D%E2%84%9D%F0%9D%94%B8%E2%84%9D"},
    "vless_3": {"name": "سيرفر VLESS الثالث 🌐", "code": "vless://77777777-8a3e-6666-b6d1-a9c5f0e8b3a2@mfa.gov.ua:2087?path=%2F&security=tls&encryption=none&host=fx3l5i2wdfxln0.fx6hsv0.ccwu.cc&fp=chrome&type=ws&sni=fx3l5i2wdfxln0.fx6hsv0.ccwu.cc#%F0%9D%94%B9%F0%9D%95%90%20%3A-%20%F0%9D%95%82%F0%9D%94%B8%E2%84%9D%E2%84%9D%F0%9D%94%B8%E2%84%9D"}
}

GCP_SERVER_LINK = "vless://abcd2026-1337-4ace-8bad-deadfacebeef@karrar-pro-482099808139.asia-southeast1.run.app:443?path=%2FTelegram%2F%40KingsNet_Free%2F%40H_G_5W&security=tls&encryption=none&host=karrar-pro-482099808139.asia-southeast1.run.app&type=ws&sni=karrar-pro-482099808139.asia-southeast1.run.app#GCP%20Google%20Cloud%20%7C%20BY%20Karrar"

# نص رسالة GCP بتنسيق HTML آمن
GCP_MESSAGE_TEXT = f"""<code>{GCP_SERVER_LINK}</code>

• <b>Google Cloud</b> ❞
• <b>Duration : 3 : 00</b> ❞
• <b>Server: USA</b> ❞
• <b>BY : @KingsNet_Free</b> ❞"""

def save_and_count_user(user_id):
    filename = "users.txt"
    if not os.path.exists(filename):
        open(filename, "w").close()
    
    with open(filename, "r") as f:
        users = set(f.read().splitlines())
    
    is_new = str(user_id) not in users
    if is_new:
        with open(filename, "a") as f:
            f.write(f"{user_id}\n")
        users.add(str(user_id))
        
    return is_new, len(users)

async def check_all_subscriptions(user_id, context):
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception:
            return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    is_new, total_users = save_and_count_user(user.id)
    
    if is_new and ADMIN_ID:
        username = f"@{user.username}" if user.username else "لا يوجد"
        lang = user.language_code if user.language_code else "غير معروفة"
        
        admin_text = (
            "👾 <b>شخص جديد دخل البوت</b>\n\n"
            "👤 <b>معلومات العضو الجديد:</b>\n"
            f"• <b>الاسم:</b> {user.full_name}\n"
            f"• <b>المعرف:</b> {username}\n"
            f"• <b>الآيدي:</b> <code>{user.id}</code>\n"
            f"• 🌐 <b>اللغة:</b> {lang}\n\n"
            f"📊 <b>إجمالي المستخدمين: {total_users}</b>"
        )
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode='HTML')
        except Exception as e:
            print(f"Failed to send admin notification: {e}")

    if not await check_all_subscriptions(user.id, context):
        keyboard = [
            [InlineKeyboardButton("📢 القناة الأولى", url="https://t.me/KingsNet_Free")],
            [InlineKeyboardButton("📢 القناة الثانية", url="https://t.me/Free_Net_Arab")],
            [InlineKeyboardButton("✅ تحقّق من الاشتراك", callback_data='check_sub')]
        ]
        await update.message.reply_text(
            "⚠️ **عذراً، يجب عليك الاشتراك في القناتين أدناه لاستخدام البوت:**",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        return

    keyboard = [[InlineKeyboardButton("سيرفرات VLESS 🚀", callback_data='vless_menu')], [InlineKeyboardButton("سيرفر Google Cloud (GCP) ☁️", callback_data='get_gcp')]]
    await update.message.reply_text("أهلاً بك! اختر نوع السيرفر:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'check_sub':
        if await check_all_subscriptions(query.from_user.id, context):
            keyboard = [[InlineKeyboardButton("سيرفرات VLESS 🚀", callback_data='vless_menu')], [InlineKeyboardButton("سيرفر Google Cloud (GCP) ☁️", callback_data='get_gcp')]]
            await query.message.edit_text("شكراً لاشتراكك في الجميع! اختر السيرفر:", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.answer("❌ لم تشترك في كل القنوات بعد!", show_alert=True)
        return

    if not await check_all_subscriptions(query.from_user.id, context):
        await query.answer("⚠️ يجب الاشتراك في جميع القنوات أولاً!", show_alert=True)
        return

    if query.data == 'vless_menu':
        keyboard = [[InlineKeyboardButton(f"🟢 {server['name']}", callback_data=key)] for key, server in VLESS_SERVERS.items()]
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data='main_menu')])
        await query.message.edit_text("اختر السيرفر:", reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif query.data in VLESS_SERVERS:
        await query.message.reply_text(f"كود {VLESS_SERVERS[query.data]['name']}:\n\n<code>{VLESS_SERVERS[query.data]['code']}</code>", parse_mode='HTML')
    
    elif query.data == 'get_gcp':
        await query.message.reply_text(GCP_MESSAGE_TEXT, parse_mode='HTML')
        
    elif query.data == 'main_menu':
        keyboard = [[InlineKeyboardButton("سيرفرات VLESS 🚀", callback_data='vless_menu')], [InlineKeyboardButton("سيرفر Google Cloud (GCP) ☁️", callback_data='get_gcp')]]
        await query.message.edit_text("أهلاً بك! اختر نوع السيرفر:", reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.run_polling()
