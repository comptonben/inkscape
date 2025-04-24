import argparse
import asyncio
import crescent
import hikari
import os
import uvloop


def run_bot(deploy: bool) -> None:
    token = os.environ["PROD_TOKEN"] if deploy else os.environ["TEST_TOKEN"]
    bot = hikari.GatewayBot(token, intents=hikari.Intents.ALL)
    client = crescent.Client(bot)
    client.plugins.load_folder("inkscape.plugins")
    bot.run()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    parser = argparse.ArgumentParser(description="Run 'The Inkscape' Discord bot")
    parser.add_argument("--deploy", type=bool, default=False, help="Set flag to True when deploying production version (Default: False)")
    args = parser.parse_args()
    run_bot(args.deploy)