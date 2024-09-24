#抓取这些用户列表的内容
import os
import time

user_list = [
    # 'Aug_Ending',
    # 'edenivys',
    # 'Sweet_BunnyXXX',
    # 'Vdsx2x',
    # 'MissBNasty',
    # 'violetsaucy',
    # 'sophiedee',
    # 'lenatheplug',
    # 'ANGELAWHITE',
    # 'PornDudeCasting',
    # 'amateurporn99',
    # 'Figen46747356',
    # 'Hentai_TL',
    # 'FinestOfLeaks',
    # 'lovelyxladies',
    # 'KinkyClipsFH',
    'kizpornosex',
    'pleasureheat',
    'yourscompIetely',
    'AnissaKate',
    'welovepornhub'
]
# user_list = user_list[:2]
print(user_list)
count = 500
for user in user_list:
    cmd = f'python3.11 scraper -t {count} -u {user}'
    result = os.system(cmd)
    print(f"result {user}:", result)
    time.sleep(60)
