import re

from app.models.models import Platform
from app.services.crawlers.base import CreatorInfo
from app.services.crawlers.registry import crawler_registry

PLATFORM_PATTERNS: dict[Platform, tuple[str, ...]] = {
    Platform.BILIBILI: (
        r"https?://space\.bilibili\.com/\d+",
        r"https?://(?:www\.)?bilibili\.com/video/BV[\w]+",
        r"https?://b23\.tv/[\w]+",
    ),
    Platform.YOUTUBE: (
        r"https?://(?:www\.)?youtube\.com/channel/[\w-]+",
        r"https?://(?:www\.)?youtube\.com/@[\w.-]+",
    ),
}


async def resolve_creator(url: str) -> tuple[Platform, CreatorInfo]:
    normalized_url = url.strip()
    for platform, patterns in PLATFORM_PATTERNS.items():
        if any(re.search(pattern, normalized_url, flags=re.IGNORECASE) for pattern in patterns):
            crawler = crawler_registry.get(platform)
            creator = await crawler.resolve_creator(normalized_url)
            return platform, creator

    raise ValueError("Unsupported creator URL")

