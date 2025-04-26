from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .routers import firm, user, auth, vote, report, count
# import aiosqlite

# models.Base.metadata.create_all(bind=engine)

api_description = """ 
This API provides read-only access to info from Money Market Fund Hub API.
The endpoints are grouped into the following categories:

## Analytics
Get information about the health of the API and counts of firms, users,
and votes.

## Firm
You can get a list of licenced Kenyan Money Market Fund Managers firms, or search for an individual firm by
firm_id.

## Rates
You can get a list of fund managers reports, including the effective annual rates
the reported and publised on Business Daily.

## Votes
Get information about the recommended firms as voted for by individual investors within the different firms.
"""

#FastAPI constructor with additional details added for OpenAPI Specification
app = FastAPI(
    description=api_description, 
    title="Money Market Fund Hub API", 
    version="0.1" 
)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# filename = r"C:\Users\Toshiba\Desktop"

app.include_router(firm.router)
app.include_router(report.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(count.router)
# app.include_router(auth.router)

@app.get("/", tags=["Analytics"])
async def root():
    return {"message": "Money Market Fund Hub API health check successful"}

