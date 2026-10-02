import json

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy import select

from sqlalchemy.orm import Session

from ..database import get_db

from ..dependencies import get_current_user

from ..models import (
    RecommendationHistory,
    User,
)


router = APIRouter(
    tags=["History"]
)


@router.get("/api/history")
def history(
    db: Session = Depends(get_db),
    user: User = Depends(
        get_current_user
    ),
):

    rows = db.scalars(

        select(
            RecommendationHistory
        )

        .where(
            RecommendationHistory.user_id
            == user.id
        )

        .order_by(
            RecommendationHistory.created_at.desc()
        )
    ).all()

    return [

        {

            "id": row.id,

            "planner":
                row.planner,

            "budget":
                row.budget,

            "created_at":
                (
                    row.created_at.isoformat()
                    if row.created_at
                    else None
                ),
        }

        for row in rows

    ]


@router.get(
    "/recommendations-details/{history_id}"
)
def recommendation_details(

    history_id: int,

    db: Session = Depends(get_db),

    user: User = Depends(
        get_current_user
    ),
):

    row = db.scalar(

        select(
            RecommendationHistory
        )

        .where(

            RecommendationHistory.id
            == history_id,

            RecommendationHistory.user_id
            == user.id,

        )
    )

    if not row:

        raise HTTPException(
            status_code=404,
            detail="Recommendation not found",
        )

    return json.loads(
        row.result_json
    )
