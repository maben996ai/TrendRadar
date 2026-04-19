import logging

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import AsyncSessionLocal, get_db
from app.models.models import ContentType, Creator, User
from app.schemas.schemas import CreatorCreate, CreatorResponse, CreatorUpdate
from app.services.resolver import resolve_creator
from app.services.scheduler import crawl_creator

router = APIRouter()
logger = logging.getLogger(__name__)


async def _run_initial_crawl(creator_id: str) -> None:
    """后台任务：独立加载 creator，再执行首次抓取。"""
    async with AsyncSessionLocal() as db:
        creator = await db.get(Creator, creator_id)
    if creator is None:
        return
    try:
        await crawl_creator(creator)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Initial crawl failed for creator=%s: %s", creator_id, exc)


@router.get("", response_model=list[CreatorResponse])
async def list_creators(
    starred: bool | None = Query(default=None),
    content_type: ContentType | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[Creator]:
    stmt = (
        select(Creator)
        .where(Creator.user_id == current_user.id)
        .order_by(Creator.created_at.desc())
    )
    if starred is not None:
        stmt = stmt.where(Creator.starred == starred)
    if content_type is not None:
        stmt = stmt.where(Creator.content_type == content_type)
    result = await db.scalars(stmt)
    return list(result)


@router.post("", response_model=CreatorResponse, status_code=status.HTTP_201_CREATED)
async def create_creator(
    payload: CreatorCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Creator:
    try:
        platform, resolved = await resolve_creator(payload.url)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    existing_creator = await db.scalar(
        select(Creator).where(
            Creator.user_id == current_user.id,
            Creator.platform == platform,
            Creator.platform_creator_id == resolved.platform_id,
        )
    )
    if existing_creator is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Creator already exists",
        )

    creator = Creator(
        user_id=current_user.id,
        platform=platform,
        platform_creator_id=resolved.platform_id,
        name=resolved.name,
        profile_url=resolved.profile_url,
        avatar_url=resolved.avatar_url,
        note=payload.note,
        content_type=payload.content_type,
    )
    db.add(creator)
    await db.commit()
    await db.refresh(creator)

    background_tasks.add_task(_run_initial_crawl, creator.id)
    return creator


@router.patch("/{creator_id}", response_model=CreatorResponse)
async def update_creator(
    creator_id: str,
    payload: CreatorUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Creator:
    creator = await db.scalar(
        select(Creator).where(
            Creator.id == creator_id,
            Creator.user_id == current_user.id,
        )
    )
    if creator is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Creator not found")

    creator.note = payload.note
    creator.category = payload.category
    if payload.starred is not None:
        creator.starred = payload.starred
    if payload.content_type is not None:
        creator.content_type = payload.content_type
    await db.commit()
    await db.refresh(creator)
    return creator


@router.delete("/{creator_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_creator(
    creator_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Response:
    creator = await db.scalar(
        select(Creator).where(
            Creator.id == creator_id,
            Creator.user_id == current_user.id,
        )
    )
    if creator is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Creator not found")

    await db.delete(creator)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

