import aiohttp
import crescent
import hikari

from bs4 import BeautifulSoup

plugin = crescent.Plugin[hikari.GatewayBot, None]()

COLOR_OPTIONS = [
    ("Amber", "amber"),
    ("Amethyst", "amethyst"),
    ("Emerald", "emerald"),
    ("Ruby", "ruby"),
    ("Sapphire", "sapphire"),
    ("Steel", "steel")
]

RARITY_OPTIONS = {
    ("Common", "common"),
    ("Uncommon", "uncommon"),
    ("Rare", "rare"),
    ("Super-Rare", "super+rare"),
    ("Legendary", "legendary"),
    ("Enchanted", "enchanted"),
    ("Promo", "promo")
}

INKABILITY_OPTIONS = {
    ("Inkable", "true"),
    ("Uninkable", "false")
}


@plugin.include
@crescent.command(name="card", description="Search for a Lorcana card")
class Card:
    token = crescent.option(
        str,
        description="Find cards that contain this search token",
    )
    color = crescent.option(
        str,
        description="Filter by color",
        choices=COLOR_OPTIONS,
        default=None,
    )
    cost = crescent.option(
        int,
        description="Filter by cost (0-9+)",
        default=0,
        min_value=0,
        max_value=9,
    )
    inkability = crescent.option(
        str,
        description="Filter by inkability",
        choices=INKABILITY_OPTIONS,
        default=None,
    )
    rarity = crescent.option(
        str,
        description="Filter by rarity",
        choices=RARITY_OPTIONS,
        default=None,
    )

    async def callback(self, ctx: crescent.Context) -> None:
        await ctx.respond(f"Searching for {self.token}...")

        url = f"https://dreamborn.ink/cards?contains={self.token}"

        if self.color:
            url += f"&color={self.color}"

        if self.cost:
            url += f"&cost={self.cost}"
            if self.cost == 9:
                url += "%2B"

        if self.inkability:
            url += f"&ink={self.inkability}"

        if self.rarity:
            url += f"&rarity={self.rarity}"

        await ctx.respond("about to hit the url")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.text()
                soup = BeautifulSoup(data, "html.parser")
                # target_class = "@container overflow-y-auto"
                target_div = soup.find("div")

                if target_div:
                    child_divs = target_div.find_all("div", recursive=False)
                    print(f"found {len(child_divs)} child divs")
                    for i, div in enumerate(child_divs, start=1):
                        print(f"\nDiv {i}:\n{div.prettify()}")
                else:
                    print("Didn't find div")
