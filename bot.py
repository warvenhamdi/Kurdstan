import asyncio
import csv
import os
from datetime import datetime
from telethon import TelegramClient, events

# ==================== زانیارییەکانت ====================
# ئاگاداربە: باشترە ئەمانە لە Environment Variablesـەکانی Railwayـدا دابنێیت
API_ID = 37308724
API_HASH = 'dd414cde663ec3ff9f48aefa8b86c1c0'
BOT_TOKEN = '8879533750:AAGM_vlkYcIh12JsOoWN1iVuCr5RHRv_jMk'

# 🔴 چەناڵەکەی تۆ
CHANNEL_USERNAME = '@Ccvkurd426'  # ناوی چەناڵەکەت
# =======================================================

client = TelegramClient('ccvkurd_scraper', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply(f"""
👋 سڵاو! بۆ بۆتی سکراپینگی چەناڵەکەت!

📌 ئەم بۆتە پەیامەکانی چەناڵی **{CHANNEL_USERNAME}** کۆدەکاتەوە.

⚡ **فەرمانەکان:**
/scratch - کۆکردنەوەی ١٠٠ پەیامی دوایین
/scratch [ژمارە] - کۆکردنەوەی ژمارەی دیاریکراو
/info - زانیاری چەناڵەکە
/help - ڕێنمایی
""")

@client.on(events.NewMessage(pattern='/scratch(?: (\\d+))?'))
async def scratch_channel(event):
    limit = int(event.pattern_match.group(1)) if event.pattern_match.group(1) else 100
    
    if limit > 1000:
        await event.reply("❌ زۆرترین ١٠٠٠ پەیام!")
        return
    
    status = await event.reply(f"⏳ کۆکردنەوەی {limit} پەیام لە {CHANNEL_USERNAME}...")
    
    try:
        channel = await client.get_entity(CHANNEL_USERNAME)
        
        # ==================== چارەسەری کێشەکە لێرەدایە ====================
        # لەبری GetHistoryRequest، iter_messages بەکاردەهێنین کە بۆ بۆتەکان ڕێگەپێدراوە
        messages = []
        async for msg in client.iter_messages(channel, limit=limit):
            messages.append(msg)
        # =================================================================

        count = len(messages)
        
        filename = f"Ccvkurd426_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ژمارە', 'بەروار', 'پەیام', 'لینک'])
            
            for idx, msg in enumerate(messages, 1):
                date = msg.date.strftime('%Y-%m-%d %H:%M:%S')
                text = msg.text.replace('\n', ' ') if msg.text else '(میدیا)'
                link = f"https://t.me/Ccvkurd426/{msg.id}"
                writer.writerow([idx, date, text[:500], link])
        
        await client.send_file(
            event.chat_id,
            filename,
            caption=f"""
✅ **پەیامەکان کۆکرانەوە!**

📊 **ئامار:**
• چەناڵ: {CHANNEL_USERNAME}
• پەیام: {count}
• کات: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📁 فایل: {filename}
"""
        )
        
        os.remove(filename)
        await status.delete()
        
    except Exception as e:
        await event.reply(f"""
❌ **هەڵە:** {str(e)}

💡 پێویستە:
1. بۆتەکە ئەندامی چەناڵەکە بێت
2. چەناڵەکە گشتی بێت یان بۆتەکە ئەندام بێت
""")

@client.on(events.NewMessage(pattern='/info'))
async def info(event):
    try:
        channel = await client.get_entity(CHANNEL_USERNAME)
        await event.reply(f"""
📊 **زانیاری چەناڵی Ccvkurd426**

📌 ناو: {channel.title}
🆔 ID: {channel.id}
👥 ئەندامان: {getattr(channel, 'participants_count', 'نادیار')}
🔒 جۆر: {'تایبەت' if getattr(channel, 'megagroup', False) else 'گشتی'}
🌐 لینک: t.me/Ccvkurd426
""")
    except Exception as e:
        await event.reply(f"❌ نەتوانرا زانیاری وەربگیرێت: {e}")

@client.on(events.NewMessage(pattern='/help'))
async def help(event):
    await event.reply(f"""
🤖 **ڕێنمایی بۆتی سکراپینگ**

📌 **چەناڵ:** @Ccvkurd426

⚡ **فەرمانەکان:**
• `/scratch` - ١٠٠ پەیامی دوایین
• `/scratch 200` - ٢٠٠ پەیام
• `/scratch 500` - ٥٠٠ پەیام
• `/info` - زانیاری چەناڵەکە
• `/help` - ئەم ڕێنماییە

⚠️ **تێبینی:**
• بۆت دەبێت ئەندامی چەناڵەکە بێت
• زۆرترین ١٠٠٠ پەیام
• فایل بە CSV دەنێردرێت
""")

# ==================== دەستپێکردن ====================

async def main():
    await client.start(bot_token=BOT_TOKEN)
    
    try:
        channel = await client.get_entity(CHANNEL_USERNAME)
        print(f"""
╔═══════════════════════════════════════════╗
║  ✅ بۆتەکە کاردەکات!                      ║
║  📌 چەناڵ: {channel.title}               ║
║  👥 ئەندامان: {getattr(channel, 'participants_count', '?')}           ║
║  💡 /help بۆ ڕێنمایی                      ║
╚═══════════════════════════════════════════╝
        """)
    except:
        print(f"""
❌ ناتوانیت بگەیت بە چەناڵی @Ccvkurd426
💡 تکایە بۆتەکە بکە بە ئەندامی چەناڵەکە!
        """)
    
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 بۆتەکە راگیرا!")
