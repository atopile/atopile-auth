import webbrowser

import supabase

from atopile_auth.oauth_callback_server import get_auth_code_via_server


def oauth_login(
    client: supabase.Client,
    provider: str,
    oauth_timeout: int = 30,
    oauth_callback_port: int = 8234,
) -> None:
    """Login, or raise an exception."""

    auth = client.auth

    oauth_response = auth.sign_in_with_oauth(
        {
            "provider": provider,
            "options": {
                "redirect_to": f"http://localhost:{oauth_callback_port}/auth/callback"
            },
        }
    )
    url = oauth_response.url
    webbrowser.open(url)

    code = get_auth_code_via_server(oauth_callback_port, timeout=oauth_timeout)
    client.auth.exchange_code_for_session({"auth_code": code})
