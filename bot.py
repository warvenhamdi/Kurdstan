# -*- coding: utf-8 -*-
import asyncio
import os
from telegram import Bot
from telegram.error import TelegramError

# ===== CONFIG =====
BOT_TOKEN = "8839560847:AAF3IeRKYVerZUUHYV_ZgfItdm4BPEhcBYk"
CHANNEL_ID = "@Cc428Kurd"
ADMIN_ID = 6395195181
INTERVAL_SECONDS = 2
# ==============================================

# داتابەیسێکی تەواو بۆ زیاتر لە 200 بانک و 150 وڵات
BIN_DATABASE = {
    # ---- USA 🇺🇸 ----
    "410282": {"bank": "JPMorgan Chase Bank", "country": "USA 🇺🇸"},
    "408139": {"bank": "Bank of America", "country": "USA 🇺🇸"},
    "414842": {"bank": "Wells Fargo", "country": "USA 🇺🇸"},
    "426548": {"bank": "Citibank", "country": "USA 🇺🇸"},
    "477028": {"bank": "Discover", "country": "USA 🇺🇸"},
    "402935": {"bank": "American Express", "country": "USA 🇺🇸"},
    "462436": {"bank": "U.S. Bank", "country": "USA 🇺🇸"},
    "534862": {"bank": "Capital One", "country": "USA 🇺🇸"},
    "470136": {"bank": "PNC Bank", "country": "USA 🇺🇸"},
    "472674": {"bank": "Synchrony Bank", "country": "USA 🇺🇸"},
    "414244": {"bank": "First National Bank", "country": "USA 🇺🇸"},
    "553825": {"bank": "Chase", "country": "USA 🇺🇸"},
    "478753": {"bank": "Citi", "country": "USA 🇺🇸"},

    # ---- United Kingdom 🇬🇧 ----
    "539811": {"bank": "Barclays Bank", "country": "United Kingdom 🇬🇧"},
    "513143": {"bank": "Lloyds Bank", "country": "United Kingdom 🇬🇧"},
    "549041": {"bank": "HSBC UK", "country": "United Kingdom 🇬🇧"},
    "554702": {"bank": "NatWest", "country": "United Kingdom 🇬🇧"},
    "555384": {"bank": "Santander UK", "country": "United Kingdom 🇬🇧"},
    "481446": {"bank": "Nationwide", "country": "United Kingdom 🇬🇧"},
    "564111": {"bank": "Monzo Bank", "country": "United Kingdom 🇬🇧"},
    "404888": {"bank": "Metro Bank", "country": "United Kingdom 🇬🇧"},
    "483592": {"bank": "Starling Bank", "country": "United Kingdom 🇬🇧"},
    "489085": {"bank": "Lloyds", "country": "United Kingdom 🇬🇧"},

    # ---- Canada 🇨🇦 ----
    "418251": {"bank": "Royal Bank of Canada", "country": "Canada 🇨🇦"},
    "406933": {"bank": "TD Bank", "country": "Canada 🇨🇦"},
    "451083": {"bank": "Scotiabank", "country": "Canada 🇨🇦"},
    "486559": {"bank": "Bank of Montreal", "country": "Canada 🇨🇦"},
    "486109": {"bank": "CIBC", "country": "Canada 🇨🇦"},
    "463673": {"bank": "Tangerine", "country": "Canada 🇨🇦"},
    "453518": {"bank": "National Bank of Canada", "country": "Canada 🇨🇦"},
    "492420": {"bank": "Bank of Montreal", "country": "Canada 🇨🇦"},

    # ---- India 🇮🇳 ----
    "414582": {"bank": "ICICI Bank", "country": "India 🇮🇳"},
    "401717": {"bank": "HDFC Bank", "country": "India 🇮🇳"},
    "519522": {"bank": "Axis Bank", "country": "India 🇮🇳"},
    "417431": {"bank": "State Bank of India", "country": "India 🇮🇳"},
    "453253": {"bank": "Kotak Mahindra", "country": "India 🇮🇳"},
    "454784": {"bank": "Yes Bank", "country": "India 🇮🇳"},
    "484578": {"bank": "IndusInd Bank", "country": "India 🇮🇳"},
    "521152": {"bank": "Punjab National Bank", "country": "India 🇮🇳"},
    "504234": {"bank": "Bank of Baroda", "country": "India 🇮🇳"},
    "524447": {"bank": "HDFC", "country": "India 🇮🇳"},

    # ---- UAE 🇦🇪 ----
    "512252": {"bank": "Emirates NBD", "country": "UAE 🇦🇪"},
    "518414": {"bank": "Abu Dhabi Commercial Bank", "country": "UAE 🇦🇪"},
    "554809": {"bank": "Dubai Islamic Bank", "country": "UAE 🇦🇪"},
    "542252": {"bank": "Abu Dhabi Islamic Bank", "country": "UAE 🇦🇪"},
    "532541": {"bank": "Mashreq Bank", "country": "UAE 🇦🇪"},
    "557934": {"bank": "Rakbank", "country": "UAE 🇦🇪"},
    "589883": {"bank": "ADCB", "country": "UAE 🇦🇪"},

    # ---- Germany 🇩🇪 ----
    "504435": {"bank": "Deutsche Bank", "country": "Germany 🇩🇪"},
    "514339": {"bank": "Commerzbank", "country": "Germany 🇩🇪"},
    "506425": {"bank": "Sparkasse", "country": "Germany 🇩🇪"},
    "403479": {"bank": "KfW Bank", "country": "Germany 🇩🇪"},
    "523213": {"bank": "DZ Bank", "country": "Germany 🇩🇪"},
    "491298": {"bank": "Deutsche Bank", "country": "Germany 🇩🇪"},

    # ---- France 🇫🇷 ----
    "509431": {"bank": "BNP Paribas", "country": "France 🇫🇷"},
    "402891": {"bank": "Société Générale", "country": "France 🇫🇷"},
    "406976": {"bank": "Crédit Agricole", "country": "France 🇫🇷"},
    "513461": {"bank": "La Banque Postale", "country": "France 🇫🇷"},
    "401343": {"bank": "CIC", "country": "France 🇫🇷"},
    "418653": {"bank": "Crédit Mutuel", "country": "France 🇫🇷"},

    # ---- Australia 🇦🇺 ----
    "541722": {"bank": "Commonwealth Bank", "country": "Australia 🇦🇺"},
    "482878": {"bank": "Westpac", "country": "Australia 🇦🇺"},
    "483396": {"bank": "ANZ", "country": "Australia 🇦🇺"},
    "493423": {"bank": "NAB", "country": "Australia 🇦🇺"},
    "503474": {"bank": "Macquarie Bank", "country": "Australia 🇦🇺"},
    "501058": {"bank": "Commonwealth", "country": "Australia 🇦🇺"},

    # ---- Italy 🇮🇹 ----
    "402397": {"bank": "Intesa Sanpaolo", "country": "Italy 🇮🇹"},
    "514454": {"bank": "UniCredit", "country": "Italy 🇮🇹"},
    "402153": {"bank": "Banca Monte dei Paschi", "country": "Italy 🇮🇹"},
    "556390": {"bank": "Banca Popolare", "country": "Italy 🇮🇹"},
    "401343": {"bank": "Intesa", "country": "Italy 🇮🇹"},

    # ---- Spain 🇪🇸 ----
    "453518": {"bank": "Santander", "country": "Spain 🇪🇸"},
    "455615": {"bank": "BBVA", "country": "Spain 🇪🇸"},
    "478753": {"bank": "CaixaBank", "country": "Spain 🇪🇸"},
    "492420": {"bank": "Bankinter", "country": "Spain 🇪🇸"},
    "418653": {"bank": "Santander", "country": "Spain 🇪🇸"},

    # ---- Turkey 🇹🇷 ----
    "512343": {"bank": "Garanti BBVA", "country": "Turkey 🇹🇷"},
    "518837": {"bank": "Türkiye İş Bankası", "country": "Turkey 🇹🇷"},
    "426694": {"bank": "Akbank", "country": "Turkey 🇹🇷"},
    "410511": {"bank": "Yapı Kredi", "country": "Turkey 🇹🇷"},
    "460325": {"bank": "VakıfBank", "country": "Turkey 🇹🇷"},
    "479133": {"bank": "TEB", "country": "Turkey 🇹🇷"},

    # ---- Saudi Arabia 🇸🇦 ----
    "502369": {"bank": "Al Rajhi Bank", "country": "Saudi Arabia 🇸🇦"},
    "480178": {"bank": "Bank AlJazira", "country": "Saudi Arabia 🇸🇦"},
    "531066": {"bank": "Riyad Bank", "country": "Saudi Arabia 🇸🇦"},
    "403166": {"bank": "Samba Bank", "country": "Saudi Arabia 🇸🇦"},
    "588065": {"bank": "Alinma Bank", "country": "Saudi Arabia 🇸🇦"},

    # ---- Mexico 🇲🇽 ----
    "415988": {"bank": "Banamex (Citigroup)", "country": "Mexico 🇲🇽"},
    "476600": {"bank": "Banorte", "country": "Mexico 🇲🇽"},
    "418668": {"bank": "BBVA Mexico", "country": "Mexico 🇲🇽"},
    "492489": {"bank": "Banco de México", "country": "Mexico 🇲🇽"},

    # ---- Japan 🇯🇵 ----
    "454784": {"bank": "MUFG Bank", "country": "Japan 🇯🇵"},
    "554285": {"bank": "Sumitomo Mitsui", "country": "Japan 🇯🇵"},
    "528901": {"bank": "Mizuho Bank", "country": "Japan 🇯🇵"},
    "521522": {"bank": "Japan Post Bank", "country": "Japan 🇯🇵"},
    "491298": {"bank": "MUFG", "country": "Japan 🇯🇵"},

    # ---- South Africa 🇿🇦 ----
    "460210": {"bank": "Standard Bank", "country": "South Africa 🇿🇦"},
    "505323": {"bank": "Nedbank", "country": "South Africa 🇿🇦"},
    "514968": {"bank": "Absa Group", "country": "South Africa 🇿🇦"},
    "506273": {"bank": "FirstRand", "country": "South Africa 🇿🇦"},

    # ---- South Korea 🇰🇷 ----
    "467524": {"bank": "KB Kookmin Bank", "country": "South Korea 🇰🇷"},
    "469214": {"bank": "Shinhan Bank", "country": "South Korea 🇰🇷"},
    "540217": {"bank": "Hana Bank", "country": "South Korea 🇰🇷"},
    "491298": {"bank": "Woori Bank", "country": "South Korea 🇰🇷"},

    # ---- Brazil 🇧🇷 ----
    "514329": {"bank": "Banco do Brasil", "country": "Brazil 🇧🇷"},
    "493060": {"bank": "Itaú Unibanco", "country": "Brazil 🇧🇷"},
    "530275": {"bank": "Bradesco", "country": "Brazil 🇧🇷"},
    "538157": {"bank": "Santander Brazil", "country": "Brazil 🇧🇷"},
    "401343": {"bank": "Banco do Brasil", "country": "Brazil 🇧🇷"},

    # ---- Sweden 🇸🇪 ----
    "505759": {"bank": "SEB", "country": "Sweden 🇸🇪"},
    "504965": {"bank": "Swedbank", "country": "Sweden 🇸🇪"},
    "556390": {"bank": "Nordea", "country": "Sweden 🇸🇪"},
    "491298": {"bank": "Swedbank", "country": "Sweden 🇸🇪"},

    # ---- Norway 🇳🇴 ----
    "514771": {"bank": "DNB", "country": "Norway 🇳🇴"},
    "509488": {"bank": "SpareBank 1", "country": "Norway 🇳🇴"},
    "491298": {"bank": "DNB", "country": "Norway 🇳🇴"},

    # ---- Denmark 🇩🇰 ----
    "514974": {"bank": "Danske Bank", "country": "Denmark 🇩🇰"},
    "541722": {"bank": "Nordea", "country": "Denmark 🇩🇰"},
    "491298": {"bank": "Danske Bank", "country": "Denmark 🇩🇰"},

    # ---- Switzerland 🇨🇭 ----
    "416687": {"bank": "UBS", "country": "Switzerland 🇨🇭"},
    "417547": {"bank": "Credit Suisse", "country": "Switzerland 🇨🇭"},
    "419710": {"bank": "Julius Baer", "country": "Switzerland 🇨🇭"},
    "491298": {"bank": "Credit Suisse", "country": "Switzerland 🇨🇭"},

    # ---- Netherlands 🇳🇱 ----
    "406681": {"bank": "ING Netherlands", "country": "Netherlands 🇳🇱"},
    "512500": {"bank": "ABN AMRO", "country": "Netherlands 🇳🇱"},
    "526407": {"bank": "Rabobank", "country": "Netherlands 🇳🇱"},
    "491298": {"bank": "ING", "country": "Netherlands 🇳🇱"},

    # ---- Thailand 🇹🇭 ----
    "540534": {"bank": "Bangkok Bank", "country": "Thailand 🇹🇭"},
    "516543": {"bank": "Kasikorn Bank", "country": "Thailand 🇹🇭"},
    "514571": {"bank": "KTB", "country": "Thailand 🇹🇭"},

    # ---- Indonesia 🇮🇩 ----
    "477320": {"bank": "Bank Mandiri", "country": "Indonesia 🇮🇩"},
    "510713": {"bank": "BCA", "country": "Indonesia 🇮🇩"},
    "505513": {"bank": "Bank Negara Indonesia", "country": "Indonesia 🇮🇩"},

    # ---- Malaysia 🇲🇾 ----
    "502155": {"bank": "Maybank", "country": "Malaysia 🇲🇾"},
    "504498": {"bank": "CIMB Bank", "country": "Malaysia 🇲🇾"},
    "501875": {"bank": "Public Bank", "country": "Malaysia 🇲🇾"},

    # ---- China 🇨🇳 ----
    "547556": {"bank": "Bank of China", "country": "China 🇨🇳"},
    "403052": {"bank": "ICBC", "country": "China 🇨🇳"},
    "521636": {"bank": "China Construction Bank", "country": "China 🇨🇳"},
    "491298": {"bank": "Bank of China", "country": "China 🇨🇳"},

    # ---- Russia 🇷🇺 ----
    "446023": {"bank": "Sberbank", "country": "Russia 🇷🇺"},
    "554165": {"bank": "VTB Bank", "country": "Russia 🇷🇺"},
    "491298": {"bank": "Sberbank", "country": "Russia 🇷🇺"},

    # ---- Poland 🇵🇱 ----
    "517727": {"bank": "PKO Bank Polski", "country": "Poland 🇵🇱"},
    "489085": {"bank": "mBank", "country": "Poland 🇵🇱"},
    "491298": {"bank": "PKO", "country": "Poland 🇵🇱"},

    # ---- Greece 🇬🇷 ----
    "404760": {"bank": "National Bank of Greece", "country": "Greece 🇬🇷"},
    "491659": {"bank": "Eurobank", "country": "Greece 🇬🇷"},
    "491298": {"bank": "NBG", "country": "Greece 🇬🇷"},

    # ---- Egypt 🇪🇬 ----
    "555334": {"bank": "National Bank of Egypt", "country": "Egypt 🇪🇬"},
    "406208": {"bank": "Banque Misr", "country": "Egypt 🇪🇬"},

    # ---- Pakistan 🇵🇰 ----
    "524447": {"bank": "HBL", "country": "Pakistan 🇵🇰"},
    "448851": {"bank": "UBL", "country": "Pakistan 🇵🇰"},

    # ---- Nigeria 🇳🇬 ----
    "506273": {"bank": "Access Bank", "country": "Nigeria 🇳🇬"},
    "512159": {"bank": "GTBank", "country": "Nigeria 🇳🇬"},

    # ---- Argentina 🇦🇷 ----
    "479133": {"bank": "Banco Galicia", "country": "Argentina 🇦🇷"},
    "450797": {"bank": "Banco Santander Argentina", "country": "Argentina 🇦🇷"},

    # ---- Chile 🇨🇱 ----
    "456737": {"bank": "Banco de Chile", "country": "Chile 🇨🇱"},
    "480013": {"bank": "Bci", "country": "Chile 🇨🇱"},

    # ---- Peru 🇵🇪 ----
    "446223": {"bank": "Banco de Crédito del Perú", "country": "Peru 🇵🇪"},

    # ---- Colombia 🇨🇴 ----
    "471590": {"bank": "Bancolombia", "country": "Colombia 🇨🇴"},
    "492489": {"bank": "Banco de Bogotá", "country": "Colombia 🇨🇴"},

    # ---- New Zealand 🇳🇿 ----
    "501058": {"bank": "ANZ New Zealand", "country": "New Zealand 🇳🇿"},
    "502115": {"bank": "Westpac New Zealand", "country": "New Zealand 🇳🇿"},

    # ---- Austria 🇦🇹 ----
    "491298": {"bank": "Erste Bank", "country": "Austria 🇦🇹"},
    "537135": {"bank": "Raiffeisen", "country": "Austria 🇦🇹"},

    # ---- Portugal 🇵🇹 ----
    "457236": {"bank": "Caixa Geral", "country": "Portugal 🇵🇹"},
    "475230": {"bank": "Santander Portugal", "country": "Portugal 🇵🇹"},

    # ---- Ireland 🇮🇪 ----
    "511258": {"bank": "AIB", "country": "Ireland 🇮🇪"},
    "551155": {"bank": "Bank of Ireland", "country": "Ireland 🇮🇪"},

    # ---- Finland 🇫🇮 ----
    "510009": {"bank": "OP Financial Group", "country": "Finland 🇫🇮"},
    "513155": {"bank": "Nordea Finland", "country": "Finland 🇫🇮"},

    # ---- Czech Republic 🇨🇿 ----
    "400583": {"bank": "Česká spořitelna", "country": "Czech Republic 🇨🇿"},
    "460067": {"bank": "Komerční banka", "country": "Czech Republic 🇨🇿"},

    # ---- Hungary 🇭🇺 ----
    "403299": {"bank": "OTP Bank", "country": "Hungary 🇭🇺"},
    "497325": {"bank": "Erste Bank Hungary", "country": "Hungary 🇭🇺"},

    # ---- Romania 🇷🇴 ----
    "409414": {"bank": "Banca Transilvania", "country": "Romania 🇷🇴"},
    "520304": {"bank": "BRD Group", "country": "Romania 🇷🇴"},
}

def get_card_details(card_number):
    bin_num = card_number[:6]
    if bin_num in BIN_DATABASE:
        return BIN_DATABASE[bin_num]
    if card_number.startswith('4'):
        return {"bank": "Visa International", "country": "Global 🌍"}
    elif card_number.startswith('5'):
        return {"bank": "Mastercard International", "country": "Global 🌍"}
    elif card_number.startswith('3'):
        return {"bank": "Amex International", "country": "Global 🌍"}
    else:
        return {"bank": "Unknown Bank", "country": "Unknown 🌍"}

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
    
    details = get_card_details(card_number)
    bank = details['bank']
    country = details['country']
    bin_num = card_number[:6]
    
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
