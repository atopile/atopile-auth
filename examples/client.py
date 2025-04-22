import json
import os
from pathlib import Path

import httpx
import platformdirs
import supabase
import typer
from supabase.lib.client_options import ClientOptions
import atopile_auth
import atopile_auth.client
from atopile_auth.data_dir_storage import SyncDataDirStorage


client = supabase.create_client(
    supabase_url=os.getenv("SUPABASE_URL"),
    supabase_key=os.getenv("SUPABASE_KEY"),
    options=ClientOptions(
        storage=SyncDataDirStorage(
            Path(platformdirs.user_data_dir("atopile", ensure_exists=True))
            / "auth.json"
        )
    ),
)

app = typer.Typer()


@app.command()
def login(
    oauth: str | None = None,
    email: str | None = None,
    password: str | None = None,
):
    if oauth:
        atopile_auth.client.oauth_login(client, provider=oauth)
    elif email and password:
        client.auth.sign_in_with_password({"email": email, "password": password})
    else:
        print("No login method provided")
        raise typer.Abort()

    print("Logged in.")


@app.command()
def demo():
    auth = client.auth
    response = httpx.get(
        "http://localhost:8000/authed",
        headers={"Authorization": f"Bearer {auth.get_session().access_token}"},
    )
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    app()
