import json
import platformdirs
from gotrue import SyncSupportedStorage
from pathlib import Path


class SyncDataDirStorage(SyncSupportedStorage):
    def __init__(self, application_name: str):
        config_dir = Path(
            platformdirs.user_data_dir(application_name, ensure_exists=True)
        )
        self._cache_file = config_dir / "auth.json"

        self._cache: dict[str, str] | None = None

    def _get_cache(self) -> dict[str, str]:
        if self._cache is None:
            try:
                with open(self._cache_file, "r") as f:
                    self._cache = json.load(f)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                self._cache = {}

        return self._cache

    def _save_cache(self) -> None:
        with open(self._cache_file, "w") as f:
            json.dump(self._cache, f)

    def get_item(self, key: str) -> str | None:
        if key in self._get_cache():
            return self._get_cache()[key]
        else:
            return None

    def set_item(self, key: str, value: str) -> None:
        self._get_cache()[key] = value
        self._save_cache()

    def remove_item(self, key: str) -> None:
        if key in self._get_cache():
            del self._get_cache()[key]
            self._save_cache()
