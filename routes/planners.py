import json

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from sqlalchemy.orm import Session

from ..database import get_db

from ..dependencies import get_current_user

from ..models import (
    User,
    RecommendationHistory,
)

from ..schemas import (
    HomeRequest,
    PartyRequest,
    RecommendationResponse,
)

from ..services.gemini_service import (
    gemini_service
)

from ..config import settings


router = APIRouter(
    tags=["Planners"]
)


def save_history(
    db,
    user,
    planner,
    budget,
    request_data,
    result,
):

    row = RecommendationHistory(

        user_id=user.id,

        planner=planner,

        budget=budget,

        request_json=json.dumps(
            request_data,
            ensure_ascii=False,
        ),

        result_json=json.dumps(
            result,
            ensure_ascii=False,
        ),
    )

    db.add(row)

    db.commit()

    db.refresh(row)

    result["history_id"] = row.id

    return result


@router.post(
    "/generate-home",
    response_model=RecommendationResponse,
)
def generate_home(
    payload: HomeRequest,
    db: Session = Depends(get_db),
    user: User = Depends(
        get_current_user
    ),
):

    data = payload.model_dump()

    result = gemini_service.generate(
        "home",
        data,
    )

    return save_history(
        db,
        user,
        "home",
        payload.budget,
        data,
        result,
    )


@router.post(
    "/generate-party",
    response_model=RecommendationResponse,
)
def generate_party(
    payload: PartyRequest,
    db: Session = Depends(get_db),
    user: User = Depends(
        get_current_user
    ),
):

    data = payload.model_dump()

    result = gemini_service.generate(
        "party",
        data,
    )

    return save_history(
        db,
        user,
        "party",
        payload.budget,
        data,
        result,
    )


@router.post(
    "/generate-jewelry",
    response_model=RecommendationResponse,
)
async def generate_jewelry(

    budget: float = Form(
        ...,
        gt=0,
        le=10_000_000,
    ),

    occasion: str = Form(
        ...,
        min_length=2,
        max_length=80,
    ),

    style: str = Form(
        ...,
        min_length=2,
        max_length=80,
    ),

    notes: str = Form(
        "",
        max_length=1000,
    ),

    outfit_image: UploadFile | None = File(
        None
    ),

    db: Session = Depends(get_db),

    user: User = Depends(
        get_current_user
    ),
):

    image_bytes = None

    mime_type = None

    if (
        outfit_image
        and outfit_image.filename
    ):

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }

        if (
            outfit_image.content_type
            not in allowed_types
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only JPEG, PNG and "
                    "WebP images are supported"
                ),
            )

        image_bytes = (
            await outfit_image.read()
        )

        max_bytes = (
            settings.max_upload_mb
            * 1024
            * 1024
        )

        if len(image_bytes) > max_bytes:

            raise HTTPException(
                status_code=413,
                detail=(
                    f"Image must be <= "
                    f"{settings.max_upload_mb} MB"
                ),
            )

        mime_type = (
            outfit_image.content_type
        )

    data = {

        "budget": budget,

        "occasion": occasion,

        "style": style,

        "notes": notes,
    }

    result = gemini_service.generate(
        "jewelry",
        data,
        image_bytes,
        mime_type,
    )

    return save_history(
        db,
        user,
        "jewelry",
        budget,
        data,
        result,
    )