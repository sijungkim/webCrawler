from wsgiref import headers
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
# import pandas as pd
from os import write
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

st_handler = logging.StreamHandler()
file_handler = logging.FileHandler('crawling_test.log')

st_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

st_handler.setFormatter(st_format)
file_handler.setFormatter(st_format)

logger.addHandler(st_handler)
logger.addFilter(file_handler)

class Crawler:
    def __init__(self, url):
        self.base_url = url
        self.visited_url = set()
        self.discovered_url = set()
        self.unavailable_url = set()
        logger.info(f"{self} object successfully created!")

    def crawl(self):
        current_url = self.base_url

        self.discovered_url = {current_url}
        while url_to_visit := self.discovered_url - self.visited_url - self.unavailable_url:
            current_url = url_to_visit.pop()
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            yield f"processing {current_url}"
            try:
                res = requests.get(current_url, headers=headers, timeout=10)
                # 실패하고 말건 어차피 현재 url은 다신 안돌아갈꺼니깐 
                res.raise_for_status()
            except requests.exceptions.RequestException as e:
                # print(f"not able to fetch: {current_url}, with following reason: ")
                self.unavailable_url.add(current_url)
                logger.error(f"failed: {current_url}\n", e)
            
            self.visited_url.add(current_url)
            logger.info(f"added to visited: {current_url}")
                
            soup = BeautifulSoup(res.content, 'html.parser')
            a_list = soup.select('a')

            for link in a_list:
                url_link = urljoin(self.base_url, link.get('href'))
                self.discovered_url.add(url_link)
                logger.info(f"added to discovered: {url_link}")
                
            self.dump_result()
    
    def dump_result(self):
        url_list = {
            "discovered": self.discovered_url, 
            "visited": self.visited_url, 
            "unavailable": self.unavailable_url,
            }
        for key, val in url_list.items():
            # 나중에 PATH 선택하는 것도 추가
            with open(f'{key}.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(val))
                
    def import_last_result(self, discovered, visited, unavailable):
        try:            
            with open(file=discovered, mode='r', encoding='utf-8') as f:
                self.discovered_url = set(f.read().split('\n'))
            with open(file=visited, mode='r', encoding='utf-8') as f:
                self.visited_url = set(f.read().split('\n'))
            with open(file=unavailable, mode='r', encoding='utf-8') as f:
                self.unavailable_url = set(f.read().split('\n'))
        except Exception as e:
            print(e)
    
    def print_current_job(self):
        return url