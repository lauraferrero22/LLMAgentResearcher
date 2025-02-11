import os
import pickle

class Cache:
    def __init__(self, cache_dir: str = "cache"):
        """Initialize the Cache object, setting the directory for cache storage."""
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_file_path(self, key: str) -> str:
        """Generate a file path for the cache key."""
        return os.path.join(self.cache_dir, f"{key}.pkl")

    def get(self, key: str):
        """Retrieve the cached result for the given key."""
        cache_file_path = self._get_cache_file_path(key)
        if os.path.exists(cache_file_path):
            with open(cache_file_path, 'rb') as f:
                return pickle.load(f)
        return None

    def set(self, key: str, value: any):
        """Store the result in the cache."""
        cache_file_path = self._get_cache_file_path(key)
        with open(cache_file_path, 'wb') as f:
            pickle.dump(value, f)

    def clear(self):
        """Clear all cached files."""
        for filename in os.listdir(self.cache_dir):
            file_path = os.path.join(self.cache_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
