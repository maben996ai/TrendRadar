from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.models import Platform, User, Video
from app.schemas.schemas import VideoResponse

router = APIRouter()


@router.get("", response_model=list[VideoResponse])
async def list_videos(
    platform: Platform | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[VideoResponse]:
    stmt = (
        select(Video)
        .options(selectinload(Video.creator))
        .join(Video.creator)
        .where(Video.creator.has(user_id=current_user.id))
        .order_by(Video.published_at.desc())
    )
    if platform is not None:
        stmt = stmt.where(Video.creator.has(platform=platform))

    result = await db.scalars(stmt)
    videos = list(result)
    return [
        VideoResponse(
            id=video.id,
            creator_id=video.creator_id,
            platform_video_id=video.platform_video_id,
            title=video.title,
            thumbnail_url=video.thumbnail_url,
            video_url=video.video_url,
            published_at=video.published_at,
            creator_name=video.creator.name,
            creator_avatar_url=video.creator.avatar_url,
            platform=video.creator.platform,
        )
        for video in videos
    ]

