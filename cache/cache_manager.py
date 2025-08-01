"""
Cache manager for storing scraped data with TTL support
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Optional, Dict
import aiofiles
import os

logger = logging.getLogger(__name__)

class CacheManager:
    """Simple file-based cache manager with TTL support"""
    
    def __init__(self, cache_dir: str = "cache_data"):
        self.cache_dir = cache_dir
        self._ensure_cache_dir()
        
    def _ensure_cache_dir(self):
        """Ensure cache directory exists"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def _get_cache_file_path(self, key: str) -> str:
        """Get the file path for a cache key"""
        safe_key = key.replace('/', '_').replace('\\', '_')
        return os.path.join(self.cache_dir, f"{safe_key}.json")
    
    def _get_meta_file_path(self, key: str) -> str:
        """Get the metadata file path for a cache key"""
        safe_key = key.replace('/', '_').replace('\\', '_')
        return os.path.join(self.cache_dir, f"{safe_key}.meta")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get a value from cache"""
        try:
            cache_file = self._get_cache_file_path(key)
            meta_file = self._get_meta_file_path(key)
            
            if not os.path.exists(cache_file) or not os.path.exists(meta_file):
                return None
            
            # Check if cache is expired
            async with aiofiles.open(meta_file, 'r') as f:
                meta_content = await f.read()
                meta = json.loads(meta_content)
                
            expiry_time = datetime.fromisoformat(meta['expires_at'])
            if datetime.now() > expiry_time:
                # Cache expired, remove files
                await self._remove_cache_files(key)
                return None
            
            # Return cached data
            async with aiofiles.open(cache_file, 'r') as f:
                content = await f.read()
                return json.loads(content)
                
        except Exception as e:
            logger.error(f"Error getting cache for key {key}: {str(e)}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600):
        """Set a value in cache with TTL in seconds"""
        try:
            cache_file = self._get_cache_file_path(key)
            meta_file = self._get_meta_file_path(key)
            
            # Write cache data
            async with aiofiles.open(cache_file, 'w') as f:
                await f.write(json.dumps(value, indent=2))
            
            # Write metadata
            expires_at = datetime.now() + timedelta(seconds=ttl)
            meta = {
                'key': key,
                'created_at': datetime.now().isoformat(),
                'expires_at': expires_at.isoformat(),
                'ttl': ttl
            }
            
            async with aiofiles.open(meta_file, 'w') as f:
                await f.write(json.dumps(meta, indent=2))
                
            logger.info(f"Cached data for key {key} with TTL {ttl}s")
            
        except Exception as e:
            logger.error(f"Error setting cache for key {key}: {str(e)}")
    
    async def delete(self, key: str):
        """Delete a cache entry"""
        try:
            await self._remove_cache_files(key)
            logger.info(f"Deleted cache for key {key}")
        except Exception as e:
            logger.error(f"Error deleting cache for key {key}: {str(e)}")
    
    async def _remove_cache_files(self, key: str):
        """Remove cache and meta files for a key"""
        cache_file = self._get_cache_file_path(key)
        meta_file = self._get_meta_file_path(key)
        
        if os.path.exists(cache_file):
            os.remove(cache_file)
        if os.path.exists(meta_file):
            os.remove(meta_file)
    
    async def clear_expired(self):
        """Clear all expired cache entries"""
        try:
            if not os.path.exists(self.cache_dir):
                return
                
            meta_files = [f for f in os.listdir(self.cache_dir) if f.endswith('.meta')]
            expired_count = 0
            
            for meta_file in meta_files:
                try:
                    meta_path = os.path.join(self.cache_dir, meta_file)
                    async with aiofiles.open(meta_path, 'r') as f:
                        meta_content = await f.read()
                        meta = json.loads(meta_content)
                    
                    expiry_time = datetime.fromisoformat(meta['expires_at'])
                    if datetime.now() > expiry_time:
                        key = meta['key']
                        await self._remove_cache_files(key)
                        expired_count += 1
                        
                except Exception as e:
                    logger.error(f"Error processing meta file {meta_file}: {str(e)}")
            
            if expired_count > 0:
                logger.info(f"Cleared {expired_count} expired cache entries")
                
        except Exception as e:
            logger.error(f"Error clearing expired cache: {str(e)}")
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            if not os.path.exists(self.cache_dir):
                return {"total_entries": 0, "expired_entries": 0}
            
            meta_files = [f for f in os.listdir(self.cache_dir) if f.endswith('.meta')]
            total_entries = len(meta_files)
            expired_entries = 0
            
            for meta_file in meta_files:
                try:
                    meta_path = os.path.join(self.cache_dir, meta_file)
                    async with aiofiles.open(meta_path, 'r') as f:
                        meta_content = await f.read()
                        meta = json.loads(meta_content)
                    
                    expiry_time = datetime.fromisoformat(meta['expires_at'])
                    if datetime.now() > expiry_time:
                        expired_entries += 1
                        
                except Exception:
                    continue
            
            return {
                "total_entries": total_entries,
                "expired_entries": expired_entries,
                "active_entries": total_entries - expired_entries
            }
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {str(e)}")
            return {"total_entries": 0, "expired_entries": 0}