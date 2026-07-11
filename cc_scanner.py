from telethon import TelegramClient, events
import re
import asyncio
from datetime import datetime
import os

# ==================== کۆنفیگ ====================
API_ID = int(os.getenv('API_ID', 37308724))
API_HASH = os.getenv('API_HASH', 'dd414cde663ec3ff9f48aefa8b86c1c0')
BOT_TOKEN = os.getenv('BOT_TOKEN', '8738218688:AAEsk2shWSPLsg3Q6FNkTsh7haZbVfY_hD4')
CHANNEL_TO_MONITOR = os.getenv('CHANNEL_TO_MONITOR', '@Ccv526')
DUMP_CHANNEL = os.getenv('DUMP_CHANNEL', '@Kurdchian')
# ================================================

client = TelegramClient('cc_scanner', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# شێوەی کارت: 16 ژمارە | مانگ | ساڵ | CVV
CC_PATTERN = r'\b(\d{16})\s*[|/:;-]\s*(\d{2})\s*[|/:;-]\s*(\d{2,4})\s*[|/:;-]\s*(\d{3,4})\b'

def luhn_check(card_number):
    total = 0
    reverse_digits = [int(d) for d in str(card_number)][::-1]
    for i, digit in enumerate(reverse_digits):
        if i % 2 == 1:
            doubled = digit * 2
            total += doubled - 9 if doubled > 9 else doubled
        else:
            total += digit
    return total % 10 == 0

@client.on(events.NewMessage(chats=CHANNEL_TO_MONITOR))
async def cc_scanner(event):
    if not event.raw_text:
        return

    matches = re.findall(CC_PATTERN, event.raw_text)
    if not matches:
        return

    found_cards = []
    for card_num, month, year, cvv in matches:
        year_full = f"20{year}" if len(year) == 2 else year
        if luhn_check(card_num):
            result = (
                f"✅ **CC Approved**\n"
                f"💳 کارت: `{card_num}`\n"
                f"📅 مانگ/ساڵ: {month}/{year_full}\n"
                f"🔐 CVV: `{cvv}`\n"
                f"🔗 [بینینی پەیام]({event.message.link})\n"
                f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"{'─'*30}"
            )
            found_cards.append(result)
            print(f"[+] کارتی پشتڕاستکراو: {card_num}")

    if found_cards:
        await client.send_message(DUMP_CHANNEL, "\n\n".join(found_cards))

async def main():
    print("="*40)
    print("🤖 بۆتی سکانکردنی CC")
    print(f"📌 چەناڵی سەرچاوە: {CHANNEL_TO_MONITOR}")
    print(f"📌 چەناڵی دەرهات: {DUMP_CHANNEL}")
    print("="*40)
    print("بۆتەکە کاردەکات... چاوەڕوانی پەیامەکان")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
