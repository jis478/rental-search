import json
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import SearchRequest, SearchResponse, ListingResponse
from openai_parser import parse_query
from domain_api import search_listings
from database import init_db, save_search, save_listings, get_searches, get_listing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Rental Property Search", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_listing(item: dict) -> ListingResponse:
    listing = item.get("listing", item)
    prop = listing.get("propertyDetails", {})
    price = listing.get("priceDetails", {})
    media = listing.get("media", [])
    geo = prop.get("geoLocation", {})
    advertiser = listing.get("advertiser", {})

    return ListingResponse(
        id=listing.get("id", 0),
        listing_type=listing.get("listingType"),
        price_display=price.get("displayPrice"),
        bedrooms=prop.get("bedrooms"),
        bathrooms=prop.get("bathrooms"),
        carspaces=prop.get("carspaces"),
        property_type=prop.get("propertyType"),
        suburb=prop.get("suburb"),
        state=prop.get("state"),
        postcode=prop.get("postcode"),
        address=prop.get("displayableAddress"),
        headline=listing.get("headline"),
        description=listing.get("summaryDescription"),
        image_url=media[0].get("url") if media else None,
        latitude=geo.get("latitude"),
        longitude=geo.get("longitude"),
        agent_name=advertiser.get("name"),
        listing_slug=listing.get("listingSlug"),
    )


@app.post("/api/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    try:
        parsed = await parse_query(request.query)
        logger.info(f"Parsed query: {parsed.searchParams.model_dump(exclude_none=True)}")
    except Exception as e:
        logger.error(f"OpenAI parse error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to parse query: {e}")

    search_params = parsed.searchParams.model_dump(exclude_none=True)

    try:
        raw_listings = await search_listings(search_params)
        logger.info(f"Domain API returned {len(raw_listings)} listings")
    except Exception as e:
        logger.error(f"Domain API error: {e}")
        raise HTTPException(status_code=502, detail=f"Domain API error: {e}")

    search_id = await save_search(request.query, search_params)
    await save_listings(search_id, raw_listings)

    listings = [extract_listing(item) for item in raw_listings]

    return SearchResponse(
        message=parsed.message,
        searchParams=search_params,
        listings=listings,
    )


@app.get("/api/searches")
async def list_searches():
    searches = await get_searches()
    for s in searches:
        if isinstance(s.get("search_params"), str):
            s["search_params"] = json.loads(s["search_params"])
    return searches


@app.get("/api/listings/{listing_id}")
async def get_listing_detail(listing_id: int):
    listing = await get_listing(listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if isinstance(listing.get("raw_json"), str):
        listing["raw_json"] = json.loads(listing["raw_json"])
    return listing
