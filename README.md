# atopile-auth

## Pitfalls

```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
```

This happens when trying to return the `ClaimsResponse` object, rather than the `claims` attribute/field via FastAPI.
