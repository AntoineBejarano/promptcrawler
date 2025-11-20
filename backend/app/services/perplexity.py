"""
Perplexity API service
"""
import httpx
from typing import List
from app.config import settings


class PerplexityService:
    """Servicio para interactuar con Perplexity API"""

    def __init__(self):
        self.api_key = settings.PERPLEXITY_API_KEY
        self.base_url = "https://api.perplexity.ai/chat/completions"

    async def discover_urls(self, prompt: str, max_urls: int = 20) -> List[str]:
        """
        Descubrir URLs relevantes usando Perplexity
        """
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY no configurada")

        system_prompt = f"""Eres un asistente que encuentra URLs relevantes en la web.
Responde SOLO con una lista de URLs separadas por saltos de línea, sin texto adicional.
Máximo {max_urls} URLs."""

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 2000
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # Extraer URLs del contenido
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            urls = [line.strip() for line in content.split("\n") if line.strip().startswith("http")]
            
            return urls[:max_urls]

