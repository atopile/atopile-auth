import json
import os
import time
from typing import Annotated

import httpx
import platformdirs
import supabase
import typer
from supabase.lib.client_options import ClientOptions
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


client = supabase.create_client(
    supabase_url="https://civmszlljkvrbgvroohk.supabase.co",
    supabase_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpdm1zemxsamt2cmJndnJvb2hrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ4MTgyNjAsImV4cCI6MjA2MDM5NDI2MH0.zbFYu1xJYGKhCnFTVzKueBQ5QEh9l6-dmZHqyIlip-4",
    options=ClientOptions(storage=SyncDataDirStorage("atopile")),
)

app = typer.Typer()


@app.command()
def login(
    email: str,
    password: Annotated[str, typer.Option(prompt=True, hide_input=True)],
):
    auth = client.auth
    auth.sign_in_with_password({"email": email, "password": password})


@app.command()
def test():
    auth = client.auth
    response = httpx.get(
        "http://localhost:8000/authed",
        headers={"Authorization": f"Bearer {auth.get_session().access_token}"},
    )
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    app()
