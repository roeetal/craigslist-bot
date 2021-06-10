from typing import Dict, Generator
from time import sleep

from craigslist import CraigslistHousing
import requests
import json

from settings import SITE, CATEGORY, FILTERS
from private import EVENT_NAME, SECRET_KEY


class Bot:
    def __init__(self, nap_time=1):
        self.nap_time = nap_time
        self.send_notice("Starting bot...")
        print("Starting bot...")
        self.posts = {x['id']: x for x in self.search()}
        sleep(self.nap_time)
        self.send_notice(f"Initialized with {len(self.posts)} posts.")

    @staticmethod
    def search() -> Generator:
        bot = CraigslistHousing(site=SITE, category=CATEGORY, filters=FILTERS)
        return bot.get_results(sort_by='newest', geotagged=True)

    @staticmethod
    def send_notice(post):
        url = f"https://maker.ifttt.com/trigger/{EVENT_NAME}/with/key/{SECRET_KEY}"
        if isinstance(post, str):
            payload = json.dumps({'value1': post})
        else:
            payload = json.dumps({'value1': post, 'value2': post.pop('url')})
        headers = {
            'Content-Type': "application/json",
            'User-Agent': "PostmanRuntime/7.15.0",
            'Accept': "\*/\*",
            'Cache-Control': "no-cache",
            'Postman-Token': "a9477d0f-08ee-4960-b6f8-9fd85dc0d5cc,d376ec80-54e1-450a-8215-952ea91b01dd",
            'Host': "maker.ifttt.com",
            'accept-encoding': "gzip, deflate",
            'content-length': "63",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }
        return requests.request("POST", url, data=payload.encode('utf-8'), headers=headers)

    def updates(self) -> Dict[str, Dict]:
        updates = {x['id']: x for x in self.search()}
        new = {x['id']: x for x in updates.values() if x['id'] not in self.posts.keys()}
        self.posts.update(updates)
        return new

    def notify(self, posts: Dict[str, Dict]):
        for p in posts.values():
            self.send_notice(p)

    def run(self):
        try:
            while True:
                updates = self.updates()
                print(f'Found {len(updates.keys())} new posts!')
                self.notify(updates)
                sleep(self.nap_time)
        except Exception as e:
            self.send_notice(str(e))
        finally:
            self.send_notice("Terminating search!")


if __name__ == "__main__":
    c_bot = Bot(nap_time=1)
    c_bot.run()
