import asyncio
import aiohttp


class NvidiaClient:
    def __init__(self, loop, config, alerter):
        self.loop = loop
        self.config = config
        self.alerter = alerter
        self.content = None

    async def start(self):
        while True:
            try:
                self.loop.create_task(self.check_page())
                await asyncio.sleep(self.config.nvidia_delay)
            except Exception:  # we must not stop
                pass

    async def check_page(self):
        output = await self.query_page()
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
            if stock > 0:
                await self.alerter.send_alert(f"STOCK DETECTED: {stock}")
            if first_retailer["hasOffer"]:
                await self.alerter.send_alert("OFFER DETECTED")

    async def query_page(self):
        async with aiohttp.ClientSession() as session:
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Referer": self.config.nvidia_referer,
                "User-Agent": self.config.user_agent,
            }
            async with session.get(self.config.nvidia_api_url, headers=headers) as resp:
                if resp.status == 200:
                    return await resp.json()