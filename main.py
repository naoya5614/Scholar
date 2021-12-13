import googlemaps
import pprint
import numpy as np
import pandas as pd
import tkinter as tk

import googlemaps
import pprint


def close_window():
    baseGround.quit()


baseGround = tk.Tk()
# GUIの画面サイズ
baseGround.geometry('500x300')
#GUIの画面タイトル
baseGround.title('近くの◯◯検索')
label1 = tk.Label(baseGround, text="調べたいキーワード")
label1.pack()
text1 = tk.Entry(width=30)
text1.pack()
label2 = tk.Label(baseGround, text="基準点となるGoogleマップのurlを貼り付ける")
label2.pack()
text2 = tk.Entry(width=30)
text2.pack()
label3 = tk.Label(baseGround, text="半径何kmを検索しますか")
label3.pack()
text3 = tk.Entry(width=30)
text3.pack()
label4 = tk.Label(baseGround, text="ファイル名を決めてください")
label4.pack()
text4 = tk.Entry(width=30)
text4.pack()
# ボタン
btn = tk.Button(baseGround, text='検索', command=close_window)
btn.pack()

#表示
baseGround.mainloop()

keyword = text1.get()
google_url = text2.get()

div = text3.get()
#stringからfloatに
div = float(div)

excel_name = text4.get()



key = 'AIzaSyAYGY0QoNaeF77iIa4aEYbAbrSOotaVouA'
client = googlemaps.Client(key)

# 基準になる位置情報
base_location = google_url.split('/')

# 軽度・緯度の情報
loc = base_location[6][1:-1]
loc = loc.split(',')
loc = {'lat': loc[0], 'lng': loc[1] }

#半径◯◯㎞以内の距離
div = int(10000*div)

#検索キーワード
keyword = "'" + keyword + "'"

#place_id情報を取得
place_results = client.places_nearby(location=loc, radius=div, keyword=keyword,language='ja')


# 検索結果の詳細情報を取得
name_list = []
vicinity_list = []
phone_num_list = []
url_list = []
opening_list = []
post_list = []



for i in place_results['results']: 
    place_detail = client.place(place_id=i['place_id'],language='ja') 
    name = place_detail['result']['name']

    try: 
        vicinity = place_detail['result']['vicinity'] 
    except:
        vicinity = ''  
        pass

    try: 
        phone_num = place_detail['result']['formatted_phone_number'] 
    except:
        phone_num = ''  
        pass

    try: 
        url = place_detail['result']['website'] 
    except:
        url = ''  
        pass

    try: 
        opening = place_detail['result']['opening_hours']['weekday_text']
    except:
        opening = ''  
        pass

    try: 
        post = place_detail['result']['address_components'][-1]['long_name'] 
    except:
        post = ''  
        pass


    name_list.append(name)
    vicinity_list.append(vicinity)
    phone_num_list.append(phone_num)
    url_list.append(url)
    opening_list.append(opening)
    post_list.append(post)


df = pd.DataFrame({'店名': name_list,
                    '電話番号': phone_num_list,
                    '郵便番号': post_list,
                    '住所': vicinity_list,
                    '営業時間': opening_list,
                    'website': url_list,
                    })


excel_name = excel_name + '.xlsx'
print(excel_name)

df.to_excel(excel_name, index=False)

finalGround = tk.Tk()
# GUIの画面サイズ
finalGround.geometry('200x200')
#GUIの画面タイトル
finalGround.title('近くの◯◯検索')

# ボタン
btn_1 = tk.Button(finalGround, text='保存しました', command=close_window)
btn_1.pack()

#表示
finalGround.mainloop()