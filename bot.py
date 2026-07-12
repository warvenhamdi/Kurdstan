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
NUMBER_OF_CARDS = 10000
# ==============================================

# 🔹 لیستی 12 BINەکان
BINS_INFO = [
    {"bin": "517949", "bank": "CITIBANK N.A.", "country": "UNITED STATES [US] 🇺🇸", "type": "MASTERCARD - PLATINUM - CREDIT"},
    {"bin": "457826", "bank": "DUBAI ISLAMIC BANK", "country": "UNITED ARAB EMIRATES 🇦🇪", "type": "VISA - PLATINUM - DEBIT"},
    {"bin": "530232", "bank": "SUMITOMO MITSUI CARD COMPANY", "country": "JAPAN 🇯🇵", "type": "MASTERCARD - GOLD - CREDIT"},
    {"bin": "512676", "bank": "PT. BANK MANDIRI (PERSERO) TBK", "country": "INDONESIA 🇮🇩", "type": "MASTERCARD - STANDARD - CREDIT"},
    {"bin": "532162", "bank": "TN CYBERTECH BANK LIMITED", "country": "ZIMBABWE 🇿🇼", "type": "MASTERCARD - DEBIT - STANDARD"},
    {"bin": "426684", "bank": "JPMORGAN CHASE BANK N.A.", "country": "UNITED STATES 🇺🇸", "type": "VISA - CREDIT - TRADITIONAL"},
    {"bin": "418966", "bank": "EMIRATES ISLAMIC BANK P.J.S.C.", "country": "UNITED ARAB EMIRATES [AE] 🇦🇪", "type": "VISA - CREDIT - PLATINUM"},
    {"bin": "415656", "bank": "BAHRAIN ISLAMIC BANK BSC", "country": "BAHRAIN [BH] 🇧🇭", "type": "VISA - CREDIT - SIGNATURE"},
    {"bin": "455633", "bank": "PT. BANK CENTRAL ASIA TBK", "country": "INDONESIA 🇮🇩", "type": "VISA - CREDIT - PLATINUM"},
    {"bin": "529415", "bank": "THE SAUDI NATIONAL BANK", "country": "SAUDI ARABIA 🇸🇦", "type": "MASTERCARD - DEBIT - STANDARD"},
    {"bin": "513338", "bank": "UNKNOWN BANK", "country": "GLOBAL 🌍", "type": "MASTERCARD - UNKNOWN - CREDIT"},
    {"bin": "502725", "bank": "UNKNOWN BANK", "country": "GLOBAL 🌍", "type": "MASTERCARD - UNKNOWN - CREDIT"},
]

def generate_cards(bins_data, count):
    cards = []
    seen_numbers = set() # بۆ پشکنینی دووبارەبوونەوە
    
    while len(cards) < count:
        selected_bin = random.choice(bins_data)
        bin_num = selected_bin["bin"]
        bank = selected_bin["bank"]
        country = selected_bin["country"]
        card_type = selected_bin["type"]

        random_part = str(random.randint(0, 999999999)).zfill(9)
        partial_card = bin_num + random_part
        card_number = append(partial_card)

        # پشکنینی دووبارەبوونەوە
        if card_number in seen_numbers:
            continue

        seen_numbers.add(card_number)
        
        # 🔹 گۆڕانکاری ساڵ و مانگ بەپێی داواکەت
        year = str(random.randint(2026, 2032))
        if year == "2026":
            # تەنها بۆ ساڵی 2026، مانگ 8 بۆ 12
            month = str(random.randint(8, 12)).zfill(2)
        else:
            # بۆ ساڵەکانی 2027-2032، مانگ 1 بۆ 12
            month = str(random.randint(1, 12)).zfill(2)
        
        cvv = str(random.randint(100, 999))

        cards.append({
            "card_number": card_number,
            "month": month, "year": year, "cvv": cvv,
            "bank": bank, "country": country, "type": card_type
        })
    return cards

CARDS_LIST = generate_cards(BINS_INFO, NUMBER_OF_CARDS)
print(f"✅ {len(CARDS_LIST)} کارتی تەواو جیاواز (بە 12 BIN) دروستکران.")

current_index = 0

async def send_card_message(bot, channel, admin):
    global current_index
    if current_index >= len(CARDS_LIST):
        await bot.send_message(chat_id=admin, text="✅ بۆت تەواو بوو! هەموو کارتەکان نێردران.")
        print("✅ بۆت تەواو بوو! هەموو کارتەکان نێردران.")
        return False

    card_data = CARDS_LIST[current_index]
    text = f"{card_data['card_number']}|{card_data['month']}|{card_data['year']}|{card_data['cvv']}\nBank: {card_data['bank']}\nCountry: {card_data['country']}\nType: {card_data['type']}"

    while True:
        try:
            await bot.send_message(chat_id=channel, text=text)
            print(f"✅ نێردرا ({current_index+1}/{len(CARDS_LIST)})")
            current_index += 1
            return True
        except TelegramError as e:
            err_msg = str(e)
            if "Flood control" in err_msg:
                match = re.search(r"Retry in (\d+)", err_msg)
                wait_time = int(match.group(1)) if match else 30
                print(f"⚠️ Flood control. چاوەڕوانی {wait_time} چرکە...")
                await asyncio.sleep(wait_time)
            else:
                print(f"❌ هەڵە: {err_msg}")
                return False

async def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.get_me()
    except TelegramError:
        print("⚠️ تۆکەنەکە نادروستە")
        return

    print(f"🚀 بۆت دەستی پێکرد بۆ ناردنی {NUMBER_OF_CARDS} کارت (ساڵ 26-32، 2026 مانگ 8-12)...")
    while True:
        result = await send_card_message(bot, CHANNEL_ID, ADMIN_ID)
        if not result:
            break
        await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
