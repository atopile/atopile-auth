# atopile-auth

A tiny package to help manage authentication for atopile to supabase via CLI and FastAPI.

## Installation

Client:

```bash
uv add atopile-auth
```

Server:

```bash
uv add "atopile-auth[server]"
```

## Pitfalls

```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
```

This happens when trying to return the `ClaimsResponse` object, rather than the `claims` attribute/field via FastAPI.
