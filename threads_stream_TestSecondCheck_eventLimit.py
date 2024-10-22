import requests
import time
import json
import datetime
from threading import Thread, Lock

#XXX 10 SEC FOUND TIME APPROXI<ALTY
import pyautogui as pag

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
import pyautogui as pag

import pickle
from selenium.webdriver.chrome.service import Service
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


def buy_script(url):
    driver.get(url)
    time.sleep(0.125)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#modal-root > div > div > div > div.Modal__body > div > div.ModalNftBuy__inner > div.NftPageBuyButton > button > div > div > div'))).click()
    # time.sleep(0.025)
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#modal-root > div.Modal.ModalDeployStatusContainer.Modal--shown.Modal--type-page.Modal--mode-fullscreen.Modal--default-width > div > div > div > div > div > div > div.ProgressList__wrapper > div.ProgressList__content > div:nth-child(1) > div.ProgressStep__content > div.ModalTonTx__bottom-wrapper > a > div > div > div'))).click()
    # time.sleep(0.666)
    # pag.click(x=-580, y=238, clicks=3, interval=0.035, button='left')

    # Confirm button in wallet LG center position
    # confirm_x, confirm_y = 890,800
    # verify_x,verify_y = 866, 839

    # confirm transaction on philips(need to adjust each time)
    
    
    
    #(103, 172, 239)(-249,  965) Saved wallet possion on philips 
    
    #XXX
    confirm_x, confirm_y = -249,  965
    verify_x,verify_y = -251, 1006

    while True:
        color = pag.pixel(confirm_x,confirm_y)
        #need to adjust each time color   
        if color != (103, 172, 239):
            time.sleep(0.015)
        else:
            break                            # 
    pag.click(x=confirm_x, y=confirm_y, clicks=1, interval=0.035, button='left')
    
    pag.moveTo(x=verify_x, y=verify_y)
    # sleep(0.4)
    while True:
        color = pag.pixel(verify_x, verify_y)   
        if color != (82, 136, 193):
            time.sleep(0.015)
        else:
            break
    pag.click(x=verify_x, y=verify_y, clicks=1, interval=1, button='left')
    time.sleep(0.2)
    pag.click(x=verify_x, y=verify_y, clicks=1, interval=1, button='left')

def second_check(n,i,lock):
    if len(non_checked_acc) > 0:
        time.sleep(4)
    # print('Thread has been started.')
        # print(f'проверка не сработаных акков: {len(non_checked_acc)}')
        res = requests.get(f'https://tonapi.io/v2/blockchain/accounts/{i[0]}/methods/get_sale_data', headers=headers)
        if res.status_code == 200:
            response = res.json()
            try:
                if response['decoded']['royalty_address'] == '0:ed53bc999e5a4af69a3f9c3de5376f7d90c487e1528f331e716dbe85903d5112':
                    with lock:
                        non_checked_acc.pop(n)
                    created_at = response['decoded']['created_at']
                    price = int(response['decoded']['full_price'])/1e9
                    nft_addr = response['decoded']['nft']
                    is_complete = response['decoded']['is_complete']
                    dt = str(datetime.datetime.fromtimestamp(created_at))
                    timeNow = str(datetime.datetime.now())[:-7]
                    # print(f'Account CHECK OK: {i[0]}')
                    # print(dt)
                    # print(timeNow)
                    # if created_at < int(time.time()) + 10 and price < 7:
                    if price < 7.8:
                        # print(f'Price: {price}', f'\nCreated at: {dt:>16}\n  Found at: {timeNow:>16}', f'\nNFT ADD: {nft_addr}\nIs_complete: {is_complete}')
                    # print(response)
                        #NFT INFO
                        #raw to friendly
                        link = requests.get(f'https://toncenter.com/api/v2/packAddress?address={nft_addr}')
                        addressContract2 = link.json()['result'].replace('/','_')
                        addressCollection1 = 'EQDmkj65Ab_m0aZaW8IpKw4kYqIgITw_HRstYEkVQ6NIYCyW'
                        url = 'https://getgems.io/collection/'+str(addressCollection1)+'/'+str(addressContract2)+'?modalNft='+str(addressContract2)+'&modalId=nft_buy'
                        print(url)
                        res = requests.get(f'https://tonapi.io/v2/nfts/{nft_addr}', headers=headers)
                        nft_res = res.json()
                        
                        if 'sale' in nft_res:
                            print(f'[Thread]\nPrice: {price}', f'\nCreated at: {dt:>16}\n  Found at: {timeNow:>16}', f'\nNFT ADD: {nft_addr}\nIs_complete: {is_complete}')
                            msg = f'Price: {price}\nCreated at: {dt:>16}\n   Found at: {timeNow:>16}\nNFT ADD: {nft_addr}\nIs_complete: {is_complete}'
                            tg_sendMsg(msg, ps='\n\nthreads_stream_eventLimit.py')
                        # buy_script(url)
                        exit()
            except Exception as e:
                # print("Exception: ", e)
                i[1] += 1
                if i[1] > 2:
                    try:
                        with lock:
                            non_checked_acc.pop(n)
                        # print(f'Success pop #{n}')
                    except:
                        pass
                    pass
        else:
            i[1] += 1
            # print('res.status_code')
            if i[1] > 2:
                with lock:
                    non_checked_acc.pop(n)
                # print(f'Success pop #{n}')
    



def fetch_url(url):
    res = requests.get(f'https://tonapi.io/v2/blockchain/accounts/{url}/methods/get_sale_data', headers=headers)
    if res.status_code == 200:
        response = res.json()
        try:
            if response['decoded']['royalty_address'] == '0:ed53bc999e5a4af69a3f9c3de5376f7d90c487e1528f331e716dbe85903d5112':
                created_at = response['decoded']['created_at']
                price = int(response['decoded']['full_price'])/1e9
                # print(f'Account OK: {i}')
                # if created_at < int(time.time()) + 10 and price < 7:
                if price < 7.8:
                    nft_addr = response['decoded']['nft']
                    is_complete = response['decoded']['is_complete']
                    dt = str(datetime.datetime.fromtimestamp(created_at))
                    timeNow = str(datetime.datetime.now())[:-7]
                    # print(f'Price: {price}', f'\nCreated at: {dt:>16}\n  Found at: {timeNow:>16}', f'\nNFT ADD: {nft_addr}\nIs_complete: {is_complete}')
                # print(response)
                    #NFT INFO
                    link = requests.get(f'https://toncenter.com/api/v2/packAddress?address={nft_addr}')
                    addressContract2 = link.json()['result'].replace('/','_')
                    addressCollection1 = 'EQDmkj65Ab_m0aZaW8IpKw4kYqIgITw_HRstYEkVQ6NIYCyW'
                    url = 'https://getgems.io/collection/'+str(addressCollection1)+'/'+str(addressContract2)+'?modalNft='+str(addressContract2)+'&modalId=nft_buy'
                    print(url)
                    
                    res = requests.get(f'https://tonapi.io/v2/nfts/{nft_addr}', headers=headers)
                    nft_res = res.json()
                    if 'sale' in nft_res:
                        print(f'Price: {price}', f'\nCreated at: {dt:>16}\n  Found at: {timeNow:>16}', f'\nNFT ADD: {nft_addr}\nIs_complete: {is_complete}')
                        msg = f'Price: {price}\nCreated at: {dt:>16}\n   Found at: {timeNow:>16}\nNFT ADD: {nft_addr}\nIs_complete: {is_complete}'
                        tg_sendMsg(msg, ps='\n\nthreads_stream_eventLimit.py')
                    # buy_script(url)
                    exit()
        except Exception as e:
            # print("Exception: ", e)
            # print('Status code: ',res.status_code)
            # print(f'Account False: {i}')
            # print(str(datetime.datetime.now())[:-7])
            non_checked_acc.append([url,0])
            pass
    
    else:
        # print('Status code: ',res.status_code)
        # print(f'Account False: {i}')
        # print(str(datetime.datetime.now())[:-7])
        non_checked_acc.append([url,0])


options = Options()
options.page_load_strategy ='none'
options.add_experimental_option("detach", True)
# options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
# options.add_argument("--user-data-dir=chrome-data")
s=Service('C:/Python311/Lib/site-packages/selenium/webdriver/common/windows/chromedriver.exe')
driver = webdriver.Chrome(service=s, options=options)
# driver = webdriver.Chrome(options=options)
driver.get('https://getgems.io/collection/EQDmkj65Ab_m0aZaW8IpKw4kYqIgITw_HRstYEkVQ6NIYCyW?filter=%7B%22saleType%22%3A%22fix_price%22%7D')
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
driver.refresh()
# pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

driver.set_window_position(-1014, 266, windowHandle='current')
driver.maximize_window()

wait = WebDriverWait(driver,5,0.025)


lock = Lock()

addr_list = []

while True:
    time.sleep(1)
    res = requests.get(f'https://tonapi.io/v2/accounts/0:0816e9c02d110e790f7db3231b3bab12cccfc56b546c3c3e530684b4a9578a43/events?limit=10', headers=headers)
    response = res.json()
    if res.status_code != 200:
        time.sleep(3)
        continue
    for i in range(10):
        st_all = time.time()
        try:
            contract_addr = response['events'][i]['actions'][1]['SmartContractExec']['contract']['address']
            addr_list.append(contract_addr)
        except KeyError:
            pass
        except IndexError:
            pass
    print('new Data')
    # if len(non_checked_acc) > 0:
    urls = [i for i in non_checked_acc]
    threads = [Thread(target=second_check, args=(n,url,lock,)) for n,url in enumerate(urls)]
    st = time.time()
    for thread in threads:
        thread.start()
    # print('Thread has been started.')
    print(f'проверка не сработаных акков: {len(non_checked_acc)}')
    # print([i[0][:7] for i in non_checked_acc])
    
    # non_checked_acc.clear()
    # print(non_checked_acc)
    end = time.time() - st
    # print('Threads cycle: ', end)

    st = time.time()
    
    # print(event_data['accounts'])
    urls = [i for i in addr_list]
    threads_main = [Thread(target=fetch_url, args=(url,)) for url in urls]
    addr_list = []
    for thread in threads_main:
        thread.start()
    for thread in threads_main:
        thread.join()
        #NFT SALE CONTRACT info with price
    end = time.time() - st
    print('Main cycle: ', end)   
# for thread in threads:
#     thread.join()
        
end_all = time.time() - st_all
# print(f'All cycle: {end_all}')
