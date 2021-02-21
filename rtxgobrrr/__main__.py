import asyncio
from config import TomlConfig
from alerters import TelegramAlerter
from nvidia import NvidiaClient
from ldlc import LdlcClient


async def main(loop):
    config = TomlConfig("config.toml", "config.template.toml")

    alerter = TelegramAlerter(config)
    await alerter.start()

    if config.nvidia_enabled:
        nvidia_client = NvidiaClient(loop, config, alerter)
        loop.create_task(nvidia_client.start())
    if config.ldlc_enabled:
        ldlc_client = LdlcClient(loop, config, alerter)
        loop.create_task(ldlc_client.start())

    await alerter.send_alert("RTXGOBRRR started successfully")


loop = asyncio.get_event_loop()
loop.create_task(main(loop))
loop.run_forever()
