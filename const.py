import emoji

HEADER_IMG_URL = "https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg"

STEAM_APPDETAIL_URL = "https://store.steampowered.com/api/appdetails?appids={appid}&cc={region}&l=en"

IR_CURRENCY_CODE = "IRR"
EXCHANGE_CURRENCY_URL = "https://freecurrencyapi.net/api/v2/latest?base_currency={currency_code}&apikey={key}"
REGION_CURRENCY_CODES = {
    "ru": "RUB",
    "ar": "ARS",
    "tr": "TRY"
}

REGION_EMOJIS = {
    "ru": "🇷🇺",
    "ar": "🇦🇷",
    "tr": "🇹🇷",
}
