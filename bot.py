import asyncio
import csv
import os
from datetime import datetime
from telethon import TelegramClient, events

# ==================== زانیارییەکانت ====================
API_ID = 37308724
# 🔴 تکایە API_HASHـە نوێیەکەت لێرە بنووسە (دەتوانی لە my.telegram.org نوێی بکەیتەوە)
API_HASH = 'dd414cde663ec3ff9f48aefa8b86c1c0' 
# 🔴 تکایە تۆکنە نوێیەکەت لێرە بنووسە (لە @BotFatherـەوە)
BOT_TOKEN = '8879533750:AAGM_vlkYcIh12JsOoWN1iVuCr5RHRv_jMk'

# 🔴 چەناڵەکەی تۆ
CHANNEL_USERNAME = '@Ccvkurd426'
# =======================================================

client = TelegramClient('ccvkurd_scraper', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply(f"""
👋 سڵاو! بۆ بۆتی سکراپینگی چەناڵەکەت!

📌 چەناڵ: {CHANNEL_USERNAME}
⚡ **فەرمانەکان:**
/scratch - کۆکردنەوەی ١٠٠ پەیام
/scratch [ژمارە] - کۆکردنەوەی ژمارەی دیاریکراو
/info - زانیاری
""")

@client.on(events.NewMessage(pattern='/scratch(?: (\\d+))?'))
async def scratch_channel(event):
    limit = int(event.pattern_match.group(1)) if event.pattern_match.group(1) else 100
    if limit > 1000:
        await event.reply("❌ زۆرترین ١٠٠٠ پەیام!")
        return
    
    status = await event.reply(f"⏳ کۆکردنەوەی {limit} پەیام...")
    
    try:
        channel = await client.get_entity(CHANNEL_USERNAME)
        
        # ==================== چارەسەری کێشەکە ====================
        # iter_messages بەکاردێنین نەک GetHistoryRequest
        messages = []
        async for msg in client.iter_messages(channel, limit=limit):
            messages.append(msg)
        # =========================================================

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
            caption=f"✅ **{count} پەیام کۆکرانەوە!**"
        )
        
        os.remove(filename)
        await status.delete()
        
    except Exception as e:
        await event.reply(f"❌ **هەڵە:** {str(e)}\n\n💡 دڵنیابە چەناڵەکە گشتییە و بۆتەکە ئەندامە.")

@client.on(events.NewMessage(pattern='/info'))
async def info(event):
    try:
        channel = await client.get_entity(CHANNEL_USERNAME)
        await event.reply(f"""
📊 **زانیاری چەناڵ**
📌 ناو: {channel.title}
🌐 لینک: {CHANNEL_USERNAME}
""")
    except Exception as e:
        await event.reply(f"❌ نەتوانرا زانیاری وەربگیرێت: {e}")

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print(f"✅ بۆتەکە کاردەکات! چەناڵ: {CHANNEL_USERNAME}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 بۆتەکە راگیرا!")
