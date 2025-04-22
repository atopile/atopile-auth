import webbrowser

import supabase

from atopile_auth.oauth_callback_server import get_auth_code_via_server


def login(
    client: supabase.Client,
    oauth: str | None = None,
    email: str | None = None,
    password: str | None = None,
    oauth_timeout: int = 30,
) -> None:
    """Login, or raise an exception."""

    auth = client.auth

    if oauth:
        callback_port = 8234
        oauth_response = auth.sign_in_with_oauth(
            {
                "provider": oauth,
                "options": {
                    "redirect_to": f"http://localhost:{callback_port}/auth/callback"
                },
            }
        )
        url = oauth_response.url
        webbrowser.open(url)

        code = get_auth_code_via_server(callback_port, timeout=oauth_timeout)
        client.auth.exchange_code_for_session({"auth_code": code})

    elif email and password:
        auth.sign_in_with_password({"email": email, "password": password})

    else:
        raise ValueError("No login method provided")
