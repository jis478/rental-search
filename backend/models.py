from pydantic import BaseModel
from typing import Optional


class SearchRequest(BaseModel):
    query: str


class LocationParam(BaseModel):
    state: Optional[str] = None
    suburb: Optional[str] = None
    postcode: Optional[str] = None
    includeSurroundingSuburbs: bool = False
    surroundingRadiusInMeters: Optional[int] = None


class SearchParams(BaseModel):
    listingType: str = "Rent"
    propertyTypes: Optional[list[str]] = None
    minBedrooms: Optional[int] = None
    maxBedrooms: Optional[int] = None
    minBathrooms: Optional[int] = None
    maxBathrooms: Optional[int] = None
    minCarspaces: Optional[int] = None
    minPrice: Optional[int] = None
    maxPrice: Optional[int] = None
    locations: Optional[list[LocationParam]] = None
    keywords: Optional[list[str]] = None
    pageSize: int = 20
    pageNumber: int = 1
    sort: Optional[dict] = None


class ParsedQuery(BaseModel):
    message: str
    searchParams: SearchParams


class ListingResponse(BaseModel):
    id: int
    listing_type: Optional[str] = None
    price_display: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    carspaces: Optional[int] = None
    property_type: Optional[str] = None
    suburb: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[str] = None
    address: Optional[str] = None
    headline: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    agent_name: Optional[str] = None
    listing_slug: Optional[str] = None


class SearchResponse(BaseModel):
    message: str
    searchParams: dict
    listings: list[ListingResponse]
