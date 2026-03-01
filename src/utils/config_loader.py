"""Configuration loader for Paper Translator."""
import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Configuration manager for Paper Translator."""
    
    _instance: Optional['Config'] = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance
    
    def _load(self):
        """Load configuration from config.yaml."""
        # Find config file: ./config/config.yaml or ../config/config.yaml
        possible_paths = [
            Path(__file__).parent.parent.parent / "config" / "config.yaml",
            Path(__file__).parent.parent.parent / "config" / "config.yaml.example",
            Path.cwd() / "config" / "config.yaml",
            Path.cwd() / "config" / "config.yaml.example",
        ]
        
        config_path = None
        for path in possible_paths:
            if path.exists():
                config_path = path
                break
        
        if config_path is None:
            # Use defaults if no config found
            self._config = self._default_config()
            return
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Failed to load config: {e}")
            self._config = self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'translator': {
                'primary': 'gemini',
                'fallback': 'google',
                'gemini': {
                    'api_key': '',
                    'model': 'gemini-2.5-flash-preview-0520',
                    'temperature': 0.3
                },
                'google': {'enabled': True}
            },
            'pdf': {
                'translate_toc': False,
                'translate_figure_captions': True,
                'translate_tables': True,
                'skip_references': True,
                'image_mode': 'add_caption'
            },
            'ui': {
                'theme': 'system',
                'split_ratio': 0.5,
                'sync_scroll': True,
                'font_size': 14
            },
            'cache': {
                'dir': 'cache',
                'enabled': True
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value by dot notation key, e.g., 'translator.primary'."""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value
    
    @property
    def gemini_api_key(self) -> str:
        """Get Gemini API key."""
        key = self.get('translator.gemini.api_key', '')
        return key if key and key != 'YOUR_GEMINI_API_KEY_HERE' else ''
    
    @property
    def is_gemini_configured(self) -> bool:
        """Check if Gemini is properly configured."""
        return bool(self.gemini_api_key)
    
    @property
    def primary_translator(self) -> str:
        """Get primary translator."""
        if self.is_gemini_configured:
            return self.get('translator.primary', 'gemini')
        # Fallback to Google if no Gemini key
        return 'google'


# Global config instance
config = Config()