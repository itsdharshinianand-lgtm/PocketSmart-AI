from .platform_catalog import platform_url


def _item(
    name,
    category,
    price,
    platform,
    reason,
    quantity=1,
):

    return {
        "name": name,
        "category": category,
        "estimated_price": round(
            float(price),
            2,
        ),
        "platform": platform,
        "url": platform_url(
            platform,
            name,
        ),
        "reason": reason,
        "quantity": quantity,
    }


def demo_home(data):

    budget = data["budget"]

    rooms = data["rooms"]

    per_room = budget / len(rooms)

    items = []

    for room in rooms:

        items.extend(
            [

                _item(
                    f"{data['style'].title()} ceiling light for {room}",
                    "Lighting",
                    per_room * 0.12,
                    "IKEA",
                    (
                        f"Balances {data['style']} "
                        "style with a controlled room budget."
                    ),
                ),

                _item(
                    f"{data['style'].title()} area rug for {room}",
                    "Decor",
                    per_room * 0.16,
                    "Amazon",
                    (
                        "Adds texture while keeping "
                        "the allocation moderate."
                    ),
                ),

                _item(
                    f"Functional storage unit for {room}",
                    "Storage",
                    per_room * 0.22,
                    "Flipkart",
                    (
                        "Prioritizes practical storage "
                        "within the room allocation."
                    ),
                ),

            ]
        )

    total = sum(
        item["estimated_price"]
        * item["quantity"]
        for item in items
    )

    return {

        "planner": "home",

        "budget": budget,

        "total_estimated": round(
            total,
            2,
        ),

        "remaining_budget": round(
            max(0, budget - total),
            2,
        ),

        "summary": (
            f"A {data['style']} home plan for "
            f"{', '.join(rooms)} with spending "
            "distributed across lighting, decor and storage."
        ),

        "budget_breakdown": {

            "lighting":
                round(budget * 0.25, 2),

            "furniture":
                round(budget * 0.45, 2),

            "decor":
                round(budget * 0.30, 2),

        },

        "recommendations": items,

        "ai_powered": False,
    }


def demo_party(data):

    budget = data["budget"]

    guests = data["guests"]

    items = [

        _item(
            f"{data['event_type'].title()} catering for {guests} guests",
            "Catering",
            budget * 0.45,
            "Swiggy",
            (
                "Largest allocation goes to food "
                "because guest count drives cost."
            ),
        ),

        _item(
            f"{data['event_type'].title()} catering alternatives",
            "Catering",
            budget * 0.12,
            "Zomato",
            (
                "Provides a second vendor "
                "search for comparison."
            ),
        ),

        _item(
            "Event decoration package",
            "Decoration",
            budget * 0.18,
            "Amazon",
            (
                "Keeps decoration visible "
                "without consuming the majority "
                "of the budget."
            ),
        ),

        _item(
            (
                f"Event venue options in "
                f"{data.get('city') or 'your city'}"
            ),
            "Venue",
            budget * 0.20,
            "OYO",
            (
                "Useful for comparing venue "
                "and accommodation options."
            ),
        ),

    ]

    total = sum(
        item["estimated_price"]
        for item in items
    )

    return {

        "planner": "party",

        "budget": budget,

        "total_estimated": round(
            total,
            2,
        ),

        "remaining_budget": round(
            max(0, budget - total),
            2,
        ),

        "summary": (
            f"Budget allocation for a "
            f"{data['event_type']} for "
            f"{guests} guests."
        ),

        "budget_breakdown": {

            "catering":
                round(budget * 0.57, 2),

            "decoration":
                round(budget * 0.18, 2),

            "venue":
                round(budget * 0.20, 2),

            "buffer":
                round(budget * 0.05, 2),
        },

        "recommendations": items,

        "ai_powered": False,
    }


def demo_jewelry(
    data,
    image_analyzed=False,
):

    budget = data["budget"]

    occasion = data["occasion"]

    style = data["style"]

    items = [

        _item(
            f"{style.title()} earrings for {occasion}",
            "Earrings",
            budget * 0.18,
            "Amazon",
            (
                "A versatile option sized "
                "to the stated budget."
            ),
        ),

        _item(
            f"{style.title()} necklace for {occasion}",
            "Necklace",
            budget * 0.38,
            "Flipkart",
            (
                "Creates a coordinated centerpiece."
            ),
        ),

        _item(
            f"{style.title()} bracelet for {occasion}",
            "Bracelet",
            budget * 0.16,
            "Amazon",
            (
                "Adds a complementary accent "
                "without exhausting the budget."
            ),
        ),

        _item(
            f"{style.title()} jewelry set for {occasion}",
            "Set",
            budget * 0.28,
            "Flipkart",
            (
                "Useful when a coordinated "
                "set is preferred."
            ),
        ),

    ]

    total = sum(
        item["estimated_price"]
        for item in items
    )

    note = ""

    if image_analyzed:

        note = (
            " The uploaded outfit image was received "
            "for visual context."
        )

    return {

        "planner": "jewelry",

        "budget": budget,

        "total_estimated": round(
            total,
            2,
        ),

        "remaining_budget": round(
            max(0, budget - total),
            2,
        ),

        "summary": (
            f"{style.title()} jewelry suggestions "
            f"for {occasion}.{note}"
        ),

        "budget_breakdown": {

            "earrings":
                round(budget * 0.18, 2),

            "necklace":
                round(budget * 0.38, 2),

            "bracelet":
                round(budget * 0.16, 2),

            "set":
                round(budget * 0.28, 2),
        },

        "recommendations": items,

        "ai_powered": False,
    }