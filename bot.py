# -*- coding: utf-8 -*-
import asyncio
import random
from telegram import Bot
from telegram.error import TelegramError

# ===== CONFIG =====
BOT_TOKEN = "8998790793:AAGawaYBBzHT-MlCv9x7eS3nnehsLTMIdg4"
CHANNEL_ID = "@Cvvcard828"
ADMIN_ID = 8130764336
INTERVAL_SECONDS = 2

# 🔹 BIN و زانیارییەکانی
BIN = "444796"
BANK_NAME = "CREDIT ONE BANK, NATIONAL ASSOCIATION"
COUNTRY = "UNITED STATES 🇺🇸"
CARD_TYPE = "VISA - CREDIT - TRADITIONAL"

NUMBER_OF_CARDS = 200
# ==============================================

# داتابەیس (تەنها BINە پێویستەکان)
BIN_DATABASE = {
    "444796": {"bank": "CREDIT ONE BANK, NATIONAL ASSOCIATION", "country": "UNITED STATES 🇺🇸"},
}

def get_card_details(bin_num):
    if bin_num in BIN_DATABASE:
        return BIN_DATABASE[bin_num]
    else:
        if bin_num.startswith('4'):
            return {"bank": "Visa", "country": "Global 🌍"}
        elif bin_num.startswith('5'):
            return {"bank": "Mastercard", "country": "Global 🌍"}
        elif bin_num.startswith('3'):
            return {"bank": "Amex", "country": "Global 🌍"}
        else:
            return {"bank": "Unknown", "country": "Unknown"}

def generate_cards(bin_num, count):
    cards = []
    for _ in range(count):
        suffix = str(random.randint(0, 9999999999)).zfill(10)
        card_number = bin_num + suffix
        if len(card_number) > 16:
            card_number = card_number[:16]
        elif len(card_number) < 16:
            card_number = card_number.ljust(16, '0')
        
        month = str(random.randint(1, 12)).zfill(2)
        year = str(random.randint(24, 30))
        cvv = str(random.randint(100, 999))
        
        cards.append(f"{card_number}|{month}|{year}|{cvv}")
    return cards

CARDS_LIST = generate_cards(BIN, NUMBER_OF_CARDS)
print(f"✅ {len(CARDS_LIST)} کارت دروستکران بە BIN: {BIN}")

current_index = 0

async def send_card_message(bot, channel, admin):
    global current_index

    if not CARDS_LIST:
        await bot.send_message(chat_id=admin, text="❌ هیچ کارتێک دروست نەکراوە.")
        return False

    if current_index >= len(CARDS_LIST):
        await bot.send_message(chat_id=admin, text="✅ هەموو کارتەکان نێردران! بۆت وەستا.")
        print("✅ هەموو کارتەکان نێردران.")
        return False

    card_line = CARDS_LIST[current_index]
    parts = card_line.split('|')
    card_number = parts[0].strip()
    month = parts[1].strip()
    year = parts[2].strip()
    cvv = parts[3].strip()

    bin_num = card_number[:6]
    details = get_card_details(bin_num)
    bank = details['bank']
    country = details['country']

    card_type = CARD_TYPE if bin_num == BIN else "Unknown"

    text = (
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"  💳  KURD SCRAPPER  💳\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Card   : {card_number}\n"
        f"Exp    : {month}/{year}\n"
        f"CVV    : {cvv}\n"
        f"BIN    : {bin_num}\n"
        f"Bank   : {bank}\n"
        f"Country: {country}\n"
        f"Info   : {card_type}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Devs   : @warven_24 & @rojAmedi2"
    )

    try:
        await bot.send_message(chat_id=channel, text=text)
        await bot.send_message(chat_id=admin, text=f"✅ نێردرا ({current_index+1}/{len(CARDS_LIST)})")
        print(f"✅ نێردرا: {card_number}")
        current_index += 1
        return True
    except TelegramError as e:
        await bot.send_message(chat_id=admin, text=f"❌ هەڵە: {e}")
        return False

async def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.get_me()
    except TelegramError:
        print("⚠️ تۆکەنەکە نادروستە")
        return

    print("🚀 بۆت دەستی پێکرد. کارتەکان دەنێردرێن...")
    while True:
        result = await send_card_message(bot, CHANNEL_ID, ADMIN_ID)
        if not result:
            break
        await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
