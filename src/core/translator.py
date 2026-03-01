"""Translation engine with Gemini and Google Translate fallback."""
import hashlib
import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Dict, Any
import requests

from ..utils.config_loader import config


class TranslationEngine(ABC):
    """Abstract base class for translation engines."""
    
    @abstractmethod
    def translate(self, text: str, source_lang: str = "en", target_lang: str = "zh") -> str:
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        pass


class GeminiEngine(TranslationEngine):
    """Google Gemini translation engine."""
    
    def __init__(self, api_key: str = None, model: str = None, temperature: float = 0.3):
        self.api_key = api_key or config.gemini_api_key
        self.model = model or config.get('translator.gemini.model', 'gemini-2.5-flash-preview-0520')
        self.temperature = temperature or config.get('translator.gemini.temperature', 0.3)
        self._client = None
    
    def _get_client(self):
        """Lazy load Gemini client."""
        if self._client is None and self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._client = genai
            except ImportError:
                return None
        return self._client
    
    def is_available(self) -> bool:
        """Check if Gemini is available."""
        if not self.api_key:
            return False
        client = self._get_client()
        return client is not None
    
    def translate(self, text: str, source_lang: str = "en", target_lang: str = "zh") -> str:
        """Translate text using Gemini."""
        if not self.is_available():
            raise RuntimeError("Gemini is not available. Check API key.")
        
        client = self._get_client()
        if not client:
            return text
        
        # Build prompt for academic translation
        prompt = f"""You are a professional academic translator. Translate the following academic text from {source_lang} to {target_lang}.

Requirements:
1. Maintain the original formatting and structure
2. Translate figure captions as "图 X. ..." (e.g., "Figure 1" → "图 1")
3. Translate table captions as "表 X. ..." (e.g., "Table 1" → "表 1")
4. Keep technical terms in English if no standard Chinese translation exists
5. Maintain mathematical expressions and equations as-is
6. Ensure translation is fluent and academically appropriate

Text to translate:
{text}

Translation:"""

        try:
            model = client.GenerativeModel(self.model)
            generation_config = {
                'temperature': self.temperature,
                'top_p': 0.95,
                'top_k': 40,
            }
            
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            if response and response.text:
                return response.text.strip()
            return text
            
        except Exception as e:
            print(f"Gemini translation error: {e}")
            raise


class GoogleTranslateEngine(TranslationEngine):
    """Google Translate (free) fallback engine."""
    
    def __init__(self):
        self.api_url = "https://translate.googleapis.com/translate_a/single"
    
    def is_available(self) -> bool:
        return True
    
    def translate(self, text: str, source_lang: str = "en", target_lang: str = "zh") -> str:
        """Translate text using Google Translate (free)."""
        if not text or not text.strip():
            return text
        
        params = {
            'client': 'gtx',
            'sl': source_lang,
            'tl': target_lang,
            'dt': 't',
            'q': text
        }
        
        try:
            response = requests.get(self.api_url, params=params, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if result and result[0]:
                    translated_text = ''.join([item[0] for item in result[0] if item[0]])
                    return translated_text
        except Exception as e:
            print(f"Google Translate error: {e}")
        
        return text


class TranslationCache:
    """Cache for translations to avoid redundant API calls."""
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = self.cache_dir / "translations.json"
        self._cache: Dict[str, str] = {}
        self._load_cache()
    
    def _load_cache(self):
        """Load cache from file."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self._cache = json.load(f)
            except:
                self._cache = {}
    
    def _save_cache(self):
        """Save cache to file."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self._cache, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def _get_key(self, text: str, source_lang: str, target_lang: str) -> str:
        """Generate cache key."""
        content = f"{source_lang}:{target_lang}:{text[:500]}"  # Limit text length for key
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def get(self, text: str, source_lang: str = "en", target_lang: str = "zh") -> Optional[str]:
        """Get cached translation."""
        key = self._get_key(text, source_lang, target_lang)
        return self._cache.get(key)
    
    def set(self, text: str, translation: str, source_lang: str = "en", target_lang: str = "zh"):
        """Cache a translation."""
        key = self._get_key(text, source_lang, target_lang)
        self._cache[key] = translation
        self._save_cache()
    
    def clear(self):
        """Clear all cache."""
        self._cache = {}
        self._save_cache()


class Translator:
    """Main translator with fallback support."""
    
    def __init__(self, config=None):
        self.config = config or config
        self.gemini = GeminiEngine() if config.is_gemini_configured else None
        self.google = GoogleTranslateEngine()
        
        # Initialize cache
        cache_enabled = config.get('cache.enabled', True)
        cache_dir = config.get('cache.dir', 'cache')
        self.cache = TranslationCache(cache_dir) if cache_enabled else None
        
        # Determine primary and fallback
        primary_name = config.get('translator.primary', 'gemini') if config else 'gemini'
        
        if primary_name == 'gemini' and self.gemini and self.gemini.is_available():
            self.primary = self.gemini
            self.fallback = self.google
        else:
            self.primary = self.google
            self.fallback = None
    
    def translate(self, text: str, source_lang: str = "en", target_lang: str = "zh") -> str:
        """Translate text with fallback support."""
        if not text or not text.strip():
            return text
        
        # Check cache first
        if self.cache:
            cached = self.cache.get(text, source_lang, target_lang)
            if cached:
                return cached
        
        # Try primary translator
        try:
            result = self.primary.translate(text, source_lang, target_lang)
            if result and result != text:
                if self.cache:
                    self.cache.set(text, result, source_lang, target_lang)
                return result
        except Exception as e:
            print(f"Primary translator failed: {e}")
        
        # Try fallback
        if self.fallback:
            try:
                result = self.fallback.translate(text, source_lang, target_lang)
                if result and result != text:
                    if self.cache:
                        self.cache.set(text, result, source_lang, target_lang)
                    return result
            except Exception as e:
                print(f"Fallback translator failed: {e}")
        
        return text
    
    def translate_batch(self, texts: List[str], source_lang: str = "en", target_lang: str = "zh") -> List[str]:
        """Translate multiple texts."""
        return [self.translate(text, source_lang, target_lang) for text in texts]


# Import config for default instance
from ..utils.config_loader import config as _config

# Default translator instance
translator = Translator(_config)