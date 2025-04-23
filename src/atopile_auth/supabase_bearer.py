import gotrue.errors
import supabase
import supabase.client
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from gotrue import ClaimsResponse


class SupabaseBearer(HTTPBearer):
    def __init__(
        self,
        supabase_client: supabase.client.Client,
        auto_error: bool = True,
        **kwargs,
    ):
        super().__init__(auto_error=auto_error, **kwargs)

        self.client = supabase_client
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request) -> ClaimsResponse | None:
        credentials = await super().__call__(request)
        if not credentials.scheme == "Bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            else:
                return None

        try:
            claims = self.client.auth.get_claims(credentials.credentials)
        except gotrue.errors.AuthInvalidJwtError:
            if self.auto_error:
                raise HTTPException(status_code=403, detail="Invalid JWT")
            else:
                return None

        if claims is None and self.auto_error:
            raise HTTPException(status_code=403, detail="No claims")

        return claims
