import json
from typing import Annotated
import httpx
import supabase
import typer


client = supabase.create_client(
    supabase_url="https://civmszlljkvrbgvroohk.supabase.co",
    supabase_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpdm1zemxsamt2cmJndnJvb2hrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ4MTgyNjAsImV4cCI6MjA2MDM5NDI2MH0.zbFYu1xJYGKhCnFTVzKueBQ5QEh9l6-dmZHqyIlip-4",
)


def main(
    email: str,
    password: Annotated[str, typer.Option(prompt=True, hide_input=True)],
):
    auth = client.auth
    auth.sign_in_with_password({"email": email, "password": password})

    response = httpx.get(
        "http://localhost:8000/authed",
        headers={"Authorization": f"Bearer {auth.get_session().access_token}"},
    )
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    typer.run(main)
