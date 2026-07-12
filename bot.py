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
        # 🔹 هەڵبژاردنی جۆری کارت بە شێوەی هەڕەمەکی
        card_type = random.choice(['VISA', 'MASTERCARD', 'DISCOVER', 'AMEX'])
        
        # 🔹 دروستکردنی پێشگر و ژمارە هەڕەمەکییەکان بەپێی جۆرەکە
        if card_type in ['VISA', 'MASTERCARD', 'DISCOVER']:
            # 16 ژمارەیی: یەکەم ژمارە (4, 5, 6) + 15 ژمارەی تر
            prefix = '4' if card_type == 'VISA' else ('5' if card_type == 'MASTERCARD' else '6')
            random_part = str(random.randint(0, 999999999999999)).zfill(15) # 15 ژمارە
            partial_card = prefix + random_part
        elif card_type == 'AMEX':
            # 15 ژمارەیی: یەکەم ژمارە (3) + 14 ژمارەی تر
            prefix = '3'
            random_part = str(random.randint(0, 99999999999999)).zfill(14) # 14 ژمارە
            partial_card = prefix + random_part

        # 🔹 زیادکردنی دوایین ژمارەی پشکنین (Check digit) بەپێی ڕێسای Luhn
        card_number = append(partial_card)
        
        # بەشەکانی تر
        month = str(random.randint(1, 12)).zfill(2)
        year = str(random.randint(2025, 2032)) # ساڵ 2025 بۆ 2032
        cvv = str(random.randint(100, 999))
        
        # تەنها فۆرمەتی سادە دەنێررێت
        cards.append(f"{card_number}|{month}|{year}|{cvv}")
    return cards

CARDS_LIST = generate_cards(NUMBER_OF_CARDS)
print(f"✅ {len(CARDS_LIST)} کارتی جۆراوجۆر (VISA, MC, Discover, AMEX) دروستکران.")

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

    # 🔹 فۆرمەتی ناردن بەپێی داوای تۆ
    text = f"{card_number}|{month}|{year}|{cvv}"

    while True:
        try:
            await bot.send_message(chat_id=channel, text=text)
            print(f"✅ نێردرا: {text}")
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

    print("🚀 بۆت دەستی پێکرد (5 چرکە، کارتی 4 جۆر، فۆرمەتی سادە)...")
    while True:
        result = await send_card_message(bot, CHANNEL_ID, ADMIN_ID)
        if not result:
            break
        await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
