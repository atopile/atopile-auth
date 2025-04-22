from fastapi import FastAPI, HTTPException, Request, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import supabase
import supabase.client
import gotrue


class JWTBearer(HTTPBearer):
    def __init__(
        self,
        supabase_url: str,
        supabase_key: str,
        auto_error: bool = True,
    ):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.client = supabase.client.create_client(
            supabase_url=supabase_url,
            supabase_key=supabase_key,
        )

    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        print(credentials)
        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=403, detail="Invalid authentication scheme."
            )

        return self.client.auth.get_claims(credentials.credentials)


supabase_jwt = JWTBearer(
    supabase_url="https://civmszlljkvrbgvroohk.supabase.co",
    supabase_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpdm1zemxsamt2cmJndnJvb2hrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NDgxODI2MCwiZXhwIjoyMDYwMzk0MjYwfQ.9CgucYyw81EVY53M8hkNFVfEap7s4BrgLgSeQJMAopk",
)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/authed")
async def authed(claims_data: dict = Security(supabase_jwt)):
    # The claims_data from supabase contains 'claims', 'headers', and 'signature'.
    # We typically only want to return the actual 'claims'.
    return {"claims": claims_data.get("claims")}
