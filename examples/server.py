import os

import supabase
from fastapi import FastAPI, Security

from atopile_auth.supabase_bearer import SupabaseBearer

client = supabase.create_client(
    supabase_url=os.getenv("SUPABASE_URL"),
    supabase_key=os.getenv("SUPABASE_KEY"),
)


supabase_jwt = SupabaseBearer(client)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/authed")
async def authed(claims_data: dict = Security(supabase_jwt)):
    # The claims_data from supabase contains 'claims', 'headers', and 'signature'.
    # We typically only want to return the actual 'claims'.
    return {"claims": claims_data.get("claims")}
