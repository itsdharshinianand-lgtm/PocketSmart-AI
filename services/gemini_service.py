import json
import re
from typing import Any

from google import genai
from google.genai import types

from .recommendation_service import (
    demo_home,
    demo_party,
    demo_jewelry,
)

from .platform_catalog import platform_url

from ..config import settings


class GeminiService:

    def __init__(self):

        self.enabled = bool(
            settings.gemini_api_key.strip()
        )

        if self.enabled:

            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )

        else:

            self.client = None

        self.model = settings.gemini_model


    def _json_prompt(
        self,
        planner: str,
        data: dict[str, Any],
    ) -> str:

        return f"""
You are PocketSmart AI.

You are a careful budget recommendation assistant.

Planner:
{planner}

User input:

{json.dumps(
    data,
    ensure_ascii=False,
    indent=2,
)}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "summary": "string",

    "budget_breakdown": {{
        "category": 0
    }},

    "recommendations": [
        {{
            "name": "string",
            "category": "string",
            "estimated_price": 0,
            "platform": "Amazon",
            "reason": "string",
            "quantity": 1
        }}
    ]
}}

Allowed platforms:

- Amazon
- Flipkart
- IKEA
- Swiggy
- Zomato
- OYO

Rules:

1. Use Indian Rupees.
2. Keep recommendations within the user's budget when practical.
3. Do not claim live stock information.
4. Do not claim live prices.
5. Do not claim live ratings or reviews.
6. Platform names are recommendation destinations/search sources.
7. Use realistic approximate prices.
8. Generate 4 to 8 recommendations.
9. Explain briefly why each recommendation fits.
10. Avoid unsafe or illegal recommendations.
11. Do not provide financial investment advice.
12. Return JSON only.
"""


    def _parse(
        self,
        text: str,
    ) -> dict:

        text = text.strip()

        text = re.sub(
            r"^```(?:json)?",
            "",
            text,
            flags=re.I,
        ).strip()

        text = re.sub(
            r"```$",
            "",
            text,
        ).strip()

        try:

            return json.loads(text)

        except json.JSONDecodeError:

            match = re.search(
                r"\{.*\}",
                text,
                flags=re.S,
            )

            if not match:

                raise

            return json.loads(
                match.group(0)
            )


    def _normalize(
        self,
        planner,
        data,
        payload,
        image_analyzed=False,
    ):

        budget = float(
            data["budget"]
        )

        recommendations = []

        raw_recommendations = payload.get(
            "recommendations",
            [],
        )

        for item in raw_recommendations:

            try:

                price = max(
                    0.0,
                    float(
                        item.get(
                            "estimated_price",
                            0,
                        )
                    ),
                )

                quantity = max(
                    1,
                    int(
                        item.get(
                            "quantity",
                            1,
                        )
                    ),
                )

            except (
                TypeError,
                ValueError,
            ):

                continue

            platform = item.get(
                "platform",
                "Amazon",
            )

            allowed_platforms = {
                "Amazon",
                "Flipkart",
                "IKEA",
                "Swiggy",
                "Zomato",
                "OYO",
            }

            if platform not in allowed_platforms:

                platform = "Amazon"

            name = str(
                item.get(
                    "name",
                    "Recommendation",
                )
            )

            recommendations.append(
                {
                    "name": name,

                    "category": str(
                        item.get(
                            "category",
                            "General",
                        )
                    ),

                    "estimated_price":
                        round(
                            price,
                            2,
                        ),

                    "platform":
                        platform,

                    "url":
                        platform_url(
                            platform,
                            name,
                        ),

                    "reason": str(
                        item.get(
                            "reason",
                            (
                                "Fits the stated "
                                "budget and preferences."
                            ),
                        )
                    ),

                    "quantity":
                        quantity,
                }
            )

        total = sum(
            item["estimated_price"]
            * item["quantity"]
            for item in recommendations
        )

        if total > budget and total > 0:

            factor = (
                budget
                / total
                * 0.95
            )

            for item in recommendations:

                item["estimated_price"] = round(
                    item["estimated_price"]
                    * factor,
                    2,
                )

            total = sum(
                item["estimated_price"]
                * item["quantity"]
                for item in recommendations
            )

        return {

            "planner":
                planner,

            "budget":
                budget,

            "total_estimated":
                round(total, 2),

            "remaining_budget":
                round(
                    max(
                        0,
                        budget - total,
                    ),
                    2,
                ),

            "summary":
                payload.get(
                    "summary",
                    "AI-generated budget recommendations.",
                ),

            "budget_breakdown":
                payload.get(
                    "budget_breakdown",
                    {},
                ),

            "recommendations":
                recommendations,

            "ai_powered":
                True,
        }


    def generate(
        self,
        planner,
        data,
        image_bytes=None,
        mime_type=None,
    ):

        # -------------------------------------------------
        # FALLBACK MODE
        # -------------------------------------------------

        if not self.enabled:

            if planner == "home":

                return demo_home(data)

            if planner == "party":

                return demo_party(data)

            return demo_jewelry(
                data,
                image_analyzed=bool(
                    image_bytes
                ),
            )

        # -------------------------------------------------
        # GEMINI MODE
        # -------------------------------------------------

        contents = [

            self._json_prompt(
                planner,
                data,
            )

        ]

        if image_bytes:

            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=(
                        mime_type
                        or "image/jpeg"
                    ),
                )
            )

            contents.append(
                """
Analyze the outfit image only for broad
visible color and style coordination.

Do not identify the person.
"""
            )

        response = (
            self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    temperature=0.4,
                    max_output_tokens=1800,
                    response_mime_type="application/json",
                ),
            )
        )

        payload = self._parse(
            response.text or "{}"
        )

        return self._normalize(
            planner,
            data,
            payload,
            image_analyzed=bool(
                image_bytes
            ),
        )


gemini_service = GeminiService()