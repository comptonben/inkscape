import crescent
import hikari

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

        await ctx.respond(url)
