import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import func, select

from app.core.database import AsyncSessionLocal
from app.models.models import CrawlLogStatus, Creator, CrawlLog, Video
from app.services.crawlers.registry import crawler_registry


class SchedulerService:
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        self._started = False

    async def start(self) -> None:
        if self._started:
            return
        self.scheduler.add_job(crawl_all_creators, "interval", minutes=30, id="crawl_all_creators", replace_existing=True)
        self.scheduler.start()
        self._started = True

    async def stop(self) -> None:
        if not self._started:
            return
        self.scheduler.shutdown(wait=False)
        self._started = False


FIRST_CRAWL_LIMIT = 30
INCREMENTAL_CRAWL_LIMIT = 2


async def crawl_creator(creator: Creator) -> int:
    crawler = crawler_registry.get(creator.platform)

    async with AsyncSessionLocal() as db:
        existing_count = await db.scalar(
            select(func.count()).select_from(Video).where(Video.creator_id == creator.id)
        )
    limit = FIRST_CRAWL_LIMIT if (existing_count or 0) == 0 else INCREMENTAL_CRAWL_LIMIT

    videos = await crawler.fetch_latest_videos(creator.platform_creator_id, limit=limit)

    async with AsyncSessionLocal() as db:
        if not videos:
            db.add(CrawlLog(creator_id=creator.id, status=CrawlLogStatus.SUCCESS, message=None, videos_found=0))
            await db.commit()
            return 0

        fetched_ids = {v.platform_video_id for v in videos}
        existing_rows = {
            row.platform_video_id: row
            for row in await db.scalars(
                select(Video).where(
                    Video.creator_id == creator.id,
                    Video.platform_video_id.in_(fetched_ids),
                )
            )
        }

        inserted = 0
        for video in videos:
            if video.platform_video_id in existing_rows:
                row = existing_rows[video.platform_video_id]
                row.title = video.title
                row.thumbnail_url = video.thumbnail_url
                row.video_url = video.video_url
                row.raw_data = video.raw_data
            else:
                db.add(
                    Video(
                        creator_id=creator.id,
                        platform_video_id=video.platform_video_id,
                        title=video.title,
                        thumbnail_url=video.thumbnail_url,
                        video_url=video.video_url,
                        published_at=video.published_at,
                        raw_data=video.raw_data,
                    )
                )
                inserted += 1

        db.add(
            CrawlLog(
                creator_id=creator.id,
                status=CrawlLogStatus.SUCCESS,
                message=None,
                videos_found=inserted,
            )
        )
        await db.commit()
        return inserted


async def crawl_all_creators() -> None:
    async with AsyncSessionLocal() as db:
        creators = list(await db.scalars(select(Creator)))

    results = await asyncio.gather(*[crawl_creator(c) for c in creators], return_exceptions=True)

    failed = [
        (creators[i], exc)
        for i, exc in enumerate(results)
        if isinstance(exc, Exception)
    ]
    if not failed:
        return

    async with AsyncSessionLocal() as db:
        for creator, exc in failed:
            db.add(
                CrawlLog(
                    creator_id=creator.id,
                    status=CrawlLogStatus.FAILED,
                    message=str(exc),
                    videos_found=0,
                )
            )
        await db.commit()


scheduler_service = SchedulerService()

