from regex import I
import requests
import time
import json
import datetime
from threading import Thread
import os

TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_ChatID = os.getenv('TG_ChatID')


def tg_sendMsg(
    msg: str | list = "no message",
    TOKEN=TG_BOT_TOKEN,
    chat_id=TG_ChatID,
    ps = "",
    *,
    sep_msg: bool = False,
) -> str:

    """send message via telegram api(url)\n
    url = (
        f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}"
    )"""
    # TOKEN = TOKEN
    # chat_id = chat_id
    _ps = ps
    isStr = type(msg) is str
    if isStr:
        msg = msg + _ps
    elif sep_msg and type(msg) == list:
        for m in msg:
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={m + _ps}"
            requests.get(url).json()
        return True
    elif not sep_msg and type(msg) != str:
        msg = " \n".join([m for m in msg]) + _ps
    url = (
        f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}"
    )
    requests.get(url).json()


headers = {
    "accept": "*/*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6",
    "authorization": "Bearer AFPJTKEBPOX3AIYAAAAKA2HWOTRNJP5MUCV5DMDCZAAOCPSAYEYS3CILNQVLF2HWKED6USY",
    "content-type": "application/json",
    "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site"
}

non_checked_acc = []

url = "https://tonapi.io/v2/sse/accounts/traces?accounts=EQAIFunALREOeQ99syMbO6sSzM_Fa1RsPD5TBoS0qVeKQ-AR&token=AFPJTKEBPOX3AIYAAAAKA2HWOTRNJP5MUCV5DMDCZAAOCPSAYEYS3CILNQVLF2HWKED6USY"
#stream accounts  https://tonviewer.com/EQAIFunALREOeQ99syMbO6sSzM_Fa1RsPD5TBoS0qVeKQ-AR
response = requests.get(url, stream=True)

for line in response.iter_lines():
    if line.startswith(b'data:'):
        # Если строка начинается с 'data:', это строка данных
        # Извлеките данные и разберите их как JSON
        data_json = line.split(b':', 1)[1].strip()
        if data_json:
            event_data = json.loads(data_json)
            # print(event_data['accounts'])
            for i in event_data['accounts']:
                Sale_addr = i
                #NFT SALE CONTRACT info with price
                res = requests.get(f'https://tonapi.io/v2/blockchain/accounts/{Sale_addr}/methods/get_sale_data', headers=headers)
                if res.status_code == 200:
                    response = res.json()
                    try:
                        if response['decoded']['royalty_address'] == '0:ed53bc999e5a4af69a3f9c3de5376f7d90c487e1528f331e716dbe85903d5112':
                            created_at = response['decoded']['created_at']
                            price = int(response['decoded']['full_price'])/1e9
                            print(f'Account OK: {i}')
                            # # if created_at < int(time.time()) + 10 and price < 7:
                            # if price < 7:
                            #     nft_addr = response['decoded']['nft']
                            #     is_complete = response['decoded']['is_complete']
                            #     dt = str(datetime.datetime.fromtimestamp(created_at))
                            #     timeNow = str(datetime.datetime.now())[:-7]
                            #     # print(f'Price: {price}', f'\nCreated at: {dt:>16}\n  Found at: {timeNow:>16}', f'\nNFT ADD: {nft_addr}\nIs_complete: {is_complete}')
                            # # print(response)
                            #     #NFT INFO
                            #     res = requests.get(f'https://tonapi.io/v2/nfts/{nft_addr}', headers=headers)
                            #     nft_res = res.json()
                            #     if 'sale' in nft_res:
                            #         print(f'Price: {price}', f'\nCreated at: {dt:>16}\n  Found at: {timeNow:>16}', f'\nNFT ADD: {nft_addr}\nIs_complete: {is_complete}')
                            #         msg = f'Price: {price}\nCreated at: {dt:>16}\n   Found at: {timeNow:>16}\nNFT ADD: {nft_addr}\nIs_complete: {is_complete}'
                            #         tg_sendMsg(msg, ps='\n\nstream_acc.py')
                    except Exception as e:
                        # print("Exception: ", e)
                        pass
                
                else:
                    print('Status code: ',res.status_code)
                    print(f'Account False: {i}')
                    non_checked_acc.append(i)
                    break
print(f'проверка не сработаных акков: {len(non_checked_acc)}')
for i in non_checked_acc:
    res = requests.get(f'https://tonapi.io/v2/blockchain/accounts/{Sale_addr}/methods/get_sale_data', headers=headers)
    if res.status_code == 200:
        response = res.json()
        try:
            if response['decoded']['royalty_address'] == '0:ed53bc999e5a4af69a3f9c3de5376f7d90c487e1528f331e716dbe85903d5112':
                created_at = response['decoded']['created_at']
                price = int(response['decoded']['full_price'])/1e9
                print(f'Account CHECK OK: {i}')
                # # if created_at < int(time.time()) + 10 and price < 7:
                # if price < 7:
                #     nft_addr = response['decoded']['nft']
                #     is_complete = response['decoded']['is_complete']
                #     dt = str(datetime.datetime.fromtimestamp(created_at))
                #     timeNow = str(datetime.datetime.now())[:-7]
                #     # print(f'Price: {price}', f'\nCreated at: {dt:>16}\n  Found at: {timeNow:>16}', f'\nNFT ADD: {nft_addr}\nIs_complete: {is_complete}')
                # # print(response)
                #     #NFT INFO
                #     res = requests.get(f'https://tonapi.io/v2/nfts/{nft_addr}', headers=headers)
                #     nft_res = res.json()
                #     if 'sale' in nft_res:
                #         print(f'Price: {price}', f'\nCreated at: {dt:>16}\n  Found at: {timeNow:>16}', f'\nNFT ADD: {nft_addr}\nIs_complete: {is_complete}')
                #         msg = f'Price: {price}\nCreated at: {dt:>16}\n   Found at: {timeNow:>16}\nNFT ADD: {nft_addr}\nIs_complete: {is_complete}'
                #         tg_sendMsg(msg, ps='\n\nstream_acc.py')
        except Exception as e:
            # print("Exception: ", e)
            pass
    else:
        print('res.status_code')