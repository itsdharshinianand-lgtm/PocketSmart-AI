from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


class RegisterRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=120,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class HomeRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000,
    )

    style: str = Field(
        default="modern",
        min_length=2,
        max_length=80,
    )

    rooms: list[str] = Field(
        min_length=1,
    )

    notes: str = Field(
        default="",
        max_length=1000,
    )

    @field_validator("rooms")
    @classmethod
    def clean_rooms(cls, value):

        value = [
            room.strip()
            for room in value
            if room.strip()
        ]

        if not value:
            raise ValueError(
                "At least one room is required"
            )

        return value


class PartyRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000,
    )

    guests: int = Field(
        gt=0,
        le=10000,
    )

    event_type: str = Field(
        min_length=2,
        max_length=80,
    )

    venue: str = Field(
        default="",
        max_length=200,
    )

    city: str = Field(
        default="",
        max_length=120,
    )

    notes: str = Field(
        default="",
        max_length=1000,
    )


class RecommendationItem(BaseModel):

    name: str

    category: str

    estimated_price: float

    platform: str

    url: str

    reason: str

    quantity: int = 1


class RecommendationResponse(BaseModel):

    planner: str

    budget: float

    total_estimated: float

    remaining_budget: float

    summary: str

    budget_breakdown: dict[str, float]

    recommendations: list[RecommendationItem]

    ai_powered: bool

    history_id: int | None = None


class HistoryItem(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    planner: str

    budget: float

    created_at: Any