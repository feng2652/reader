import concurrent

import requests
from bs4 import BeautifulSoup
import re
import datetime, time
from concurrent.futures import ThreadPoolExecutor

URL = 'https://blog.edisonweii497vip.top'  # 替换为实际的目标网址
HEADERS = {
    'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def get_date_within_item(item_soup):
    # 根据实际HTML结构编写获取日期元素并转换为datetime对象的代码
    date_str = item_soup.select_one('.item-meta-li.date')  # 示例：选取包含日期的元素
    if date_str:
        return datetime.datetime.strptime(date_str.text.strip(), '%Y-%m-%d')  # 示例格式化字符串，请根据实际情况修改
    else:
        return None

def get_title_and_url(soup):
    title = ""
    live_url = ""
    content = soup.select_one('.entry-content').text if soup else ""
    zb_title = soup.select_one('.entry-title').text if soup else ""

    patterns = [
        r'源链接：\s?(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)',
        r'Pandalive-\s?([a-zA-Z0-9_]+)'
    ]

    for pattern in patterns:
        if pattern.startswith('Pandalive'):
            match = re.search(pattern, zb_title)
            if match:
                title = match.group(1)
        else:
            match = re.search(pattern, content)
            if match:
                live_url = match.group(1)
    print(title, live_url)
    return title, live_url

def main():
    print(datetime.datetime.now())

    response = requests.get(URL, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        current_date = datetime.datetime.now().date()

        playlist_items = []

        next_page = soup.select_one('ul.pagination > li.next')


        # 获取初始页面的详情页链接
        for item in soup.select('.sec-panel-body > ul.post-loop > .item'):
            detail_url = item.find('h2', class_='item-title').select_one("a")['href']
            date_element = get_date_within_item(item)
            if '000001' in detail_url:
                continue
            if date_element.date() == current_date - datetime.timedelta(days=1) or date_element.date() == current_date:
                playlist_items.append(URL+detail_url)
            else:
                next_page = None
        # 遍历所有分页（请根据实际网页结构实现分页逻辑）
        while next_page:
            next_page_url = next_page.select_one('a')['href']
            response = requests.get(URL + next_page_url, headers=HEADERS)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                next_page = soup.select_one('ul.pagination > li.next')
                for item in soup.select('.sec-panel-body > ul.post-loop > .item'):
                    detail_url = item.find('h2', class_='item-title').select_one("a")['href']
                    date_element = get_date_within_item(item)
                    if '000001' in detail_url:
                        continue
                    if date_element.date() == current_date - datetime.timedelta(days=1) or date_element.date() == current_date:
                        playlist_items.append(URL+detail_url)
                    else:
                        next_page = None
                        break

        # 使用多线程并发请求详情页获取名称和链接
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(get_title_and_url_from_detail_page, url): url for url in playlist_items}
            playlist = []
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    title, live_url = future.result()
                    if title and live_url:
                        playlist.append({'title': title, 'live_url': live_url})
                except Exception as exc:
                    print(f"Error occurred while fetching data from '{url}': {exc}")

        # 将结果写入文件
        with open("./wzaz259/pandaTV.txt", 'w', encoding='utf-8') as f:
            for item in playlist:
                f.write(f"{item['title']},{item['live_url']}\n")
         # 将结果写入文件
        with open("./wzaz259/playlist.txt", 'a', encoding='utf-8') as f:
            f.write("pandaTV,#genre#\n")
            for item in playlist:
                f.write(f"{item['title']},{item['live_url']}\n")

    print(datetime.datetime.now())

def get_title_and_url_from_detail_page(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return get_title_and_url(soup)
    else:
        return None, None

if __name__ == "__main__":
    main()
