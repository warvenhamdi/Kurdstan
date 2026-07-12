# -*- coding: utf-8 -*-
import asyncio
import random
import re
from telegram import Bot
from telegram.error import TelegramError
from luhn import append

# ===== CONFIG =====
BOT_TOKEN = "8998790793:AAGawaYBBzHT-MlCv9x7eS3nnehsLTMIdg4"
CHANNEL_ID = "@Cvvcard828"
ADMIN_ID = 8130764336
INTERVAL_SECONDS = 5 # ٥ چرکە

NUMBER_OF_CARDS = 200
# ==============================================

def generate_cards(count):
    cards = []
    for _ in range(count):
        random_15_digits = str(random.randint(100000000000000, 999999999999999))
        card_number = append(random_15_digits) # 16 خانە بەپێی Luhn
        
        month = str(random.randint(1, 12)).zfill(2)
        # 🔹 گۆڕانکاری: ساڵ لە 2025 بۆ 2032
        year = str(random.randint(2025, 2032))
        cvv = str(random.randint(100, 999))
        
        cards.append(f"{card_number}|{month}|{year}|{cvv}")
    return cards

CARDS_LIST = generate_cards(NUMBER_OF_CARDS)
print(f"✅ {len(CARDS_LIST)} کارت دروستکران.")

current_index = 0

async def send_card_message(bot, channel, admin):
    global current_index

    if not CARDS_LIST:
        print("❌ هیچ کارتێک دروست نەکراوە.")
        return False

    if current_index >= len(CARDS_LIST):
        print("✅ هەموو کارتەکان نێردران!")
        return False

    card_line = CARDS_LIST[current_index]
    parts = card_line.split('|')
    card_number = parts[0].strip()
    month = parts[1].strip()
    year = parts[2].strip()
    cvv = parts[3].strip()

    # 🔹 فۆرمەتی ڕاستەوخۆ
    text = f"{card_number}|{month}|{year}|{cvv}"

    while True:
        try:
            await bot.send_message(chat_id=channel, text=text)
            print(f"✅ نێردرا: {card_number}|{month}|{year}|{cvv}")
            current_index += 1
            return True
        
        except TelegramError as e:
            err_msg = str(e)
            if "Flood control" in err_msg:
                match = re.search(r"Retry in (\d+)", err_msg)
                wait_time = int(match.group(1)) if match else 30
                print(f"⚠️ Flood control. چاوەڕوانی {wait_time} چرکە بکە...")
                await asyncio.sleep(wait_time)
            else:
                print(f"❌ هەڵەی تر ڕوویدا: {err_msg}")
                return False

async def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.get_me()
    except TelegramError:
        print("⚠️ تۆکەنەکە نادروستە")
        return

    print("🚀 بۆت دەستی پێکرد (5 چرکە، ساڵ 2025-2032)...")
    while True:
        result = await send_card_message(bot, CHANNEL_ID, ADMIN_ID)
        if not result:
            break
        await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
