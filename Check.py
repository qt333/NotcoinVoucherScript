from regex import I
import requests
import time
import json
import datetime

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

non_checked_acc = ['0:c6b36a4a2d896e4ded82f8da191806c973645a01db115a2e72fb021301d1e894','0:c9d47e599149d27d0e79e1d80d735d06bd394c6c137fbbbe9db25109e778f406','0:3291822b3bad7219fdbae9c4dc5bf133af65b2d2d93ade88a8d19a825f8817b5']

for i in non_checked_acc:
    res = requests.get(f'https://tonapi.io/v2/blockchain/accounts/{i}/methods/get_sale_data', headers=headers)
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