import re
from datetime import UTC, datetime
from urllib.parse import ParseResult, parse_qs, urlparse

import httpx

from app.models.models import Platform
from app.services.crawlers.base import BaseCrawler, CrawledVideo, CreatorInfo

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


class BilibiliCrawler(BaseCrawler):
    platform = Platform.BILIBILI

    async def resolve_creator(self, url: str) -> CreatorInfo:
        async with httpx.AsyncClient(headers={"User-Agent": USER_AGENT}, timeout=15) as client:
            parsed = await self._normalize_url(url, client)
            uid = await self._extract_uid(parsed, client)
            if uid is None:
                raise ValueError("Unsupported Bilibili creator URL")
            response = await client.get("https://api.bilibili.com/x/space/acc/info", params={"mid": uid})
            response.raise_for_status()
            payload = response.json()

        data = payload.get("data") or {}
        if payload.get("code") not in (0, None) or not data:
            raise ValueError("Failed to resolve Bilibili creator")

        return CreatorInfo(
            platform_id=str(data["mid"]),
            name=data.get("name") or f"Bilibili {uid}",
            profile_url=f"https://space.bilibili.com/{data['mid']}",
            avatar_url=data.get("face"),
            raw_data=data,
        )

    async def fetch_latest_videos(self, creator_id: str, limit: int = 20) -> list[CrawledVideo]:
        # TODO: /x/space/arc/search was deprecated in 2023; migrate to /x/space/wbi/arc/search
        # which requires WBI request signing. See https://github.com/SocialSisterYi/bilibili-API-collect
        async with httpx.AsyncClient(headers={"User-Agent": USER_AGENT}, timeout=20) as client:
            response = await client.get(
                "https://api.bilibili.com/x/space/arc/search",
                params={"mid": creator_id, "pn": 1, "ps": limit, "order": "pubdate"},
            )
            response.raise_for_status()
            payload = response.json()

        data = payload.get("data") or {}
        videos = ((data.get("list") or {}).get("vlist")) or []
        results: list[CrawledVideo] = []
        for item in videos:
            bvid = item.get("bvid")
            if not bvid:
                continue
            results.append(
                CrawledVideo(
                    platform_video_id=bvid,
                    title=item.get("title") or bvid,
                    video_url=f"https://www.bilibili.com/video/{bvid}",
                    thumbnail_url=item.get("pic"),
                    published_at=datetime.fromtimestamp(item.get("created", 0), tz=UTC),
                    raw_data=item,
                )
            )
        return results

    async def _extract_uid(self, parsed: ParseResult, client: httpx.AsyncClient) -> str | None:
        url = parsed.geturl()
        space_match = re.search(r"space\.bilibili\.com/(\d+)", url)
        if space_match:
            return space_match.group(1)

        bv_match = re.search(r"/video/(BV[\w]+)", url)
        if bv_match:
            response = await client.get(
                "https://api.bilibili.com/x/web-interface/view",
                params={"bvid": bv_match.group(1)},
            )
            response.raise_for_status()
            payload = response.json()
            owner = (payload.get("data") or {}).get("owner") or {}
            mid = owner.get("mid")
            return str(mid) if mid else None

        query = parse_qs(parsed.query)
        if "mid" in query and query["mid"]:
            return query["mid"][0]

        return None

    async def _normalize_url(self, url: str, client: httpx.AsyncClient) -> ParseResult:
        parsed = urlparse(url)
        if parsed.netloc.lower().endswith("b23.tv"):
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            return urlparse(str(response.url))
        return parsed
