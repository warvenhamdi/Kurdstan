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

# 🔹 داتابەیس و زانیارییەکانی ئەو 6 BINەی کە ناردووت
BINS_INFO = [
    {"bin": "517949", "bank": "CITIBANK N.A.", "country": "UNITED STATES [US] 🇺🇸", "type": "MASTERCARD - PLATINUM - CREDIT"},
    {"bin": "508933", "bank": "HDFC BANK", "country": "INDIA [IN] 🇮🇳", "type": "RUPAY - PLATINUM - DEBIT"},
    {"bin": "516628", "bank": "WESTPAC BANKING CORPORATION", "country": "AUSTRALIA [AU] 🇦🇺", "type": "MASTERCARD - CREDIT"},
    {"bin": "457826", "bank": "DUBAI ISLAMIC BANK", "country": "UNITED ARAB EMIRATES 🇦🇪", "type": "VISA - PLATINUM - DEBIT"},
    {"bin": "530232", "bank": "SUMITOMO MITSUI CARD COMPANY", "country": "JAPAN 🇯🇵", "type": "MASTERCARD - GOLD - CREDIT"},
    {"bin": "512676", "bank": "PT. BANK MANDIRI (PERSERO) TBK", "country": "INDONESIA 🇮🇩", "type": "MASTERCARD - STANDARD - CREDIT"},
]

def generate_cards(bins_data, count):
    cards = []
    for _ in range(count):
        # 🔹 هەڵبژاردنی یەک BIN بە هەڕەمەکی
        selected_bin = random.choice(bins_data)
        bin_num = selected_bin["bin"]
        bank = selected_bin["bank"]
        country = selected_bin["country"]
        card_type = selected_bin["type"]

        # دروستکردنی 9 ژمارەی هەڕەمەکی دیکە بۆ گەیشتن بە 15 ژمارە
        random_part = str(random.randint(0, 999999999)).zfill(9)
        partial_card = bin_num + random_part

        # زیادکردنی دوایین ژمارە بەپێی ڕێسای Luhn بۆ گەیشتن بە 16 ژمارە
        card_number = append(partial_card)

        month = str(random.randint(1, 12)).zfill(2)
        year = str(random.randint(2025, 2032)) # وەک داوای خۆت (25 بۆ 32)
        cvv = str(random.randint(100, 999))

        # زانیارییەکان دەپارێزرێن بۆ ناردن
        cards.append({
            "card_number": card_number,
            "month": month,
            "year": year,
            "cvv": cvv,
            "bank": bank,
            "country": country,
            "type": card_type
        })
    return cards

CARDS_LIST = generate_cards(BINS_INFO, NUMBER_OF_CARDS)
print(f"✅ {len(CARDS_LIST)} کارت بە 6 BINە جیاوازەکان دروستکران.")

current_index = 0

async def send_card_message(bot, channel, admin):
    global current_index

    if not CARDS_LIST:
        print("❌ هیچ کارتێک دروست نەکراوە.")
        return False

    if current_index >= len(CARDS_LIST):
        print("✅ هەموو کارتەکان نێردران!")
        return False

    card_data = CARDS_LIST[current_index]
    card_number = card_data["card_number"]
    month = card_data["month"]
    year = card_data["year"]
    cvv = card_data["cvv"]
    bank = card_data["bank"]
    country = card_data["country"]
    card_type = card_data["type"]

    # 🔹 فۆرمەتی سادە و خاوێن (بەپێی داوای تۆ + زانیارییەکانی BIN)
    text = (
        f"{card_number}|{month}|{year}|{cvv}\n"
        f"Bank: {bank}\n"
        f"Country: {country}\n"
        f"Type: {card_type}"
    )

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

    print(f"🚀 بۆت دەستی پێکرد (5 چرکە، کارت لە 6 BINە ناردووەکان)...")
    while True:
        result = await send_card_message(bot, CHANNEL_ID, ADMIN_ID)
        if not result:
            break
        await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
