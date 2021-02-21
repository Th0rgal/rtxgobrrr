import asyncio
import aiohttp
import time


class NvidiaClient:
    def __init__(self, loop, config, alerter):
        self.loop = loop
        self.config = config
        self.alerter = alerter
        self.last_error = 0
        self.content = None

    async def start(self):
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    self.loop.create_task(self.check_page(session))
                    await asyncio.sleep(self.config.nvidia_delay)
                except Exception as exception:  # we must not stop
                    if time.time() - self.last_error > 60:  # to avoid spamming errors
                        self.alerter.send_alert(f"An error occured: {exception}")
                        self.last_error = time.time()

    async def check_page(self, session):
        output = await self.query_page(session)
        if output:
            # api change detection
            if self.content != output:
                if self.content:
                    await self.alerter.send_alert("a change has been detected")
                else:
                    self.content = output

            # refill detection
            first_retailer = output["searchedProducts"]["featuredProduct"]["retailers"][
                0
            ]  # ldlc is the only retailer
            stock = first_retailer["stock"]
            url = (
                first_retailer["directPurchaseLink"]
                if "directPurchaseLink" in first_retailer
                else "null"
            )
            if stock > 0:
                await self.alerter.send_alert(f"STOCK DETECTED: {stock}, url: {url}")
            if first_retailer["hasOffer"]:
                await self.alerter.send_alert(f"OFFER DETECTED, url: {url}")

    async def query_page(self, session):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Referer": self.config.nvidia_referer,
            "User-Agent": self.config.user_agent,
        }
        async with session.get(self.config.nvidia_api_url, headers=headers) as resp:
            if resp.status == 200:
                return await resp.json()
