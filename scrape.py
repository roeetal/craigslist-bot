from typing import Dict, Generator
from time import sleep

from craigslist import CraigslistForSale
from spontit import SpontitResource

from settings import SITE, CATEGORY, FILTERS
from private import USERNAME, SECRET_KEY


class BikeFinder:
    def __init__(self, nap_time=1):
        self.nap_time = nap_time
        self.bot = CraigslistForSale(site=SITE, category=CATEGORY, filters=FILTERS)
        self.notification = SpontitResource(USERNAME, SECRET_KEY)
        self.notification.push("Starting bot...")
        self.posts = {x['id']: x for x in self.search()}
        sleep(self.nap_time)
        self.notification.push(f"Initialized with {len(self.posts)} posts.")

    def search(self) -> Generator:
        return self.bot.get_results(sort_by='newest', geotagged=True)

    def updates(self) -> Dict[str, Dict]:
        updates = {x['id']: x for x in self.search()}
        new = {x['id']: x for x in updates.values() if x['id'] not in self.posts.keys()}
        self.posts.update(updates)
        return new

    def notify(self, posts: Dict[str, Dict]):
        for p in posts.values():
            self.notification.push("\n".join([k + ": " + str(v) for k, v in p.items() if v is not None]))

    def run(self):
        try:
            while True:
                updates = self.updates()
                self.notify(updates)
                sleep(self.nap_time)
        finally:
            self.notification.push("Terminating search!")


if __name__ == "__main__":
    findBike = BikeFinder(nap_time=30)
    findBike.run()
