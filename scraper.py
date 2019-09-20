import re
import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query


BASE_URL = 'http://bbs.skykiwi.com/'
GENERAL_FILTER = 'forum.php?mod=forumdisplay&fid=19&orderby=dateline&filter=sortid&sortid=287' # 基于发帖时间排序,只看出租
LOCATION_FILTER = {
    'central': '&filter=typeid&typeid=38',
    'northshore': '&filter=typeid&typeid=37'
}

KEYWORD = ['dominion', '倒霉', 'eden', 'birkenhead', 'glenfield']
DEPTH = 30

db = TinyDB('entry.json')
room = Query()

def get_soup(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_time(soup):
    try:
        time = soup.select_one('em[id^="authorposton"] > span')
        if time == None:
            time = soup.select_one('em[id^="authorposton"]').get_text().split('发表于 ')[1]
        else:
            time = time.get('title')
        return time
    except:
        return None

def get_price(soup):
    try: 
        price = soup.select_one('div.table-container > table > tr:nth-of-type(2) > td:nth-of-type(2)')
        if price == None:
            price = soup.select_one('td[id^="postmessage"]').get_text()
            price = float(re.findall(r'NZD\$\d+.\d+', price)[0].split('$')[1])
        else:
            price = float(price.get_text().split(' ')[0])
        return price
    except:
        return None

def get_room_type(soup):
    try:
        room_type = soup.select_one('div.table-container > table > tr:nth-of-type(1) > td:nth-of-type(2)')
        if room_type == None:
            room_type = soup.select_one('td[id^="postmessage"]').get_text()
            room_type = re.findall(r'房屋类型.*', room_type)[0].split(':')[1]
        else:
            room_type = room_type.get_text()
        return room_type
    except:
        return None

def save_entry(entries, location):
    repeating = False
    for entry in entries:
        body = entry.find('th', class_=['common', 'new']).find('a', recursive=False)
        description = body.get_text()
        if any([word in description.lower() for word in KEYWORD]):
            link = BASE_URL + body.get('href')
            id = re.findall(r'tid=\d+', link)[0].split('=')[1]
            if db.get(room.id == id) != None:
                repeating = True
                break
            threadSoup = get_soup(link)
            price = get_price(threadSoup)
            time = get_time(threadSoup)
            room_type = get_room_type(threadSoup)
            db.insert({
                'id': id,
                'description' : description,
                'location': location,
                'price': price,
                'time': time,
                'room_type': room_type
            })
    return repeating

def main():
    print('Start scraping...')
    for location in LOCATION_FILTER:
        for page in range(1, DEPTH+1):
            link = f'{BASE_URL}{GENERAL_FILTER}{LOCATION_FILTER[location]}&page={page}'
            soup = get_soup(link)
            try:
                entries = soup.select('table#forum_19 > tbody[id^="normalthread"] > tr')
                repeating = save_entry(entries, location)
                if repeating:
                    break
            except:
                print('You have reached the end for this location.')
                break
    print('Done scraping!!!')

if __name__ == "__main__":
    main()