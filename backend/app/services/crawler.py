"""
Crawl4AI service
"""
from typing import Optional
from crawl4ai import AsyncWebCrawler


class CrawlerService:
    """Servicio para crawlear páginas web usando Crawl4AI"""

    async def crawl_url(self, url: str) -> Optional[str]:
        """
        Crawlear una URL y devolver el contenido en markdown
        """
        try:
            async with AsyncWebCrawler() as crawler:
                result = await crawler.arun(url=url)
                
                if result.success and result.markdown:
                    return result.markdown
                elif result.html:
                    # Si no hay markdown, devolver HTML limpio
                    return result.html
                else:
                    return None
        except Exception as e:
            print(f"Error crawleando {url}: {e}")
            return None

