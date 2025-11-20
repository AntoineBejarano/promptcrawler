"""
LLM extraction service
"""
import httpx
import json
from typing import List, Dict, Any
from app.config import settings


class ExtractorService:
    """Servicio para extraer datos estructurados usando LLM"""

    def __init__(self):
        self.openai_key = settings.OPENAI_API_KEY
        self.perplexity_key = settings.PERPLEXITY_API_KEY
        self.use_perplexity = bool(self.perplexity_key)

    async def extract_structured_data(
        self,
        prompt: str,
        content: str,
        max_items: int = 200
    ) -> List[Dict[str, Any]]:
        """
        Extraer datos estructurados del contenido usando LLM
        """
        system_prompt = f"""Eres un extractor de datos estructurados.
Extrae información relevante del contenido basándote en el prompt del usuario.
Devuelve SOLO un array JSON válido de objetos, sin texto adicional.
Cada objeto debe contener los campos relevantes extraídos.
Máximo {max_items} items."""

        user_prompt = f"""Prompt original: {prompt}

Contenido a procesar:
{content[:10000]}  # Limitar contenido a 10k caracteres

Extrae los datos relevantes en formato JSON array."""

        if self.use_perplexity:
            return await self._extract_with_perplexity(system_prompt, user_prompt, max_items)
        elif self.openai_key:
            return await self._extract_with_openai(system_prompt, user_prompt, max_items)
        else:
            # Fallback: extracción básica
            return self._basic_extraction(content, prompt)

    async def _extract_with_perplexity(
        self,
        system_prompt: str,
        user_prompt: str,
        max_items: int
    ) -> List[Dict[str, Any]]:
        """Extraer usando Perplexity"""
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.perplexity_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 4000
                }
            )
            response.raise_for_status()
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # Intentar parsear JSON
            try:
                # Buscar array JSON en el contenido
                start_idx = content.find("[")
                end_idx = content.rfind("]") + 1
                if start_idx != -1 and end_idx > start_idx:
                    json_str = content[start_idx:end_idx]
                    return json.loads(json_str)[:max_items]
            except:
                pass
            
            return []

    async def _extract_with_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        max_items: int
    ) -> List[Dict[str, Any]]:
        """Extraer usando OpenAI"""
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4-turbo-preview",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 4000,
                    "response_format": {"type": "json_object"}
                }
            )
            response.raise_for_status()
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            try:
                result = json.loads(content)
                # Si devuelve un objeto con una key, extraer el array
                if isinstance(result, dict) and len(result) == 1:
                    key = list(result.keys())[0]
                    items = result[key]
                    if isinstance(items, list):
                        return items[:max_items]
                elif isinstance(result, list):
                    return result[:max_items]
            except:
                pass
            
            return []

    def _basic_extraction(self, content: str, prompt: str) -> List[Dict[str, Any]]:
        """Extracción básica sin LLM (fallback)"""
        # Implementación básica que devuelve estructura mínima
        return [{"content": content[:500], "prompt": prompt}]

