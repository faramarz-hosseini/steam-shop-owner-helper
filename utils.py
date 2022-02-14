import os
from typing import Dict

import requests
import const


def get_steam_game_image_url(app_id: str):
    return const.HEADER_IMG_URL.format(appid=app_id)


# TODO: Apply async-await
def get_game_prices(app_id: str) -> Dict[str, float]:
    currency_to_rial = {k: {} for k, v in const.REGION_CURRENCY_CODES.items()}
    price_req = requests.get(
        const.EXCHANGE_CURRENCY_URL.format(currency_code="USD", key=os.environ.get('apikey'))
    )
    usd_to_toman = get_live_usd_to_irr()
    for region, currency_code in const.REGION_CURRENCY_CODES.items():
        appdetail_req = requests.get(
            const.STEAM_APPDETAIL_URL.format(appid=app_id, region=region)
        )
        if appdetail_req.json()[app_id]['success']:
            game_prices = appdetail_req.json()[app_id]['data']['package_groups'][0]['subs']
            for price_info in game_prices:
                buy_option = price_info['option_text'].split('-')[0].rstrip()
                price = price_info['price_in_cents_with_discount'] / 100
                currency_to_rial[region][buy_option] = \
                    (price / int(price_req.json()['data'][currency_code])) * usd_to_toman
        else:
            currency_to_rial[region][" "] = "در این ریجن موجود نمیباشد"

    return currency_to_rial


# TODO: Heavy improvements on this one
def generate_caption(price_dict):
    caption = ""
    for region, price_infos in price_dict.items():
        caption += const.REGION_EMOJIS[region]+":\n"
        for option, price in price_infos.items():
            modified_price = str(int(price))+"T" if is_number(price) else price
            caption += option+": "+str(modified_price)+"\n"
    return caption


def get_live_usd_to_irr():
    req = requests.get("https://api.nobitex1.ir/v2/crypto-prices").json()
    return req['params']['USDTIRT'] / 10


def is_number(inp):
    try:
        int(inp)
    except ValueError:
        return False
    return True


def parse_currency(currency_string):
    return int(''.join(chr for chr in currency_string if is_number(chr))) / 100
